import os

from fetchers.ubuntu import get_ubuntu_releases
from fetchers.almalinux import fetch_almalinux_releases
from fetchers.rhel import get_rhel_releases
from fetchers.rocky import get_rocky_releases
from fetchers.suse import get_suse_releases
from fetchers.openeuler import get_openeuler_releases
from fetchers.openanolis import get_anolis_releases

from utils.html_generator import generate_html
from utils.mailer import send_mail

from utils.testing_status import (
    load_tested_versions,
    check_testing_status
)

from utils.logger import logger


# ==========================================
# PROCESS OS DATA
# ==========================================

def process_os_data(
    display_name,
    lookup_name,
    data,
    tested_versions,
    all_data
):

    logger.info(
        f"Processing {display_name} data"
    )

    # ======================================
    # Section Header
    # ======================================

    all_data.append({

        "version":
        f"{display_name} Latest Releases",

        "release_date": "",

        "comments": "",

        "color": "section"
    })

    # ======================================
    # Actual Versions
    # ======================================

    for item in data:

        status = check_testing_status(
            lookup_name.lower(),
            item["version"],
            tested_versions
        )

        # ==================================
        # Comment Logic
        # ==================================

        if status["color"] == "red":

            comment = (
                "New Version - "
                "Testing Required"
            )

        else:

            comment = (
                "Included in Testing"
            )

        all_data.append({

            "version":
            item["version"],

            "release_date":
            item["release_date"],

            "comments":
            comment,

            "color":
            status["color"]
        })


# ==========================================
# MAIN
# ==========================================

def main():

    print("\nCollecting Linux release data...\n")

    logger.info(
        "Collecting Linux release data"
    )

    # ======================================
    # Load Tested Versions
    # ======================================

    tested_versions = load_tested_versions()

    logger.info(
        "Loaded tested versions JSON"
    )

    # ======================================
    # Fetch Data
    # ======================================

    logger.info("Fetching Ubuntu data")

    ubuntu_data = get_ubuntu_releases()

    logger.info("Fetching AlmaLinux data")

    alma_data = fetch_almalinux_releases()

    logger.info("Fetching RHEL data")

    rhel_data = get_rhel_releases()

    logger.info("Fetching Rocky Linux data")

    rocky_data = get_rocky_releases()

    logger.info("Fetching SUSE data")

    suse_data = get_suse_releases()

    logger.info("Fetching openEuler data")

    openeuler_data = get_openeuler_releases()

    logger.info("Fetching OpenAnolis data")

    openanolis_data = get_anolis_releases()

    # ======================================
    # Final Combined Data
    # ======================================

    all_data = []

    # ======================================
    # Ubuntu
    # ======================================

    process_os_data(
        "Ubuntu",
        "ubuntu",
        ubuntu_data,
        tested_versions,
        all_data
    )

    # ======================================
    # AlmaLinux
    # ======================================

    process_os_data(
        "AlmaLinux",
        "almalinux",
        alma_data,
        tested_versions,
        all_data
    )

    # ======================================
    # RHEL
    # ======================================

    process_os_data(
        "RHEL",
        "rhel",
        rhel_data,
        tested_versions,
        all_data
    )

    # ======================================
    # Rocky Linux
    # ======================================

    process_os_data(
        "Rocky Linux",
        "rocky linux",
        rocky_data,
        tested_versions,
        all_data
    )

    # ======================================
    # SUSE
    # ======================================

    process_os_data(
        "SUSE",
        "suse",
        suse_data,
        tested_versions,
        all_data
    )

    # ======================================
    # openEuler
    # ======================================

    process_os_data(
        "openEuler",
        "openeuler",
        openeuler_data,
        tested_versions,
        all_data
    )

    # ======================================
    # OpenAnolis
    # ======================================

    process_os_data(
        "OpenAnolis",
        "openanolis",
        openanolis_data,
        tested_versions,
        all_data
    )

    # ======================================
    # Generate HTML
    # ======================================

    print("\nGenerating HTML report...\n")

    logger.info(
        "Generating HTML report"
    )

    html_content = generate_html(
        all_data
    )

    # ======================================
    # Send Mail
    # ======================================

    print("Sending email...")

    logger.info(
        "Sending email"
    )

    send_mail(html_content)

    logger.info(
        "Mail sent successfully"
    )

    print(
        "\nProcess completed successfully"
    )

    logger.info(
        "Process completed successfully"
    )


# ==========================================
# ENTRY
# ==========================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        logger.error(
            f"Main execution failed: {e}"
        )

        print(
            f"\nError occurred: {e}"
        )