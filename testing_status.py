import json


TESTED_FILE = "reports/tested_versions.json"


def load_tested_versions():
    """
    Load tested versions from JSON file
    """

    try:

        with open(TESTED_FILE, "r") as file:

            return json.load(file)

    except Exception as e:

        print(
            f"Error loading tested versions: {e}"
        )

        return {}


def check_testing_status(
    os_name,
    version,
    tested_versions
):
    """
    Check whether version is already included in testing
    """

    os_name = os_name.lower()

    tested_list = tested_versions.get(
        os_name,
        []
    )

    # Already included in testing
    if version in tested_list:

        return {
            "color": "black"
        }

    # New latest version
    return {
        "color": "red"
    }