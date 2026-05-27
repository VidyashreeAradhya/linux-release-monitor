import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


URL = "https://access.redhat.com/articles/3078"


def format_date(date_string):
    """
    Convert:
    2025-05-20 -> 5/20/2025
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


def fetch_rhel_page():
    """
    Fetch RHEL page with retry logic.
    """

    retries = 3

    for attempt in range(1, retries + 1):

        try:

            print(
                f"\nFetching RHEL data "
                f"(Attempt {attempt})..."
            )

            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 200:

                print(
                    "RHEL data fetched successfully"
                )

                return response.text

            else:

                print(
                    f"HTTP Error: "
                    f"{response.status_code}"
                )

        except Exception as e:

            print(
                f"Attempt {attempt} failed: {e}"
            )

        if attempt < retries:

            print(
                "Retrying in 5 seconds..."
            )

            time.sleep(5)

    return None


def get_rhel_releases():
    """
    Fetch latest 6 RHEL releases.
    """

    html = fetch_rhel_page()

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    rows = soup.find_all("tr")

    release_data = []

    for row in rows:

        columns = row.find_all("td")

        if len(columns) < 2:
            continue

        release_text = columns[0].get_text(
            strip=True
        )

        release_date = columns[1].get_text(
            strip=True
        )

        # Match:
        # RHEL 10.0
        # RHEL 9.6
        # RHEL 8.10

        match = re.search(
            r"RHEL\s+(\d+\.\d+)",
            release_text
        )

        if not match:
            continue

        version = match.group(1)

        # Ignore beta releases
        if "Beta" in release_text:
            continue

        # Ignore GA entries
        if "GA" in release_text:
            continue

        # Validate date
        try:

            parsed_date = datetime.strptime(
                release_date,
                "%Y-%m-%d"
            )

        except Exception:
            continue

        release_data.append({
            "version": f"RHEL {version}",
            "release_date": format_date(
                release_date
            ),
            "sort_date": parsed_date
        })

    # Remove duplicates
    unique_data = {}

    for item in release_data:

        unique_data[item["version"]] = item

    final_list = list(unique_data.values())

    # Sort by latest release date
    final_list.sort(
        key=lambda x: x["sort_date"],
        reverse=True
    )

    # Latest 5 versions
    latest_five = final_list[:5]

    # Remove internal key
    output = []

    for item in latest_five:

        output.append({
            "version": item["version"],
            "release_date": item["release_date"]
        })

    return output


if __name__ == "__main__":

    data = get_rhel_releases()

    print("\nLatest RHEL Releases:\n")

    for item in data:
        print(item)