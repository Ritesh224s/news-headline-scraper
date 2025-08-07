import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ---------------- Configuration ---------------- #

URL = "https://www.aajtak.in/"  # You can change this to any news site
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
OUTPUT_FILE = "headlines.txt"

# ---------------- Core Functions ---------------- #

def fetch_html(url):
    """Fetch HTML content of the given URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching URL: {e}")
        return None

def parse_headlines(html):
    """Parse and return a list of headlines from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # BBC usually uses <h3> for headlines
    headlines = soup.find_all(['h1', 'h2', 'h3'])
    
    # Clean and filter headlines
    clean_headlines = []
    for tag in headlines:
        text = tag.get_text(strip=True)
        if text and len(text) > 10:  # Filter out short or empty lines
            clean_headlines.append(text)
    
    return list(dict.fromkeys(clean_headlines))  # Remove duplicates

def save_headlines(headlines):
    """Save the headlines to a .txt file with a timestamp."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Top Headlines as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for i, headline in enumerate(headlines, 1):
            f.write(f"{i}. {headline}\n")
    print(f"✅ Headlines saved to '{OUTPUT_FILE}'")

# ---------------- Main ---------------- #

def main():
    print("📰 News Headline Scraper Started...")
    html = fetch_html(URL)
    if html:
        headlines = parse_headlines(html)
        if headlines:
            save_headlines(headlines)
        else:
            print("⚠️ No headlines found.")
    else:
        print("❌ Failed to retrieve data.")

if __name__ == "__main__":
    main()
