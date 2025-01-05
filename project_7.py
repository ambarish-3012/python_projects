import os
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Constants
RSS_FILE = "./rss_feed.xml"
OUTPUT_FILE = "./output.txt"
MAX_THREADS = 5

def ensure_file_exists(file_path):
    """Ensures the file exists."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

def load_rss_links(rss_file):
    """Loads links from an RSS XML file."""
    try:
        ensure_file_exists(rss_file)
        tree = ET.parse(rss_file)
        root = tree.getroot()
        links = []
        for item in root.findall(".//item"):
            link = item.find("link")
            if link is not None and link.text:
                links.append(link.text)
        if not links:
            raise ValueError("No links found in the RSS file.")
        return links
    except ET.ParseError:
        raise ValueError("RSS file is not a valid XML.")
    except Exception as e:
        raise Exception(f"Error loading RSS links: {e}")

def fetch_content_from_link(link):
    """Fetches content from a given URL."""
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching content from {link}: {e}"

def write_to_output_file(content, output_file):
    """Writes content to the output file."""
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(content)
            file.write("\n" + "-"*80 + "\n")
    except Exception as e:
        raise Exception(f"Error writing to output file: {e}")

def process_links(links, output_file):
    """Processes all links using threading and writes content to the output file."""
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(fetch_content_from_link, links)
        for link, content in zip(links, results):
            content_header = f"Content from link: {link}\n{'='*80}\n"
            write_to_output_file(content_header + content, output_file)

def main():
    try:
        # Load RSS links
        links = load_rss_links(RSS_FILE)

        # Ensure output file exists and clear it
        if os.path.exists(OUTPUT_FILE):
            open(OUTPUT_FILE, 'w').close()

        # Process links and write content to output file
        process_links(links, OUTPUT_FILE)

        print(f"Content from all links successfully written to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
