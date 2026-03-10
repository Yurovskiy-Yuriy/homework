

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
CREATE TABLE IF NOT EXISTS artist_genre (    -- артист может иметь много жанров, жанр - много артистов
    artist_id INT REFERENCES artist(id),	  -- внешний ключ на артиста
    genre_id INT REFERENCES genre(id),		  -- внешний ключ на жанр
    PRIMARY KEY (artist_id, genre_id)         -- составной первичный ключ (оба поля уникальны вместе)
);

--album — Альбом (N:N к артисту)
CREATE TABLE IF NOT EXISTS album (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- имя альбома
    year INT NOT NULL					-- год альбома
);

--artist_album — ПОСРЕДНИК N:N (артисты - альбомы)
CREATE TABLE IF NOT EXISTS artist_album (
    artist_id INT REFERENCES artist(id),		-- внешний ключ на артиста
    album_id INT REFERENCES album(id),			-- внешний ключ на альбом
    PRIMARY KEY (artist_id, album_id)           -- составной первичный ключ
);

--track — трек (принадлежит строго одному альбому)
CREATE TABLE IF NOT EXISTS track (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- имя трека
    time TIME NOT NULL,                  -- длина(время) трека
    album_id INT REFERENCES album(id)       -- внешний ключ на альбом (отношение 1:N)
);

--collection — Сборник 
CREATE TABLE IF NOT EXISTS collection (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- имя альбома
    year INT NOT NULL					-- год альбома
);

--track_collection — ПОСРЕДНИК N:N (треки - сборники)
CREATE TABLE IF NOT EXISTS track_collection (
    track_id INT REFERENCES track(id),		    	-- внешний ключ на трек
    collection_id INT REFERENCES collection(id),   -- внешний ключ на сборник
    PRIMARY KEY (track_id, collection_id) 		   -- составной первичный ключ
);
