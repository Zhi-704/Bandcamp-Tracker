-- Insert into subscriber
INSERT INTO subscriber (email, name) VALUES
('john.doe@example.com', 'John Doe'),
('jane.smith@example.com', 'Jane Smith');

-- Insert into artist
INSERT INTO artist (name, url) VALUES
('The Rolling Stones', 'http://rollingstones.com'),
('The Beatles', 'http://thebeatles.com');

-- Insert into album
INSERT INTO album (title, artist_id, url) VALUES
('Let It Bleed', 1, 'http://rollingstones.com/let-it-bleed'),
('Abbey Road', 2, 'http://thebeatles.com/abbey-road');

-- Insert into track
INSERT INTO track (title, album_id, artist_id, url) VALUES
('Gimme Shelter', 1, 1, 'http://rollingstones.com/gimme-shelter'),
('Come Together', 2, 2, 'http://thebeatles.com/come-together');

-- Insert into country
INSERT INTO country (name) VALUES
('USA'),
('UK');

-- Insert into album_purchase
INSERT INTO album_purchase (album_id, timestamp, amount_usd, country_id) VALUES
(1, '2023-01-01 10:00:00', 9.99, 1),
(2, '2023-01-02 11:00:00', 12.99, 2);

-- Insert into track_purchase
INSERT INTO track_purchase (track_id, timestamp, amount_usd, country_id) VALUES
(1, '2023-01-01 10:05:00', 1.29, 1),
(2, '2023-01-02 11:05:00', 1.29, 2);

-- Insert into tag
INSERT INTO tag (name) VALUES
('Rock'),
('Classic');

-- Insert into album_tag_assignment
INSERT INTO album_tag_assignment (tag_id, album_id) VALUES
(1, 1),
(2, 2);

-- Insert into track_tag_assignment
INSERT INTO track_tag_assignment (tag_id, track_id) VALUES
(1, 1),
(2, 2);