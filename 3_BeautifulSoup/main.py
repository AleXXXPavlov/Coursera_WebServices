import re
import os

from bfs import *
from parse import parse


def get_page_links(path, page) -> list:
    """
    Возвращает список страниц, по которым есть переход в переданной странице,
    а также только те, что сохранены в директории /wiki/.
    """

    with open(os.path.join(path, page), mode="r", encoding="utf-8") as file:
        links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())

    right_links = list()
    for link in list(set(links)):
        if os.path.isfile(os.path.join(path, link)):
            right_links.append(link)

    return right_links


def build_bridge(path, start_page, end_page):
    """
    Возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список.
    """

    graph_pages = dict()                            # граф, где вершина - страница википедии

    all_pages = os.listdir(path)
    for page in all_pages:
        graph_pages[page] = get_page_links(path, page)

    _, parents = bfs(graph_pages, start_page, end_page)
    parents_path = get_parent_path(parents, start_page, end_page)

    return parents_path


def get_statistics(path, start_page, end_page):
    """
    Собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы.
    """

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)

    # сбор статистики
    statistics = dict()
    for page in pages:
        statistics[page] = parse(os.path.join(path, page))

    return statistics


