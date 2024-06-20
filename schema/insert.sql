
-- Insert data into subscriber table
INSERT INTO subscriber (email, name) VALUES ('john.doe@example.com', 'John Doe');
INSERT INTO subscriber (email, name) VALUES ('jane.smith@example.com', 'Jane Smith');
INSERT INTO subscriber (email, name) VALUES ('alice.jones@example.com', 'Alice Jones');

-- Insert data into artist table
INSERT INTO artist (name, url) VALUES ('The Beatles', 'http://thebeatles.com');
INSERT INTO artist (name, url) VALUES ('Pink Floyd', 'http://pinkfloyd.com');
INSERT INTO artist (name, url) VALUES ('Led Zeppelin', 'http://ledzeppelin.com');

-- Insert data into album table
INSERT INTO album (title, artist_id) VALUES ('Abbey Road', 1);
INSERT INTO album (title, artist_id) VALUES ('The Dark Side of the Moon', 2);
INSERT INTO album (title, artist_id) VALUES ('Led Zeppelin IV', 3);

-- Insert data into track table
INSERT INTO track (title, album_id, artist_id) VALUES ('Come Together', 1, 1);
INSERT INTO track (title, album_id, artist_id) VALUES ('Money', 2, 2);
INSERT INTO track (title, album_id, artist_id) VALUES ('Stairway to Heaven', 3, 3);

-- Insert data into country table
INSERT INTO country (name) VALUES ('United States');
INSERT INTO country (name) VALUES ('United Kingdom');
INSERT INTO country (name) VALUES ('Canada');

-- Insert data into album_purchase table
INSERT INTO album_purchase (album_id, timestamp, amount_usd, country_id) VALUES (1, '2023-01-01 12:00:00', 15.00, 1);
INSERT INTO album_purchase (album_id, timestamp, amount_usd, country_id) VALUES (2, '2023-02-01 12:00:00', 20.00, 2);
INSERT INTO album_purchase (album_id, timestamp, amount_usd, country_id) VALUES (3, '2023-03-01 12:00:00', 25.00, 3);

-- Insert data into track_purchase table
INSERT INTO track_purchase (track_id, timestamp, amount_usd, country_id) VALUES (1, '2023-01-05 12:00:00', 1.50, 1);
INSERT INTO track_purchase (track_id, timestamp, amount_usd, country_id) VALUES (2, '2023-02-05 12:00:00', 2.00, 2);
INSERT INTO track_purchase (track_id, timestamp, amount_usd, country_id) VALUES (3, '2023-03-05 12:00:00', 2.50, 3);

-- Insert data into tag table
INSERT INTO tag (name) VALUES ('Rock');
INSERT INTO tag (name) VALUES ('Classic');
INSERT INTO tag (name) VALUES ('Pop');

-- Insert data into album_tag_assignment table
INSERT INTO album_tag_assignment (tag_id, album_id) VALUES (1, 1);
INSERT INTO album_tag_assignment (tag_id, album_id) VALUES (1, 2);
INSERT INTO album_tag_assignment (tag_id, album_id) VALUES (2, 3);

-- Insert data into track_tag_assignment table
INSERT INTO track_tag_assignment (tag_id, track_id) VALUES (1, 1);
INSERT INTO track_tag_assignment (tag_id, track_id) VALUES (2, 2);
INSERT INTO track_tag_assignment (tag_id, track_id) VALUES (3, 3);