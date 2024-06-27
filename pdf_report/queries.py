import pandas as pd


def get_top_5_artists_world_sales(cur: object) -> pd.DataFrame:
    cur.execute("""
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
ORDER BY total_sales DESC LIMIT 5;""")

    result = cur.fetchall()
    result_df = pd.DataFrame(result)
    result_df[1] = result_df[1].astype(float)
    result_df[2] = result_df[0].apply(
        lambda x: x[:12] + '...' if len(x) > 12 else x)

    return result_df


def get_top_5_tags_world_sales(cur: object) -> pd.DataFrame:
    cur.execute("""
SELECT t.name AS tag, COALESCE(ap.total, 0) + COALESCE(tp.total, 0) AS total_sales
FROM tag t
LEFT JOIN (
    SELECT ata.tag_id, SUM(ap.amount_usd) AS total
    FROM album_tag_assignment ata
    JOIN album_purchase ap ON ata.album_id = ap.album_id
    GROUP BY ata.tag_id) ap ON t.tag_id = ap.tag_id
LEFT JOIN (
    SELECT tta.tag_id, SUM(tp.amount_usd) AS total
    FROM track_tag_assignment tta
    JOIN track_purchase tp ON tta.track_id = tp.track_id
    GROUP BY tta.tag_id) tp ON t.tag_id = tp.tag_id
GROUP BY t.name, ap.total, tp.total
ORDER BY total_sales DESC LIMIT 5;""")

    result = cur.fetchall()
    result_df = pd.DataFrame(result)
    result_df[1] = result_df[1].astype(float)
    result_df[2] = result_df[0].apply(
        lambda x: x[:12] + '...' if len(x) > 12 else x)

    return result_df


def get_top_5_tracks_world_sales(cur: object) -> pd.DataFrame:
    cur.execute("""
SELECT t.title AS track, COALESCE(tp.total_sales, 0) AS total_sales
FROM track t
LEFT JOIN (
    SELECT track_id, SUM(amount_usd) AS total_sales
    FROM track_purchase
    GROUP BY track_id) tp ON t.track_id = tp.track_id
ORDER BY total_sales DESC LIMIT 5;""")

    result = cur.fetchall()
    result_df = pd.DataFrame(result)
    result_df[1] = result_df[1].astype(float)
    result_df[2] = result_df[0].apply(
        lambda x: x[:25] + '...' if len(x) > 25 else x)

    return result_df


def get_top_5_countries_sales(cur: object) -> list[tuple]:
    cur.execute(f"""
SELECT c.name AS country,COALESCE(ap.total_sales, 0) + COALESCE(tp.total_sales, 0) AS total_sales
FROM country c
LEFT JOIN (
    SELECT country_id, SUM(amount_usd) AS total_sales
    FROM album_purchase
    GROUP BY country_id) ap ON c.country_id = ap.country_id
LEFT JOIN (
    SELECT country_id, SUM(amount_usd) AS total_sales
    FROM track_purchase
    GROUP BY country_id) tp ON c.country_id = tp.country_id
GROUP BY c.name, ap.total_sales, tp.total_sales
ORDER BY total_sales DESC LIMIT 5;""")

    result = cur.fetchall()

    return result


def format_length_of_string(string: str):
    if len(string) > 25:
        return string[:25] + '...'
    return string


def get_top_5_artists_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT a.name AS artist, COALESCE(ap.total_sales_count, 0) + COALESCE(tp.total_sales_count, 0) AS total_sales_count
FROM artist a
LEFT JOIN (
    SELECT al.artist_id, COUNT(DISTINCT(ap.album_purchase_id)) AS total_sales_count
    FROM album al
    JOIN album_purchase ap ON al.album_id = ap.album_id
    JOIN country c ON ap.country_id = c.country_id
    WHERE c.name = %s
    GROUP BY al.artist_id) ap ON a.artist_id = ap.artist_id
LEFT JOIN (
    SELECT t.artist_id, COUNT(DISTINCT(tp.track_purchase_id)) AS total_sales_count
    FROM track t
    JOIN track_purchase tp ON t.track_id = tp.track_id
    JOIN country c ON tp.country_id = c.country_id
    WHERE c.name = %s
    GROUP BY t.artist_id) tp ON a.artist_id = tp.artist_id
GROUP BY a.name, ap.total_sales_count, tp.total_sales_count
ORDER BY total_sales_count DESC LIMIT 5;""", (country, country))

    result = cur.fetchall()
    formatted_result = [
        f"{i+1}. {format_length_of_string(artist)}, {value}" for i, (artist, value) in enumerate(result)]

    return formatted_result


def get_top_5_tag_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT t.name AS tag, COALESCE(ap.total_sales_count, 0) + COALESCE(tp.total_sales_count, 0) AS total_sales_count
FROM tag t
LEFT JOIN (
    SELECT ata.tag_id, COUNT(DISTINCT(ap.album_purchase_id)) AS total_sales_count
    FROM album_tag_assignment ata
    JOIN album_purchase ap ON ata.album_id = ap.album_id
    JOIN country c ON ap.country_id = c.country_id
    WHERE c.name = %s
    GROUP BY ata.tag_id) ap ON t.tag_id = ap.tag_id
LEFT JOIN (
    SELECT tta.tag_id, COUNT(DISTINCT(tp.track_purchase_id)) AS total_sales_count
    FROM track_tag_assignment tta
    JOIN track_purchase tp ON tta.track_id = tp.track_id
    JOIN country c ON tp.country_id = c.country_id
    WHERE c.name = %s
    GROUP BY tta.tag_id) tp ON t.tag_id = tp.tag_id
GROUP BY t.name, ap.total_sales_count, tp.total_sales_count
ORDER BY total_sales_count DESC LIMIT 5;""", (country, country))
    result = cur.fetchall()
    formatted_result = [
        f"{i+1}. {format_length_of_string(tag)}, {value}" for i, (tag, value) in enumerate(result)]

    return formatted_result


def get_top_5_tracks_volume_specific(cur: object, country: str) -> list[tuple]:
    cur.execute("""
SELECT t.title AS track, COALESCE(tp.total_sales_count, 0) AS total_sales_count
FROM track t
LEFT JOIN (
    SELECT tp.track_id, COUNT(DISTINCT(tp.track_purchase_id)) AS total_sales_count
    FROM track_purchase tp
    JOIN country c ON tp.country_id = c.country_id
    WHERE c.name = %s
    GROUP BY tp.track_id) tp ON t.track_id = tp.track_id
GROUP BY t.title, tp.total_sales_count
ORDER BY total_sales_count DESC LIMIT 5;""", (country,))
    result = cur.fetchall()
    formatted_result = [
        f"{i+1}. {format_length_of_string(track)}, {value}" for i, (track, value) in enumerate(result)]

    return formatted_result


def get_top_5_metrics_in_top_5_countries(cur: object, countries: list[tuple]) -> list[list]:
    country_metrics = []
    for country in countries:
        country_info = []
        country_info.append(get_top_5_artists_volume_specific(cur, country))
        country_info.append(get_top_5_tag_volume_specific(cur, country))
        country_info.append(get_top_5_tracks_volume_specific(cur, country))
        country_metrics.append(country_info)

    return country_metrics
