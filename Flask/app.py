from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

ads = []
next_ad_id = 1

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Flask успешно запущен и готов к работе!"})

@app.route('/ads', methods=['GET'])
def get_ads():
    return jsonify({
        "message": "Здесь будет список объявлений"
    })

@app.route('/ads', methods=['POST'])
def create_ad():
    # Получаем JSON из тела запроса
    data = request.get_json()

    # Проверка обязательных полей
    if not data:
        return jsonify({"error": "Тело запроса должно быть JSON"}), 400

    title = data.get("title")
    description = data.get("description")
    owner = data.get("owner")

    if not title or not description or not owner:
        return jsonify({
            "error": "Обязательные поля: title, description, owner"
        }), 400

    # Создаём объявление
    global next_ad_id
    ad = {
        "id": next_ad_id,
        "title": title,
        "description": description,
        "owner": owner,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    ads.append(ad)
    next_ad_id += 1

    return jsonify(ad), 201

def get_ad_or_404(ad_id):
    """Найти объявление по ID или вернуть None."""
    for ad in ads:
        if ad["id"] == ad_id:
            return ad
    return None

@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = get_ad_or_404(ad_id)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404
    return jsonify(ad), 200

@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    ad = get_ad_or_404(ad_id)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Тело запроса должно быть JSON"}), 400

    # Обновляем только переданные поля
    if "title" in data:
        ad["title"] = data["title"]
    if "description" in data:
        ad["description"] = data["description"]
    if "owner" in data:
        ad["owner"] = data["owner"]

    return jsonify(ad), 200

@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = get_ad_or_404(ad_id)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404

    ads.remove(ad)
    return jsonify({"message": "Объявление удалено"}), 200

if __name__ == '__main__':
    app.run(debug=True)