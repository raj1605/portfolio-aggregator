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
            name = r.find("a").text
            percent = r.find_all("td")[4].text
            percent_number = float(percent.replace("%", ""))
            portfolio[name] = percent_number

    debt_table = soup.select_one("#portfolioDebtTable tbody")
    if debt_table is not None:
        rows = debt_table.find_all("tr")
        for r in rows:
            name = r.find("a").text
            percent = r.find_all("td")[6].text
            percent_number = float(percent.replace("%", ""))
            portfolio[name] = percent_number

    others_tables = soup.select_one(".portf_others tbody")
    if others_tables is not None:
        rows = others_tables.find_all("tr")
        for r in rows:
            name = r.find("a").text
            percent = r.find_all("td")[2].text
            percent_number = float(percent.replace("%", ""))
            portfolio[name] = percent_number

    return portfolio


# TODO:: write util
# convert this link
# https://www.moneycontrol.com/mutual-funds/nav/axis-bluechip-fund-direct-plan/MAA181
# to this
# https://www.moneycontrol.com/mutual-funds/axis-bluechip-fund-direct-plan/portfolio-holdings/MAA181


if __name__ == "__main__":
    urls = [
        'https://www.moneycontrol.com/mutual-funds/axis-bluechip-fund-direct-plan/portfolio-holdings/MAA181',
        'https://www.moneycontrol.com/mutual-funds/canara-robeco-equity-hybrid-fund-direct-plan/portfolio-holdings/MCA208'
    ]
    console_port = {}
    for url in urls:
        port = get_portfolio(url)
        for k, v in port.items():
            if k in console_port:
                console_port[k] = v + console_port[k]
            else:
                console_port[k] = v
    print(console_port)
