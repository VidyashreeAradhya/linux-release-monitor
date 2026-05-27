import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL = "https://en.wikipedia.org/wiki/Rocky_Linux"


def format_date(date_string):
    """
    Convert:
    2025-05-31 -> 5/31/2025
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


def fetch_rocky_page():
    """
    Fetch Rocky Linux page
    with retry logic.
    """

    retries = 3

    for attempt in range(1, retries + 1):

        try:

            print(
                f"\nFetching Rocky Linux data "
                f"(Attempt {attempt})..."
            )

            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 200:

                print(
                    "Rocky Linux data fetched successfully"
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


def get_rocky_releases():
    """
    Fetch latest 5 Rocky Linux releases.
    """

    html = fetch_rocky_page()

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    tables = soup.find_all("table")

    release_data = []

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            columns = row.find_all(["td", "th"])

            if len(columns) < 2:
                continue

            row_text = row.get_text(
                " ",
                strip=True
            )

            # Match versions:
            # 9.7
            # 9.6
            # 8.10
            version_match = re.search(
                r"\b(\d+\.\d+)\b",
                row_text
            )

            if not version_match:
                continue

            version = version_match.group(1)

            # Ignore beta / rc
            lower_text = row_text.lower()

            if (
                "beta" in lower_text
                or "rc" in lower_text
                or "release candidate" in lower_text
            ):
                continue

            # Find date
            date_match = re.search(
                r"(\d{4}-\d{2}-\d{2})",
                row_text
            )

            if not date_match:
                continue

            release_date = date_match.group(1)

            try:

                parsed_date = datetime.strptime(
                    release_date,
                    "%Y-%m-%d"
                )

            except Exception:
                continue

            release_data.append({
                "version": (
                    f"Rocky Linux {version}"
                ),
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

    # Sort latest first
    final_list.sort(
        key=lambda x: x["sort_date"],
        reverse=True
    )

    # Latest 6 versions
    latest_six = final_list[:5]

    # Final output
    output = []

    for item in latest_six:

        output.append({
            "version": item["version"],
            "release_date": item["release_date"]
        })

    return output


if __name__ == "__main__":

    data = get_rocky_releases()

    print("\nLatest Rocky Linux Releases:\n")

    for item in data:
        print(item)