# The pipeline 🚰

- Extract script
- Transform script
- Load script
- (Main) Pipeline script

`.env` variables required:

- DB_PASS
- DB_HOST
- DB_USER
- DB_NAME
- DB_PORT

Run tests with `pytest ./pipeline`

To run pipeline:
    - containerise it (docker, )

NB: Pipeline relies on access to the Bandcamp API:
- [API](https://bandcamp.com/api/salesfeed/1/get_initial)
- [The website](https://bandcamp.com/)

NB: HTTPS STATUS CODE: 429 is inevitable due to the number of requests being made when scraping for data. This pipeline simply omits any sales that have missing scraped data. These sales are mentioned in the logs and are viewable via AWS.