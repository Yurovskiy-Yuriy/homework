/*  Задание 3
	Написать SELECT-запросы, которые выведут информацию согласно инструкциям ниже.
Внимание: результаты запросов не должны быть пустыми, при необходимости добавьте данные в таблицы.

1.	Количество исполнителей в каждом жанре.
2.	Количество треков, вошедших в альбомы 2019–2020 годов.
3.	Средняя продолжительность треков по каждому альбому.
4.	Все исполнители, которые не выпустили альбомы в 2020 году.
5.	Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
  */

-- 1.	Количество исполнителей в каждом жанре.
SELECT 
    g.name AS жанр,
    COUNT(ag.artist_id) AS количество_исполнителей
FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY g.id, g.name
ORDER BY количество_исполнителей DESC;

-- 2.	Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT 
    COUNT(t.id) AS количество_треков
FROM track t
JOIN album a ON t.album_id = a.id
WHERE a.year BETWEEN 1980 AND 1989;  -- изменены года

-- 3.	Средняя продолжительность треков по каждому альбому.
SELECT 
    a.name AS альбом,
    a.year AS год_выпуска,
    COUNT(t.id) AS количество_треков,
    ROUND(AVG(t.duration_seconds), 2) AS средняя_длительность_секунд
    --ROUND(AVG(t.duration_seconds) / 60, 2) AS средняя_длительность_минут
FROM album a
LEFT JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.name, a.year
ORDER BY a.year;

--4.	Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT 
    a.name AS исполнитель
FROM artist a
WHERE a.id NOT IN (
    SELECT DISTINCT aa.artist_id
    FROM artist_album aa
    JOIN album al ON aa.album_id = al.id
    WHERE al.year = 2020
)
ORDER BY a.name;

-- 5.	Названия сборников, в которых присутствует Виктор Цой
SELECT DISTINCT 
    c.name AS сборник,
    c.year AS год_выпуска
FROM collection c
JOIN track_collection tc ON c.id = tc.collection_id
JOIN track t ON tc.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'Виктор Цой'
ORDER BY c.year;