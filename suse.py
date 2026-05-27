import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# ── Constants ────────────────────────────────────────────────────────────────

WIKI_URL = (
    "https://en.wikipedia.org/wiki/"
    "SUSE_Linux_Enterprise"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

TOP_N = 5


# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch_page(url):
    """
    Fetch page with retry + timeout logic.
    """

    retries = 3

    for attempt in range(1, retries + 1):

        try:

            print(
                f"\nFetching SUSE data "
                f"(Attempt {attempt})..."
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 200:

                print(
                    "SUSE data fetched successfully"
                )

                return BeautifulSoup(
                    response.text,
                    "html.parser"
                )

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


def find_version_table(soup):
    """
    Find the SECOND table:
    'Version history'
    """

    tables = soup.find_all(
        "table",
        class_="wikitable"
    )

    if len(tables) < 2:

        print(
            "Target table not found"
        )

        return None

    # Second table
    return tables[1]


def clean_text(element):
    """
    Remove citation references.
    """

    for sup in element.find_all("sup"):
        sup.decompose()

    return element.get_text(
        separator=" ",
        strip=True
    )


def parse_date(date_str):
    """
    Parse:
    24 June 2025
    4 November 2025
    """

    date_str = date_str.strip()

    formats = [
        "%d %B %Y",
        "%B %Y"
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                date_str,
                fmt
            )

        except Exception:
            continue

    # Year only
    year_match = re.match(
        r"^(\d{4})$",
        date_str
    )

    if year_match:

        return datetime(
            int(year_match.group(1)),
            1,
            1
        )

    return None


def format_version_label(
    major,
    revision
):
    """
    Build version label.
    """

    revision_lower = revision.lower()

    if (
        revision_lower == "initial release"
    ):

        return f"SLES {major}.0"

    else:

        return (
            f"SUSE Linux "
            f"{major} "
            f"{revision}"
        )


def format_date_output(dt):
    """
    Convert:
    2025-11-04
    ->
    11/4/25
    """

    return (
        f"{dt.month}/"
        f"{dt.day}/"
        f"{str(dt.year)[2:]}"
    )


def parse_version_table(table):

    release_data = []

    current_major = None

    rows = table.find_all("tr")

    for row in rows:

        cells = row.find_all(
            ["td", "th"]
        )

        if not cells:
            continue

        first_cell = cells[0]

        # Skip header row
        if (
            first_cell.name == "th"
            and (
                "Version"
                in first_cell.get_text()
                or "Revision"
                in first_cell.get_text()
            )
        ):
            continue

        # Major version row
        if first_cell.name == "th":

            current_major = clean_text(
                first_cell
            )

            remaining = cells[1:]

            if len(remaining) < 2:
                continue

            revision = clean_text(
                remaining[0]
            )

            date_str = clean_text(
                remaining[1]
            )

        # Sub rows
        else:

            if not current_major:
                continue

            if len(cells) < 2:
                continue

            revision = clean_text(
                cells[0]
            )

            date_str = clean_text(
                cells[1]
            )

        parsed_date = parse_date(
            date_str
        )

        if not parsed_date:
            continue

        version_label = (
            format_version_label(
                current_major,
                revision
            )
        )

        release_data.append({
            "version": version_label,
            "release_date": (
                format_date_output(
                    parsed_date
                )
            ),
            "sort_date": parsed_date
        })

    return release_data


def get_suse_releases():

    soup = fetch_page(WIKI_URL)

    if not soup:
        return []

    table = find_version_table(soup)

    if not table:
        return []

    release_data = parse_version_table(
        table
    )

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

    # Latest 6
    latest_six = final_list[:TOP_N]

    output = []

    for item in latest_six:

        output.append({
            "version": item["version"],
            "release_date": (
                item["release_date"]
            )
        })

    return output


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    data = get_suse_releases()

    print(
        "\nLatest SUSE Releases:\n"
    )

    if not data:

        print("No data found")

    else:

        for item in data:
            print(item)