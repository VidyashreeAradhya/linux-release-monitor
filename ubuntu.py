import requests  #Used to fetch webpage content dynamically.
from bs4 import BeautifulSoup  #Used to parse HTML structure and extract required data.
import re #regex: Used for pattern matching- versions, dates, ISO filenames
from datetime import datetime
import time

# ==========================================
# Browser Headers
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ==========================================
# Retry Request Function
# ==========================================

def make_request(url):
    """
    Send HTTP request with retry logic.
    """

    retries = 3

    for attempt in range(1, retries + 1):

        try:

            print(
                f"\nFetching Ubuntu data "
                f"(Attempt {attempt})..."
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 200:

                return response

            else:

                print(
                    f"HTTP Error: "
                    f"{response.status_code}"
                )

        except requests.exceptions.Timeout:

            print(
                f"Timeout while fetching: {url}"
            )

        except Exception as e:

            print(
                f"Request failed: {e}"
            )

        if attempt < retries:

            print(
                "Retrying in 5 seconds..."
            )

            time.sleep(5)

    return None


# ==========================================
# Version Sorting Logic
# ==========================================

def version_key(version):
    """
    Convert version into sortable tuple.

    Example:
    26.04     -> (26, 4)
    24.04.4   -> (24, 4, 4)
    """

    return tuple(
        map(
            int,
            version.split(".")
        )
    )


# ==========================================
# Date Formatting
# ==========================================

def format_date(date_string):
    """
    Convert:
    2026-04-20

    TO:

    4/20/2026
    """

    try:

        date_obj = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        return (
            f"{date_obj.month}/"
            f"{date_obj.day}/"
            f"{date_obj.year}"
        )

    except Exception:

        return date_string


# ==========================================
# Fetch Exact Release Details
# ==========================================

def fetch_release_data(version):
    """
    Fetch exact Ubuntu release data
    using ISO filename matching.
    """

    url = f"https://releases.ubuntu.com/{version}/"

    response = make_request(url)

    if not response:
        return None

    if response.status_code != 200:
        return None

    try:

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        rows = soup.find_all("tr")

        target_iso = (
            f"ubuntu-{version}"
            f"-live-server-amd64.iso"
        )

        page_text = soup.get_text(
            " ",
            strip=True
        )

        for row in rows:

            row_text = row.get_text(
                " ",
                strip=True
            )

            # Match exact ISO filename
            if target_iso in row_text:

                date_match = re.search(
                    r'(\d{4}-\d{2}-\d{2})',
                    row_text
                )

                if not date_match:
                    continue

                raw_date = date_match.group(1)

                version_name = f"Ubuntu {version}"

                # Proper LTS detection
                if "LTS" in page_text:
                    version_name += " LTS"

                return {
                    "version": version_name,
                    "release_date": format_date(raw_date),
                    "raw_version": version
                }

        return None

    except Exception as e:

        print(
            f"Error parsing "
            f"{version}: {e}"
        )

        return None


# ==========================================
# Main Ubuntu Fetcher
# ==========================================

def get_ubuntu_releases():
    """
    Fetch latest 7 Ubuntu releases.
    """

    url = "https://releases.ubuntu.com/"

    response = make_request(url)

    if not response:
        return []

    if response.status_code != 200:

        print(
            f"Failed to fetch Ubuntu releases: "
            f"{response.status_code}"
        )

        return []

    try:

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        pre_tag = soup.find("pre")

        if not pre_tag:

            print(
                "Ubuntu release list not found"
            )

            return []

        lines = pre_tag.text.splitlines()

        versions = set()

        # ==================================
        # Extract Numeric Versions
        # ==================================

        for line in lines:

            line = line.strip()

            match = re.search(
                r'(\d+\.\d+(?:\.\d+)?)\/',
                line
            )

            if not match:
                continue

            version = match.group(1)

            # Ignore alias versions
            # Example:
            # Ignore 24.04
            # if 24.04.4 exists

            parts = version.split(".")

            if len(parts) == 2:

                alias_found = False

                for other_line in lines:

                    if (
                        version + "."
                    ) in other_line:

                        alias_found = True
                        break

                if alias_found:
                    continue

            versions.add(version)

        # ==================================
        # Fetch Release Data
        # ==================================

        release_data = []

        for version in versions:

            data = fetch_release_data(version)

            if data:
                release_data.append(data)

        # ==================================
        # Remove Duplicate Versions
        # ==================================

        unique_versions = {}

        for item in release_data:

            unique_versions[
                item["version"]
            ] = item

        release_data = list(
            unique_versions.values()
        )

        # ==================================
        # Sort Latest Versions
        # ==================================

        release_data.sort(
            key=lambda x: version_key(
                x["raw_version"]
            ),
            reverse=True
        )

        # ==================================
        # Take Latest 5
        # ==================================

        latest_seven = release_data[:7]

        # ==================================
        # Final Clean Output
        # ==================================

        final_output = []

        for item in latest_seven:

            final_output.append({

                "version": item["version"],

                "release_date": item["release_date"]

            })

        return final_output

    except Exception as e:

        print(
            f"Error occurred: {e}"
        )

        return []


# ==========================================
# Local Testing
# ==========================================

if __name__ == "__main__":

    data = get_ubuntu_releases()

    print("\nLatest Ubuntu Releases:\n")

    for item in data:

        print(item)