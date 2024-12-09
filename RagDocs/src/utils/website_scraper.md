# scrape_url.py Documentation

This Python script defines a function `scrape_url` that scrapes text content from a given URL, cleans it, and returns it as a string.


## Function: `scrape_url(url: str)`

This function takes a URL (string) as input and returns the cleaned text content of the webpage.

**Parameters:**

* `url (str)`: The URL of the webpage to scrape.

**Returns:**

* `str`: A string containing the cleaned text content of the webpage.  Whitespace is normalized (multiple spaces reduced to single spaces, leading/trailing whitespace removed).  Script and style tags are removed.

**Functionality:**

1. **Requesting the webpage:** It uses the `requests` library to fetch the webpage content, including a custom `User-Agent` header to avoid potential access restrictions.

2. **Parsing with BeautifulSoup:**  It uses `BeautifulSoup` with the `lxml` parser to parse the HTML content.

3. **Removing script and style tags:** It iterates through all `<script>` and `<style>` tags and removes them from the parsed HTML to avoid unwanted code or formatting elements in the extracted text.

4. **Extracting and cleaning text:** It extracts the text content from the parsed HTML using `soup.get_text()`.  It then processes this text to:
    * Remove leading/trailing whitespace from each line.
    * Split lines into phrases using double spaces as delimiters.
    * Remove empty phrases.
    * Join the remaining phrases with newline characters.

**Example Usage:**

```python
from scrape_url import scrape_url

url = "https://www.example.com"  # Replace with your target URL
text = scrape_url(url)
print(text)
```

**Dependencies:**

* `requests`
* `beautifulsoup4`
* `lxml` (recommended for faster parsing)


**Note:**  Always respect the `robots.txt` file and terms of service of the website you are scraping.  Excessive scraping may be against a website's terms of service and could lead to your IP address being blocked.
