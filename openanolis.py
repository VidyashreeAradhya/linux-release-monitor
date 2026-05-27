import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# The OpenAnolis primary mirror url
BASE_MIRROR_URL = "https://mirrors.openanolis.cn/anolis/"
TOP_N = 5

def format_date(date_obj):
    """
    Convert: datetime obj -> MM/DD/YYYY
    Example: 2025-04-03 -> 4/3/2025
    """
    return f"{date_obj.month}/{date_obj.day}/{date_obj.year}"

def fetch_html_content(url):
    """
    Fetch HTML content with a robust retry-and-timeout tracking structure.
    """
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            # Printing connection logs to stderr keeps your clean stdout untainted
            print(f"Fetching: {url} (Attempt {attempt})...", file=sys.stderr)
            response = requests.get(url, headers=HEADERS, timeout=20, verify=True)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP Status Error: {response.status_code}", file=sys.stderr)
                
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
            
        if attempt < retries:
            print("Retrying in 5 seconds...", file=sys.stderr)
            time.sleep(5)
            
    return None

def get_anolis_releases():
    """
    Crawls OpenAnolis directories, targets exact x86_64 community builds, 
    parses release timestamps, and extracts the 6 latest versions.
    """
    print(f"Scanning main mirror index: {BASE_MIRROR_URL}", file=sys.stderr)
    root_html = fetch_html_content(BASE_MIRROR_URL)
    if not root_html:
        print("[ERROR] Max retries exceeded completely for the root mirror index.", file=sys.stderr)
        return []

    soup = BeautifulSoup(root_html, "html.parser")
    
    # 1. Discover potential version entries (e.g., '8.8/', '8.10/', '23.4/')
    # Single-digit pointers like '8/' or '23/' are skipped as they are structural aliases/symlinks.
    version_dirs = []
    for link in soup.find_all("a"):
        href = link.get('href', '')
        if re.match(r'^\d+\.\d+/?$', href):
            version_dirs.append(href.strip('/'))

    # Deduplicate and sort
    version_dirs = sorted(list(set(version_dirs)))
    
    release_data = []

    # 2. Iterate through versions and target the x86_64 path explicitly
    for version in version_dirs:
        # OpenAnolis structures stable production x86_64 ISOs under this definitive path
        target_iso_url = f"{BASE_MIRROR_URL}{version}/isos/GA/x86_64/"
        html_content = fetch_html_content(target_iso_url)
        
        if not html_content:
            continue
            
        iso_soup = BeautifulSoup(html_content, "html.parser")
        text_lines = iso_soup.get_text().split('\n')
        
        for line in text_lines:
            # We target the master installation DVD ISO file for correct context
            if f"AnolisOS-{version}" in line and "-x86_64-dvd.iso" in line:
                
                # Look for standard server file timestamp patterns: DD-MMM-YYYY or YYYY-MM-DD
                date_human_match = re.search(r'(\d{2}-[A-Za-z]{3}-\d{4})', line)
                date_iso_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                
                parsed_date = None
                if date_human_match:
                    try:
                        parsed_date = datetime.strptime(date_human_match.group(1), "%d-%b-%Y")
                    except ValueError:
                        pass
                elif date_iso_match:
                    try:
                        parsed_date = datetime.strptime(date_iso_match.group(1), "%Y-%m-%d")
                    except ValueError:
                        pass
                
                if parsed_date:
                    release_data.append({
                        "version": f"Anolis OS {version}",
                        "release_date": format_date(parsed_date),
                        "sort_date": parsed_date
                    })
                    break # Target architecture image parsed for this directory, break out

    # Filter out potential duplicate processing entries
    unique_data = {}
    for item in release_data:
        unique_data[item["version"]] = item

    final_list = list(unique_data.values())

    # 3. Sort strictly by calendar timestamp descending (Newest first)
    final_list.sort(key=lambda x: x["sort_date"], reverse=True)

    # Pick top N entries
    latest_selections = final_list[:TOP_N]

    # Format cleanly to final array
    output = []
    for item in latest_selections:
        output.append({
            "version": item["version"],
            "release_date": item["release_date"]
        })

    return output

# ── Execution ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = get_anolis_releases()
    
    print("\nLatest OpenAnolis Releases (x86_64 Community GA):\n")
    for item in data:
        print(item)