# import requests
# import time
# import random
# import csv
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry

# def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
#     session = requests.Session()
#     retry = Retry(
#         total=retries,
#         read=retries,
#         connect=retries,
#         backoff_factor=backoff_factor,
#         status_forcelist=status_forcelist,
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#     return session

# def get_ieee_articles(search_terms, num_pages):
#     base_url = "https://ieeexplore.ieee.org/rest/search"
#     headers = {
#         "Accept": "application/json, text/plain, */*",
#         "Origin": "https://ieeexplore.ieee.org",
#         "Content-Type": "application/json",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     session = requests_retry_session()
#     all_articles = []

#     for search_term in search_terms:
#         print(f"Searching for: {search_term}")
#         for page in range(1, num_pages + 1):
#             payload = {
#                 "newsearch": True,
#                 "queryText": search_term,
#                 "highlight": True,
#                 "returnFacets": ["ALL"],
#                 "returnType": "SEARCH",
#                 "matchPubs": True,
#                 "pageNumber": page
#             }

#             try:
#                 response = session.post(base_url, json=payload, headers=headers)
#                 response.raise_for_status()
#                 data = response.json()

#                 if "records" not in data or not data["records"]:
#                     print(f"No records found on page {page} for '{search_term}'")
#                     continue

#                 for record in data["records"]:
#                     article_title = record.get("articleTitle", "No title available")
#                     article_url = f"https://ieeexplore.ieee.org{record.get('documentLink', '#')}"
#                     abstract = record.get("abstract", "No abstract available")
#                     authors = ", ".join([author["preferredName"] for author in record.get("authors", [])])

#                     all_articles.append({
#                         "keyword": search_term,
#                         "title": article_title,
#                         "url": article_url,
#                         "abstract": abstract,
#                         "authors": authors
#                     })

#                 print(f"Scraped page {page}/{num_pages} for '{search_term}'")

#             except requests.exceptions.RequestException as e:
#                 print(f"Error occurred while scraping page {page} for '{search_term}': {e}")
#                 continue
#             except ValueError as e:
#                 print(f"Error decoding JSON on page {page} for '{search_term}': {e}")
#                 continue

#             time.sleep(random.uniform(2, 5))

#     return all_articles

# def save_to_csv(articles, filename):
#     if not articles:
#         print("No articles to save.")
#         return

#     keys = articles[0].keys()
#     with open(filename, 'w', newline='', encoding='utf-8') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(articles)

# if __name__ == "__main__":
#     search_terms = [
#         "machine learning", "artificial intelligence", "deep learning", "neural networks", "data mining",
#         "computer vision", "natural language processing", "robotics", "internet of things", "cybersecurity",
#         "big data", "cloud computing", "quantum computing", "blockchain", "augmented reality",
#         "virtual reality", "5G", "edge computing", "bioinformatics", "computer graphics",
#         "autonomous systems", "rweinforcement learning", "computational biology", "federated learning",
#         "swarm intelligence", "genetic algorithms", "digital twins", "wearable technology",
#         "smart cities", "self-driving cars", "speech recognition", "human-computer interaction",
#         "recommender systems", "semantic web", "AI ethics", "medical imaging", "sensor networks",
#         "multimodal learning", "AI in healthcare", "privacy-preserving AI", "software engineering"
#     ]

#     num_pages = 50
#     article_data = get_ieee_articles(search_terms, num_pages)

#     csv_filename = "ieee_articles.csv"
#     save_to_csv(article_data, csv_filename)
#     print(f"Saved {len(article_data)} articles to {csv_filename}")

import requests
import time
import random
import csv
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scrape_citations(citations_url):
    """
    Scrape the list of citations from the citations page using Selenium.
    """
    options = Options()
    # Run in headless mode to avoid opening browser
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    citations_list = []

    try:
        driver.get(citations_url)
        time.sleep(5)  # Allow time for JavaScript to load

        # Find citation entries (adjust based on actual page structure)
        citation_elements = driver.find_elements(
            By.CSS_SELECTOR, ".citation-content-class")  # Adjust selector

        for citation in citation_elements:
            citations_list.append(citation.text.strip())

    except Exception as e:
        print(f"Error fetching citations from {citations_url}: {e}")

    finally:
        driver.quit()

    return citations_list


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_ieee_articles(search_terms, num_pages):
    base_url = "https://ieeexplore.ieee.org/rest/search"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ieeexplore.ieee.org",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    session = requests_retry_session()
    all_articles = []

    for search_term in search_terms:
        print(f"Searching for: {search_term}")
        for page in range(1, num_pages + 1):
            payload = {
                "newsearch": True,
                "queryText": search_term,
                "highlight": True,
                "returnFacets": ["ALL"],
                "returnType": "SEARCH",
                "matchPubs": True,
                "pageNumber": page
            }

            try:
                response = session.post(
                    base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()

                if "records" not in data or not data["records"]:
                    print(
                        f"No records found on page {page} for '{search_term}'")
                    continue

                for record in data["records"]:
                    article_title = record.get(
                        "articleTitle", "No title available")
                    article_url = f"https://ieeexplore.ieee.org{record.get('documentLink', '#')}"
                    abstract = record.get("abstract", "No abstract available")
                    authors = ", ".join([author["preferredName"]
                                        for author in record.get("authors", [])])
                    # Article number needed for citation URL
                    article_number = record.get("articleNumber")
                    citations_url = f"https://ieeexplore.ieee.org/document/{article_number}/citations#citations"

                    # Scrape citations from the citations page
                    citations_list = scrape_citations(citations_url)

                    all_articles.append({
                        "keyword": search_term,
                        "title": article_title,
                        "url": article_url,
                        "abstract": abstract,
                        "authors": authors,
                        "citations_list": citations_list
                    })

                print(f"Scraped page {page}/{num_pages} for '{search_term}'")

            except requests.exceptions.RequestException as e:
                print(
                    f"Error occurred while scraping page {page} for '{search_term}': {e}")
                continue
            except ValueError as e:
                print(
                    f"Error decoding JSON on page {page} for '{search_term}': {e}")
                continue

            # To avoid being blocked by the server
            time.sleep(random.uniform(2, 5))

    return all_articles


def scrape_citations(citations_url):
    """
    Scrape the list of citations from the citations page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(citations_url, headers=headers)
        response.raise_for_status()

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find citation entries (adjust selectors based on actual HTML structure)
        # Adjust selector based on actual structure
        citation_items = soup.select('.stats-document-abstract-doi')
        print(citation_items)
        citations_list = []
        for item in citation_items:
            citation_title = item.text.strip()
            citations_list.append(citation_title)

        return citations_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching citations from {citations_url}: {e}")
        return []


def save_to_csv(articles, filename):
    if not articles:
        print("No articles to save.")
        return

    keys = articles[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(articles)


if __name__ == "__main__":
    search_terms = [
        "machine learning", "artificial intelligence", "deep learning"
        # Add more search terms here...
    ]
    num_pages = 1  # Adjust the number of pages to scrape
    article_data = get_ieee_articles(search_terms, num_pages)

    csv_filename = "ieee_articles_with_citations.csv"
    save_to_csv(article_data, csv_filename)
    print(f"Saved {len(article_data)} articles to {csv_filename}")
