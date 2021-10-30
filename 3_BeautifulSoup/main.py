import unittest
import re
import os

from bs4 import BeautifulSoup
from bfs import *


def parse(path_to_file):
    """
    Сбор статистики со странички из path_to_file, в виде списка из 4 элементов. где
        1 - количество картинок (img) с шириной (width) не меньше 200,
        2 - количество заголовков, первая буква текста внутри которых
        соответствует заглавной букве E, T или C,
        3 - длину максимальной последовательности ссылок, между которыми
        нет других тегов, открывающихся или закрывающихся,
        4 - количество невложенных списков <ol> и <ul>
    """

    # открытие странички - создание soup
    with open(path_to_file, mode="r", encoding="utf-8") as html_file:
        html_text = html_file.read()
    soup = BeautifulSoup(html_text, "lxml")

    # Количество картинок (img) с шириной (width) не меньше 200.
    imgs = 0
    img_objs = soup.find_all('img')
    for img in img_objs:
        if img.has_attr("width"):
            if int(img["width"]) >= 200:
                imgs += 1

    # Количество заголовков, первая буква текста внутри которых соответствует заглавной букве E, T или C.
    headers = len(re.findall(r"<h[1-5][^>]*.*?>[ETC].*?</h[1-5]>", html_text))

    # Длина максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
    links = re.findall('<[a-zA-Z]+|</[a-zA-Z]+>', html_text)
    linkslen = 0
    i = 0
    while i < len(links):
        curr_a = 0
        while links[i] == "<a":
            while links[i] != "</a>":
                i += 1
            i += 1
            curr_a += 1

        linkslen = curr_a if curr_a > linkslen else linkslen
        i += 1

    # Количество невложенных списков <ol> и <ul>
    lists = 0
    i = 0
    while i < len(links):
        if links[i] in ["<ol", "<ul"]:
            nested_lists = 1
            while nested_lists != 0:
                i += 1
                if links[i] in ["<ol", "<ul"]:
                    nested_lists += 1
                elif links[i] in ["</ol>", "</ul>"]:
                    nested_lists -= 1
            lists += 1
        i += 1

    return [imgs, headers, linkslen, lists]


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


if __name__ == '__main__':
    print(parse("wiki/Stone_Age"))
