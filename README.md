# Broadway Grosses Scraper

A python webscraper using [Selenium](https://selenium-python.readthedocs.io/) to get gross revenue and additional figures for braodway shows from the [Broadway League's website](https://www.broadwayleague.com/research/grosses-broadway-nyc/). Data dates back to the 1980-1981 Broadway Season. Between each week scrape, script sleeps for 0-3 seconds.

To scrape run the following in terminal:
```
pip install -r requirements.txt
python3 scraper.py
```