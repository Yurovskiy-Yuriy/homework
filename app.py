#app.py
#Удалено сохранение на диск. Добавлен новый роут для отдачи байтов из Celery.

import os
import io
import base64
from flask import Flask, request, jsonify, send_file
from tasks import process_upscale_task, celery_app

app = Flask(__name__)

@app.route('/upscale', methods=['POST'])
def upscale_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    input_bytes = file.read()
    task = process_upscale_task.apply_async(args=[input_bytes])
    
    return jsonify({"task_id": task.id}), 202

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery_app.AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task.state,
    }

    if task.state == 'SUCCESS':
        response["result_url"] = f"/tasks/{task_id}/result"
    elif task.state == 'FAILURE':
        response["error"] = str(task.info)

    return jsonify(response)

@app.route('/tasks/<task_id>/result', methods=['GET'])
def get_processed_file_result(task_id):
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'SUCCESS':
        # ### ДОРАБОТКА: Декодируем base64 обратно в bytes
        result_b64 = task.result
        result_bytes = base64.b64decode(result_b64)
        
        return send_file(
            io.BytesIO(result_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='upscaled_image.png'
        )
    elif task.state == 'FAILURE':
        return jsonify({"error": "Task failed"}), 500
    else:
        return jsonify({"error": "Task not ready yet"}), 202

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)