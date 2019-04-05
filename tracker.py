#!/usr/bin/env python3
"""Checks the Zen website for status updates to broadband. Anything which has
not been previously reported, and are happening in the next 48 hours, will be
reported as per configuration.
"""

from datetime import datetime, date, timedelta
from lxml import html
import urllib.request


PREFIX = "01413"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'


def get_page(prefix=PREFIX):
    """Gets the HTML of the status page, given the prefix.
    """
    url = f"https://status.zen.co.uk/broadband/outages.aspx?number={prefix}"
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    return urllib.request.urlopen(request).read()


def parse_date(datestr):
    """Parse a date string in the Zen format, returning the date object.
    """
    return datetime.strptime(datestr, "%d/%m/%Y %H:%M")


def parse_page(page):
    """Parses some HTML, returning a dict of issues that are either current, or
    will occur in the next 48 hours.
    """
    # Current, planned, past issues
    issues = [[], [], []]
    tree = html.fromstring(page)
    today = date.today()
    time_gap = timedelta(days=2)
    grid_prefix = "ctl00_ctl00_ContentPlaceholderColumnTwo_PageContent_"
    gridname = grid_prefix + "pastOutagesGridView"
    for row in tree.xpath(f"//table[@id=\"{gridname}\"]//tbody//tr"):
        issue = {}
        issue['issue_type'] = row[0].text
        issue['reference'] = row[1].text_content()
        issue['start'] = parse_date(row[2].text)
        issue['end'] = parse_date(row[3].text)
        issue['codes'] = row[4].text
        if issue['start'].date() - today < time_gap and today - issue['end'].date() < time_gap:
            issues[2].append(issue)
    gridname = grid_prefix + "plannedOutagesGridView"
    for row in tree.xpath(f"//table[@id=\"{gridname}\"]//tbody//tr"):
        issue = {}
        issue['issue_type'] = row[0].text
        issue['reference'] = row[1].text_content()
        issue['start'] = parse_date(row[2].text)
        issue['end'] = parse_date(row[3].text)
        issue['codes'] = row[4].text
        if issue['start'].date() - today < time_gap and today - issue['end'].date() < time_gap:
            issues[1].append(issue)
    gridname = grid_prefix + "currentOutagesGridView"
    for row in tree.xpath(f"//table[@id=\"{gridname}\"]//tbody//tr"):
        issue = {}
        issue['issue_type'] = row[0].text
        issue['reference'] = row[1].text_content()
        issue['start'] = parse_date(row[2].text)
        issue['end'] = parse_date(row[3].text)
        issue['codes'] = row[4].text
        if issue['start'].date() - today < time_gap and today - issue['end'].date() < time_gap:
            issues[0].append(issue)
    return issues


def report(issues):
    """Report the given issues"""
    for issue in issues[0]:
        print(f"Outage current at {issue['start'].isoformat()}")
        message = f"Outage {issue['reference']} planned to start at "
        message += f"{issue['start'].isoformat()} and end at "
        message += f"{issue['end'].isoformat()}. Hopefully check "
        message += f"reference {issue['reference']} at "
        outage_id = issue['reference'][2:]
        message += f"https://status.zen.co.uk/broadband/maintenance-outage-details.aspx?reference={outage_id}"
    for issue in issues[1]:
        print(f"Outage planned at {issue['start'].isoformat()}")
        message = f"Outage {issue['reference']} planned to start at "
        message += f"{issue['start'].isoformat()} and end at "
        message += f"{issue['end'].isoformat()}. Hopefully check "
        message += f"reference {issue['reference']} at "
        outage_id = issue['reference'][2:]
        message += f"https://status.zen.co.uk/broadband/maintenance-outage-details.aspx?reference={outage_id}"
        print(message)
    for issue in issues[2]:
        print(f"Outage complete, ended at {issue['end'].isoformat()}")
        message = f"Outage {issue['reference']} planned to start at "
        message += f"{issue['start'].isoformat()} and end at "
        message += f"{issue['end'].isoformat()}. Hopefully check "
        message += f"reference {issue['reference']} at "
        outage_id = issue['reference'][2:]
        message += f"https://status.zen.co.uk/broadband/maintenance-outage-details.aspx?reference={outage_id}"
        print(message)


def main():
    """Do all the stuff."""
    page = get_page()
    issues = parse_page(page)
    report(issues)

if __name__ == "__main__":
    main()
