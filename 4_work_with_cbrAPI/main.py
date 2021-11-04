from bs4 import BeautifulSoup
from decimal import Decimal


def get_rate(valuta: str, soup) -> Decimal:
    """
        Получение курса валюты из soup с учетом номинала
    """

    point = lambda s: s.replace(',', '.')
    value = point(soup.find('CharCode', text=valuta).find_next_sibling('Value').string)
    nominal = point(soup.find('CharCode', text=valuta).find_next_sibling('Nominal').string)

    return Decimal(value) / Decimal(nominal)


def convert(amount, cur_from, cur_to, date, requests):
    """
        Конвертация валюты cur_from в cur_to, используя API ЦБР, в количестве amount
    """

    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp?date_req=")
    soup = BeautifulSoup(response.content, "xml")

    value_from = get_rate(cur_from, soup)
    value_to = get_rate(cur_to, soup)

    return (Decimal(amount) * value_from / value_to).quantize(Decimal("0.0001"))

