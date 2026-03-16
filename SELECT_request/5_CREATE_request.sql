--genre — Жанр (N:N к артисту)
CREATE TABLE IF NOT EXISTS genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL           -- имя жанра
);

-- artist — Артист
CREATE TABLE IF NOT EXISTS artist (
    id SERIAL PRIMARY KEY,                   
    name VARCHAR(50) NOT NULL               -- Имя артиста
);
    
--artist_genre — ПОСРЕДНИК N:N (артисты - жанры)
CREATE TABLE IF NOT EXISTS artist_genre (   	 -- артист может иметь много жанров, жанр - много артистов
    artist_id INT REFERENCES artist(id),	  -- внешний ключ на артиста
    genre_id INT REFERENCES genre(id),		  -- внешний ключ на жанр
    PRIMARY KEY (artist_id, genre_id)        	 -- составной первичный ключ (оба поля уникальны вместе)
);

--album — Альбом (N:N к артисту)
CREATE TABLE IF NOT EXISTS album (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- имя альбома
    year INT NOT NULL			-- год альбома
);

ALTER TABLE album  				   -- изменить таблицу album
ADD CONSTRAINT check_album_year_valid   -- добавить ограничение с именем check_album_year_valid
CHECK (year BETWEEN 1900 AND 2026);	 -- проверять, что столбик year находится (BETWEEN) между 1900 и 2026


--artist_album — ПОСРЕДНИК N:N (артисты - альбомы)
CREATE TABLE IF NOT EXISTS artist_album (
    artist_id INT REFERENCES artist(id),		-- внешний ключ на артиста
    album_id INT REFERENCES album(id),			-- внешний ключ на альбом
    PRIMARY KEY (artist_id, album_id)          		 -- составной первичный ключ
);

--track — трек (принадлежит строго одному альбому)
CREATE TABLE IF NOT EXISTS track (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,                    -- имя трека
    duration_seconds INT NOT NULL,                 -- длительность трека В СЕКУНДАХ 
    album_id INT REFERENCES album(id)              -- внешний ключ на альбом (отношение 1:N)
);

ALTER TABLE track  					-- изменить таблицу track  
ADD CONSTRAINT check_track_duration_range  		-- добавить ограничение
CHECK (duration_seconds BETWEEN 1 AND 7200); 		-- проверка


--collection — Сборник 
CREATE TABLE IF NOT EXISTS collection (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- имя сборника
    year INT NOT NULL			-- год выпуска сборника
);


ALTER TABLE collection   				-- изменить таблицу collection   
ADD CONSTRAINT check_collection_year_valid 		-- добавить ограничение
CHECK (year BETWEEN 1900 AND 2026); 			-- проверка

--track_collection — ПОСРЕДНИК N:N (треки - сборники)
CREATE TABLE IF NOT EXISTS track_collection (
    track_id INT REFERENCES track(id),		   	  -- внешний ключ на трек
    collection_id INT REFERENCES collection(id),  	 -- внешний ключ на сборник
    PRIMARY KEY (track_id, collection_id) 		-- составной первичный ключ
);


