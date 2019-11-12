import csv
import operator
from typing import List

import requests
from bs4 import BeautifulSoup


def get_portfolio(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    portfolio = {}

    equity_table = soup.select_one('#equityCompleteHoldingTable tbody')
    if equity_table is not None:
        rows = equity_table.find_all('tr')
        for r in rows:
            name = r.find("a").text.strip()
            percent = r.find_all("td")[4].text.strip()
            percent_number = float(percent.replace("%", ""))
            if name in portfolio:
                portfolio[name] = portfolio[name] + percent_number
            else:
                portfolio[name] = percent_number

    debt_table = soup.select_one("#portfolioDebtTable tbody")
    if debt_table is not None:
        rows = debt_table.find_all("tr")
        for r in rows:
            name = r.find("a").text.strip()
            percent = r.find_all("td")[6].text.strip()
            percent_number = float(percent.replace("%", ""))
            if name in portfolio:
                portfolio[name] = portfolio[name] + percent_number
            else:
                portfolio[name] = percent_number

    others_tables = soup.select_one(".portf_others tbody")
    if others_tables is not None:
        rows = others_tables.find_all("tr")
        for r in rows:
            name = r.find("a").text.strip()
            percent = r.find_all("td")[2].text.strip()
            percent_number = float(percent.replace("%", ""))
            if name in portfolio:
                portfolio[name] = portfolio[name] + percent_number
            else:
                portfolio[name] = percent_number

    return portfolio


def sort_portfolio(port: {}):
    return sorted(port.items(), key=operator.itemgetter(1), reverse=True)


def write_to_csv(prefix: str, headers, data_port: {}):
    csv_file = prefix + ".csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for d in data_port:
                writer.writerow(d)
    except IOError:
        print("I/O error")


# TODO:: improve this
# converts this link
# https://www.moneycontrol.com/mutual-funds/nav/axis-bluechip-fund-direct-plan/MAA181
# to this
# https://www.moneycontrol.com/mutual-funds/axis-bluechip-fund-direct-plan/portfolio-holdings/MAA181
def get_port_url(u: str):
    data = u.split("/nav/", 2)
    new_data = data[-1].split("/")
    return "https://www.moneycontrol.com/mutual-funds/" + new_data[0] + "/portfolio-holdings/" + new_data[1]


def consolidate_portfolio(urls: List[str]):
    console_port = {}
    for url in urls:
        port_url = get_port_url(url)
        port = get_portfolio(port_url)
        sum = 0
        for k, v in port.items():
            sum += v
            if k in console_port:
                console_port[k] = v + console_port[k]
            else:
                console_port[k] = v
        # sum must be 100
    sorted = sort_portfolio(console_port)

    data = []
    count = len(urls)
    for k, v in sorted:
        data.append([k, v, v / count])
    return data

if __name__ == "__main__":
    urls = [
        'https://www.moneycontrol.com/mutual-funds/nav/mirae-asset-tax-saver-fund-direct-plan/MMA150',
        'https://www.moneycontrol.com/mutual-funds/nav/tata-india-tax-savings-fund-direct-plan-growth/MTA1114',
        'https://www.moneycontrol.com/mutual-funds/nav/axis-long-term-equity-fund-direct-plan-growth/MAA192',
        'https://www.moneycontrol.com/mutual-funds/nav/l-t-emerging-businesses-fund-direct-plan/MCC492',
        'https://www.moneycontrol.com/mutual-funds/nav/sbi-magnum-multicap-fund-direct-plan-growth/MSB503',
        'https://www.moneycontrol.com/mutual-funds/nav/dsp-govt-sec-fund-direct-plan-growth/MDS622',
        'https://www.moneycontrol.com/mutual-funds/nav/axis-bluechip-fund-direct-plan-growth/MAA181',
        'https://www.moneycontrol.com/mutual-funds/nav/l-t-ultra-short-term-fund-direct-plan-growth/MCC247'
    ]

    consolidated = consolidate_portfolio(urls)
    headers = ['Stock Name', 'Total %', 'Avg %']
    write_to_csv("consolidated", headers, consolidated)
