DROP TABLE IF EXISTS track_tag_assignment;
DROP TABLE IF EXISTS album_tag_assignment;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS track_purchase;
DROP TABLE IF EXISTS album_purchase;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS track;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS subscriber;


CREATE TABLE subscriber (
    subscriber_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(60) NOT NULL
);

CREATE TABLE artist (
    artist_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE album (
    album_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

CREATE TABLE track (
    track_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    album_id INT NOT NULL,
    artist_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)  
);

CREATE TABLE country (
    country_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(60) UNIQUE NOT NULL
);

CREATE TABLE album_purchase (
    album_purchase_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    album_id INT NOT NULL,
    timestamp TIMESTAMP(0) NOT NULL,
    amount_usd DECIMAL(6,2) NOT NULL,
    country_id SMALLINT NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album(album_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE track_purchase (
    track_purchase_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    track_id INT NOT NULL,
    timestamp TIMESTAMP(0) NOT NULL,
    amount_usd DECIMAL(6,2) NOT NULL,
    country_id SMALLINT NOT NULL,
    FOREIGN KEY (track_id) REFERENCES track(track_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE tag (
    tag_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE album_tag_assignment (
    album_genre_assignment_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tag_id SMALLINT NOT NULL,
    album_id INT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
    FOREIGN KEY (album_id) REFERENCES album(album_id)
);

CREATE TABLE track_tag_assignment (
    track_tag_assignment_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tag_id SMALLINT NOT NULL,
    track_id INT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
    FOREIGN KEY (track_id) REFERENCES track(track_id)
);