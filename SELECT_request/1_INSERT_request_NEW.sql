/* Задание 1
В этом задании заполните базу данных. В ней должно быть:
•	не менее 4 исполнителей,
•	не менее 3 жанров,
•	не менее 3 альбомов,
•	не менее 6 треков,
•	не менее 4 сборников.
Внимание: должны быть заполнены все поля каждой таблицы,
в том числе таблицы связей исполнителей с жанрами,
исполнителей с альбомами, сборников с треками. */


-- ИСПОЛНИТЕЛИ
INSERT INTO artist (name) VALUES 
('Фредди Меркьюри'),        -- id=1
('Майкл Джексон'),          -- id=2
('Элвис Пресли'),     	    -- id=3
('Виктор Цой');             -- id=4

-- ЖАНРЫ
INSERT INTO genre (name) VALUES 
('Диско'),       		    -- id=1
('Рок-н-ролл'),       		-- id=2
('Рок'),       				-- id=3
('Поп'),     	    		-- id=4
('Поп-рок'),     	    	-- id=5
('Кантри');                 -- id=6


-- АЛЬБОМЫ
INSERT INTO album (name, year) VALUES 
('The Freddie Mercury Album', 1985), -- id=1
('Barcelona', 1988),      		-- id=2
('Thriller', 1982),     			-- id=3
('Bad', 1987),            		-- id=4
('Elvis Presley', 1956),  		-- id=5
('From Elvis in Memphis', 1969),  -- id=6
('Группа крови', 1988),     		-- id=7
('Звезда по имени Солнце', 1989);  -- id=8

-- ТРЭКИ (данные могут не соответсвовать действительности)
INSERT INTO track (name, duration_seconds, album_id)  VALUES 
('The Great Pretender', 207, 2),    
('Barcelona', 337, 1),    
('Smooth Criminal', 298, 4),    
('Billie Jean', 294, 3),    
('Mystery Train', 149, 5), 
('In the Ghetto', 165, 6), 
('Группа крови', 306, 7),    
('Спокойная ночь', 324, 7),
('Звезда по имени Солнце', 225, 8);  

-- СБОРНИКИ - 
INSERT INTO collection (name, year) VALUES 
('The Freddie Mercury Album', 1992),		-- id=1
('Solo', 2000),      						-- id=2
('Number Ones', 2003),     				-- id=3
('The Essential Michael Jackson', 2005), -- id=4
('ELV1S: 30 Hits', 2002),  				-- id=5
('Elvis. Golden Records, Vol. 1', 1958),  -- id=6
('Легенды русского рока. Кино', 1997),	-- id=7
('Последний герой', 1989); 				-- id=8

-- N:N АРТИСТ-ЖАНРЫ
INSERT INTO artist_genre (artist_id, genre_id) VALUES 
(1,3),  -- Фредди Меркьюри - Рок
(1,5),  -- Фредди Меркьюри - Поп-рок
(2,4),  -- Майкл Джексон - Поп
(2,1),  -- Майкл Джексон - Диско
(3,2),  -- Элвис Пресли - Рок-н-ролл
(3,6),  -- Элвис Пресли - Кантри
(4,3);  -- Виктор Цой -  Рок

-- N:N АРТИСТ-АЛЬБОМ
INSERT INTO artist_album (artist_id, album_id) VALUES 
(1,1),  -- Фредди Меркьюри - The Freddie Mercury Album
(1,2),  -- Фредди Меркьюри - Barcelona
(2,3),  -- Майкл Джексон - Thriller
(2,4),  -- Майкл Джексон - Bad
(3,5),  -- Элвис Пресли - Elvis Presley
(3,6),  -- Элвис Пресли - From Elvis in Memphis
(4,7),  -- Виктор Цой - Группа крови
(4,8);  -- Виктор Цой - Звезда по имени Солнце

-- N:N ТРЭК-СБОРНИК (данные не соответсвуют действительности)
INSERT INTO track_collection (track_id, collection_id) VALUES 
(1,1),  -- The Great Pretender - The Freddie Mercury Album
(1,2),  -- The Great Pretender - Solo
(2,3),  -- Barcelona - Number Ones
(3,4),  -- Smooth Criminal - The Essential Michael Jackson
(4,5),  -- Billie Jean - ELV1S: 30 Hit
(5,6),  -- Mystery Train - Elvis. Golden Records, Vol. 1
(6,6),  -- In the Ghetto - Elvis. Golden Records, Vol. 1
(7,7),  -- Группа крови - Легенды русского рока. Кино
(8,7),  -- Спокойная ночь - Легенды русского рока. Кино
(7,8);  -- Звезда по имени Солнце - Последний герой 


--ДОРАБОТКА
INSERT INTO track (name, duration_seconds, album_id) VALUES 
('my own', 180, 1),
('own my', 180, 1),
('my', 180, 1),
('oh my god', 180, 1),
('myself', 180, 1),
('by myself', 180, 1),
('bemy self', 180, 1),
('myself by', 180, 1),
('by myself by', 180, 1),
('beemy', 180, 1),
('premyne', 180, 1);


