import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin, urlsplit
from bs4 import BeautifulSoup

# The sitemap URL
SITEMAP_URL = "https://developers.hubspot.com/sitemap.xml"

# Base URL to filter out relevant docs pages
DOCS_BASE_URL = "https://developers.hubspot.com/docs/api/crm"

# Set of already visited URLs to avoid re-crawling
visited_urls = set()

# Function to initialize the headless browser
def init_browser():
    options = Options()
    options.headless = True  # Run in headless mode (no UI)
    driver = webdriver.Chrome(options=options)  # Chrome will be controlled by Selenium
    return driver

# Function to fetch the content of a page
def fetch_page(driver, url):
    try:
        driver.get(url)
        time.sleep(2)  # Let the page load (adjust as needed)
        return driver.page_source
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract all links from a page
def extract_links(page_content, base_url):
    links = []
    
    # Parse the page content with BeautifulSoup (from the fetched HTML)
    soup = BeautifulSoup(page_content, "html.parser")
    
    # Find all <a> tags and extract the href attribute
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        # Make the link absolute by joining with the base URL
        full_link = urljoin(base_url, link)
        
        # Ensure that the link is within the same domain and contains the DOCS_BASE_URL
        if urlparse(full_link).netloc == urlparse(base_url).netloc and full_link.startswith(DOCS_BASE_URL):
            links.append(full_link)
    
    return links

# Function to create directories based on URL path and save text content
def save_page_content(url, content):
    # Remove the scheme and netloc to get the relative path
    path = urlsplit(url).path.strip('/')
    
    # Replace slashes with os-specific directory separator
    dir_structure = os.path.join('root', *path.split('/'))
    
    # Handle the fragment (anything after #)
    fragment = urlsplit(url).fragment
    if fragment:
        # Append the fragment as part of the filename (if present)
        filename = f'content_{fragment}.txt'
    else:
        filename = 'content.txt'
    
    # Create the directory if it doesn't exist
    os.makedirs(dir_structure, exist_ok=True)
    
    # Save the text content to a file
    file_path = os.path.join(dir_structure, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved content to {file_path}")

# Function to extract the visible text from a page (excluding scripts, styles, etc.)
def extract_text(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    
    # Remove unwanted elements (scripts, styles, etc.)
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Get the visible text and clean it up
    text_content = soup.get_text(separator="\n", strip=True)
    
    # Optionally, further clean up whitespace, newlines, etc.
    text_content = "\n".join(line.strip() for line in text_content.splitlines() if line.strip())
    
    return text_content

# Function to crawl a page and recursively find links
def crawl(driver, url):
    # Avoid visiting the same URL more than once
    if url in visited_urls:
        return
    
    try:
        print(f"Crawling: {url}")
        visited_urls.add(url)
        
        # Fetch the page content
        page_content = fetch_page(driver, url)
        
        if page_content is None:
            return
        
        # Extract the text content from the page
        text_content = extract_text(page_content)
        
        # Save the page's text content to the corresponding folder
        save_page_content(url, text_content)
        
        # Extract links from the page
        links = extract_links(page_content, url)
        
        # Crawl each link (recursive crawl)
        for link in links:
            crawl(driver, link)
    
    except Exception as e:
        print(f"Error crawling {url}: {e}")

# Function to get all URLs from the sitemap XML using Selenium
def get_urls_from_sitemap(sitemap_url):
    try:
        # Start the Selenium driver
        driver = init_browser()
        
        # Fetch the sitemap page
        driver.get(sitemap_url)
        time.sleep(2)  # Allow the page to load
        
        # Get the page content and parse it with BeautifulSoup
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        
        # Find all <loc> tags in the XML structure
        urls = [loc.text for loc in soup.find_all("loc")]
        
        # Print the extracted URLs for debugging
        print(f"Extracted {len(urls)} URLs from the sitemap.")
        for url in urls[:10]:  # Print the first 10 URLs
            print(url)
        
        # Return the list of URLs
        return urls
    
    except Exception as e:
        print(f"Error fetching or parsing sitemap: {e}")
        return []
    finally:
        driver.quit()  # Close the browser after fetching the sitemap

# Main function to start crawling
def start_crawling():
    # Fetch all URLs from the sitemap
    urls = get_urls_from_sitemap(SITEMAP_URL)
    
    # Filter the URLs to include only those that start with DOCS_BASE_URL
    docs_urls = [url for url in urls if url.startswith(DOCS_BASE_URL)]
    
    if not docs_urls:
        print("No URLs found in sitemap that match the docs base URL.")
        return
    
    # Initialize the Selenium browser
    driver = init_browser()
    
    try:
        # Crawl each valid docs URL
        for url in docs_urls:
            crawl(driver, url)
    finally:
        driver.quit()  # Close the browser after crawling

# Run the crawler
if __name__ == "__main__":
    start_crawling()
