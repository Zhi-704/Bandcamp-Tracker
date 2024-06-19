DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS item_genre_assignment;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS format;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS subscriber;


CREATE TABLE subscriber (
    subscriber_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE country (
    country_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(60) UNIQUE NOT NULL
);

CREATE TABLE format (
    format_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE artist (
    artist_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE item (
    item_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    track_title VARCHAR(255) NOT NULL,
    album_title VARCHAR(255) NOT NULL, 
    format_id INT NOT NULL,
    artist_id INT NOT NULL,
    item_url VARCHAR(255) NOT NULL,
    art_url VARCHAR(255) NOT NULL,
    FOREIGN KEY (format_id) REFERENCES format(format_id),
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id),
    CHECK (track_title IS NOT NULL OR album_title IS NOT NULL)
);

CREATE TABLE genre (
    genre_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE item_genre_assignment (
    assignment_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    item_id INT NOT NULL,
    genre_id SMALLINT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE purchase (
    purchase_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    timestamp TIMESTAMP(0) NOT NULL,
    country_id SMALLINT NOT NULL,
    amount_usd decimal(8,2) NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country(country_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);
