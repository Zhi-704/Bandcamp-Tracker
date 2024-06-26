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


SELECT t.name, SUM(album_table.album_total + track_table.track_total) AS total_sales
  FROM tag t
   INNER JOIN(
        SELECT ata.tag_id, COUNT(DISTINCT ap.album_purchase_id) as album_total
        FROM album_tag_assignment ata
        INNER JOIN album_purchase ap
        ON ata.album_id=ap.album_id
        GROUP BY ata.tag_id)
      album_table ON album_table.tag_id = t.tag_id
    INNER JOIN(
        SELECT tta.tag_id, COUNT(DISTINCT tp.track_purchase_id) as track_total
        FROM track_tag_assignment tta
        INNER JOIN track_purchase tp
        ON tta.track_id=tp.track_id
        GROUP BY tta.tag_id)
      track_table ON track_table.tag_id = t.tag_id
    GROUP BY t.tag_id
    ORDER BY total_sales DESC
    LIMIT % s