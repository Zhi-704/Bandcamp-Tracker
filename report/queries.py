def get_top_5_artists_world_sales(cur: object) -> list[tuple]:
    cur.execute("""
SELECT a.name AS artist, COALESCE(SUM(ap.amount_usd), 0) + COALESCE(SUM(tp.amount_usd), 0) AS total_sales
FROM artist a
LEFT JOIN album al ON a.artist_id = al.artist_id
LEFT JOIN track t ON a.artist_id = t.artist_id
LEFT JOIN album_purchase ap ON al.album_id = ap.album_id
LEFT JOIN track_purchase tp ON t.track_id = tp.track_id
GROUP BY a.name
ORDER BY total_sales DESC LIMIT 5;""")
    result = cur.fetchall()
    return result


def get_top_5_genres_world_sales(cur: object) -> list[tuple]:
    cur.execute("""
SELECT t.name AS tag, COALESCE(SUM(ap.amount_usd), 0) + COALESCE(SUM(tp.amount_usd), 0) AS total_sales
FROM tag t
LEFT JOIN album_tag_assignment ata ON t.tag_id = ata.tag_id
LEFT JOIN track_tag_assignment tta ON t.tag_id = tta.tag_id
LEFT JOIN album_purchase ap ON ata.album_id = ap.album_id
LEFT JOIN track_purchase tp ON tta.track_id = tp.track_id
GROUP BY t.name
ORDER BY total_sales DESC LIMIT 5;""")
    result = cur.fetchall()
    return result


def get_top_5_tracks_world_sales(cur: object) -> list[tuple]:
    cur.execute("""
SELECT t.title AS track, COALESCE(SUM(tp.amount_usd), 0) AS total_sales
FROM track t
LEFT JOIN track_purchase tp ON t.track_id = tp.track_id
GROUP BY t.title
ORDER BY total_sales DESC LIMIT 5;""")
    result = cur.fetchall()
    return result


def get_top_5_countries_sales(cur: object) -> list[tuple]:
    cur.execute(f"""
SELECT c.name AS country, COALESCE(SUM(ap.amount_usd), 0) + COALESCE(SUM(tp.amount_usd), 0) AS total_sales
FROM country c
LEFT JOIN album_purchase ap ON c.country_id = ap.country_id
LEFT JOIN track_purchase tp ON c.country_id = tp.country_id
GROUP BY c.name
ORDER BY total_sales DESC LIMIT 5;""")
    result = cur.fetchall()
    return result


def get_top_5_artists_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT a.name AS artist, COALESCE(COUNT(ap.album_purchase_id), 0) + COALESCE(COUNT(tp.track_purchase_id), 0) AS total_sales_count
FROM artist a
LEFT JOIN album al ON a.artist_id = al.artist_id
LEFT JOIN track t ON a.artist_id = t.artist_id
LEFT JOIN album_purchase ap ON al.album_id = ap.album_id
LEFT JOIN track_purchase tp ON t.track_id = tp.track_id
JOIN country c ON ap.country_id = c.country_id OR tp.country_id = c.country_id
WHERE c.name = %s
GROUP BY a.name
ORDER BY total_sales_count DESC LIMIT 5;""", (country,))
    result = cur.fetchall()
    return result


def get_top_5_genres_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT t.name AS tag, COALESCE(COUNT(ap.album_purchase_id), 0) + COALESCE(COUNT(tp.track_purchase_id), 0) AS total_sales_count
FROM tag t
LEFT JOIN album_tag_assignment ata ON t.tag_id = ata.tag_id
LEFT JOIN track_tag_assignment tta ON t.tag_id = tta.tag_id
LEFT JOIN album_purchase ap ON ata.album_id = ap.album_id
LEFT JOIN track_purchase tp ON tta.track_id = tp.track_id
JOIN country c ON ap.country_id = c.country_id OR tp.country_id = c.country_id
WHERE c.name = %s
GROUP BY t.name
ORDER BY total_sales_count DESC LIMIT 5;""", (country,))
    result = cur.fetchall()
    return result


def get_top_5_tracks_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT t.title AS track, COALESCE(COUNT(tp.track_purchase_id), 0) AS total_sales_count
FROM track t
LEFT JOIN track_purchase tp ON t.track_id = tp.track_id
JOIN country c ON tp.country_id = c.country_id
WHERE c.name = %s
GROUP BY t.title
ORDER BY total_sales_count DESC LIMIT 5;""", (country,))
    result = cur.fetchall()
    return result
