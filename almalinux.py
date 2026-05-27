import requests

from bs4 import BeautifulSoup

from datetime import datetime

import time


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


URL = "https://wiki.almalinux.org/release-notes/"


def format_date(date_obj):

    return (
        f"{date_obj.month}/"
        f"{date_obj.day}/"
        f"{date_obj.year}"
    )


def fetch_almalinux_releases():

    retries = 3

    for attempt in range(retries):

        try:

            print(
                f"\nFetching AlmaLinux data "
                f"(Attempt {attempt + 1})..."
            )

            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code != 200:

                print(
                    f"Failed to fetch page: "
                    f"{response.status_code}"
                )

                time.sleep(3)

                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            tables = soup.find_all("table")

            release_data = []

            # =====================================
            # Parse all release tables dynamically
            # =====================================

            for table in tables:

                rows = table.find_all("tr")

                for row in rows[1:]:

                    cols = row.find_all("td")

                    if len(cols) < 6:
                        continue

                    release = cols[0].get_text(
                        strip=True
                    )

                    release_date = cols[3].get_text(
                        strip=True
                    )

                    architectures = cols[5].get_text(
                        strip=True
                    )

                    # ==========================
                    # Skip Beta Releases
                    # ==========================

                    if "Beta" in release:
                        continue

                    # ==========================
                    # Only x86_64 Supported
                    # ==========================

                    if "x86_64" not in architectures:
                        continue

                    # ==========================
                    # Release date required
                    # ==========================

                    if not release_date:
                        continue

                    # ==========================
                    # Parse release date
                    # Example:
                    # 27 May 2025
                    # ==========================

                    try:

                        parsed_date = datetime.strptime(
                            release_date,
                            "%d %b %Y"
                        )

                    except Exception:
                        continue

                    release_data.append({

                        "version":
                        f"Alma Linux {release}",

                        "release_date":
                        format_date(parsed_date),

                        "raw_date":
                        parsed_date
                    })

            # =====================================
            # Remove duplicate versions
            # =====================================

            unique_versions = {}

            for item in release_data:

                unique_versions[
                    item["version"]
                ] = item

            final_data = list(
                unique_versions.values()
            )

            # =====================================
            # Sort using release date
            # Latest first
            # =====================================

            final_data.sort(
                key=lambda x: x["raw_date"],
                reverse=True
            )

            # =====================================
            # Take latest 5 releases
            # =====================================

            latest_five = final_data[:5]

            # =====================================
            # Remove raw_date before output
            # =====================================

            output = []

            for item in latest_five:

                output.append({

                    "version":
                    item["version"],

                    "release_date":
                    item["release_date"]

                })

            print(
                "AlmaLinux data fetched successfully"
            )

            return output

        except Exception as e:

            print(
                f"Attempt {attempt + 1} failed: {e}"
            )

            # Wait before retry
            time.sleep(5)

    print(
        "Failed after multiple retries"
    )

    return []


if __name__ == "__main__":

    data = fetch_almalinux_releases()

    print("\nLatest AlmaLinux Releases:\n")

    for item in data:

        print(item)