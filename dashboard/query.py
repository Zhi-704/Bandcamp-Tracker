"""
SELECT a.name AS artist, COALESCE(ap.total, 0) + COALESCE(tp.total, 0) AS total_sales
FROM artist a
LEFT JOIN (
    SELECT al.artist_id, SUM(ap.amount_usd) AS total
    FROM album al
    JOIN album_purchase ap ON al.album_id = ap.album_id
    GROUP BY al.artist_id) ap ON a.artist_id = ap.artist_id
LEFT JOIN (
    SELECT t.artist_id, SUM(tp.amount_usd) AS total
    FROM track t
    JOIN track_purchase tp ON t.track_id = tp.track_id
    GROUP BY t.artist_id) tp ON a.artist_id = tp.artist_id
GROUP BY a.name, ap.total, tp.total
ORDER BY total_sales DESC LIMIT 5;"""
