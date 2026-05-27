import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL = "https://repo.openeuler.org/"


def fetch_page(url):
    """
    Fetch page with retry logic.
    """

    retries = 3

    for attempt in range(1, retries + 1):

        try:

            print(
                f"\nFetching openEuler data "
                f"(Attempt {attempt})..."
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 200:

                print(
                    "openEuler data fetched successfully"
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


def format_date(date_obj):
    """
    Convert date format:
    2024-08-02 -> 8/2/24
    """

    return (
        f"{date_obj.month}/"
        f"{date_obj.day}/"
        f"{str(date_obj.year)[2:]}"
    )


def get_openeuler_releases():
    """
    Fetch latest 6 openEuler releases.
    """

    html = fetch_page(URL)

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

        if len(columns) < 3:
            continue

        # Version column
        link = columns[0].find("a")

        if not link:
            continue

        version_text = link.get_text(
            strip=True
        )

        # Remove trailing slash
        version_text = version_text.rstrip("/")

        # Ignore unwanted rows
        lower_text = version_text.lower()

        if (
            "bugfix" in lower_text
            or "everything" in lower_text
            or "experimental" in lower_text
            or "dailybuild" in lower_text
            or "preview" in lower_text
            or "test" in lower_text
            or "embedded" in lower_text
            or "64kb" in lower_text
        ):
            continue

        # Only valid openEuler versions
        if not version_text.startswith(
            "openEuler"
        ):
            continue

        # Date column
        date_text = columns[2].get_text(
            strip=True
        )

        # Example:
        # 2024-Aug-02 10:18

        try:

            parsed_date = datetime.strptime(
                date_text,
                "%Y-%b-%d %H:%M"
            )

        except Exception:
            continue

        release_data.append({
            "version": version_text,
            "release_date": format_date(
                parsed_date
            ),
            "sort_date": parsed_date
        })

    # Remove duplicates
    unique_data = {}

    for item in release_data:

        unique_data[
            item["version"]
        ] = item

    final_list = list(
        unique_data.values()
    )

    # Sort latest first
    final_list.sort(
        key=lambda x: x["sort_date"],
        reverse=True
    )

    # Latest 5 versions
    latest_five = final_list[:5]

    # Final output
    output = []

    for item in latest_five:

        output.append({
            "version": item["version"],
            "release_date": item["release_date"]
        })

    return output


if __name__ == "__main__":

    data = get_openeuler_releases()

    print(
        "\nLatest openEuler Releases:\n"
    )

    if not data:

        print("No data found")

    else:

        for item in data:

            print(item)