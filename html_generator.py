from datetime import datetime


def generate_html(all_data):

    generated_time = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )

    html = f"""

    <html>

    <body
        style="
            font-family: Arial, Helvetica, sans-serif;
            font-size: 14px;
            color: #333333;
            background-color: #ffffff;
            line-height: 1.5;
        "
    >

    <br>

    <p>
        Hello Team,
    </p>

    <p>
        Good Morning!
    </p>

    <p>
        Please find below the latest Linux OS
        release versions and release dates.
    </p>

        <p
        style="
            font-size:12px;
            color:#666666;
            margin-top:4px;
        "
    >
        <b>Note:</b>
        Versions highlighted in
        <span style="color:red;">
            red
        </span>
        indicate newly released versions
        that are not yet included in testing.
    </p>

    <p>
        Report Generated:
        <b>{generated_time}</b>
    </p>

    <br>

    <table
        border="1"
        cellspacing="0"
        cellpadding="10"
        style="
            border-collapse: collapse;
            width: 88%;
            border: 1px solid #d6d6d6;
        "
    >

        <tr
            style="
                background-color: #2f2f2f;
                color: white;
            "
        >

            <th
                style="
                    text-align:left;
                "
            >
                Version
            </th>

            <th
                style="
                    text-align:left;
                "
            >
                Release Date
            </th>

            <th
                style="
                    text-align:left;
                "
            >
                Comments
            </th>

        </tr>

    """

    for item in all_data:

        # ======================================
        # Section Header
        # ======================================

        if item["color"] == "section":

            html += f"""

            <tr
                style="
                    background-color:#eeeeee;
                "
            >

                <td
                    colspan="3"
                    style="
                        font-weight:bold;
                        font-size:15px;
                        color:#555555;
                    "
                >

                    {item['version']}

                </td>

            </tr>

            """

            continue

        # ======================================
        # Version Color
        # ======================================

        text_color = (
            "red"
            if item["color"] == "red"
            else "#222222"
        )

        html += f"""

        <tr
            style="
                background-color:#ffffff;
            "
        >

            <td
                style="
                    color:{text_color};
                    font-weight:bold;
                "
            >

                {item['version']}

            </td>

            <td
                style="
                    color:#333333;
                "
            >

                {item['release_date']}

            </td>

            <td
                style="
                    color:#333333;
                "
            >

                {item['comments']}

            </td>

        </tr>

        """

    html += """

    </table>

    <br><br>

    <h3
        style="
            color:#555555;
        "
    >
        Reference Links
    </h3>

    <ul
        style="
            line-height: 1.8;
        "
    >

        <li>
            Ubuntu:
            <a href="https://releases.ubuntu.com/">
                https://releases.ubuntu.com/
            </a>
        </li>

        <li>
            AlmaLinux:
            <a href="https://wiki.almalinux.org/release-notes/">
                https://wiki.almalinux.org/release-notes/
            </a>
        </li>

        <li>
            RHEL:
            <a href="https://access.redhat.com/articles/3078">
                https://access.redhat.com/articles/3078
            </a>
        </li>

        <li>
            Rocky Linux:
            <a href="https://en.wikipedia.org/wiki/Rocky_Linux">
                https://en.wikipedia.org/wiki/Rocky_Linux
            </a>
        </li>

        <li>
            SUSE:
            <a href="https://en.wikipedia.org/wiki/SUSE_Linux_Enterprise">
                https://en.wikipedia.org/wiki/SUSE_Linux_Enterprise
            </a>
        </li>

        <li>
            OpenEuler:
            <a href="https://repo.openeuler.org/">
                https://repo.openeuler.org/
            </a>
        </li>

        <li>
            OpenAnolis:
            <a href="https://mirrors.openanolis.cn/anolis/">
                https://mirrors.openanolis.cn/anolis/
            </a>
        </li>

    </ul>

    <br>

    <p>
        Regards,
        <br>
        Vidyashree
    </p>

    </body>

    </html>

    """

    return html