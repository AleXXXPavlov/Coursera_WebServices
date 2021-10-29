from bs4 import BeautifulSoup
import unittest
import re


def parse(path_to_file):
    with open(path_to_file, mode="r", encoding="utf-8") as html_file:
        html_text = html_file.read()
    soup = BeautifulSoup(html_text, "lxml")

    # # Количество картинок (img) с шириной (width) не меньше 200.
    imgs = 0
    img_objs = soup.find_all('img')
    for img in img_objs:
        if img.has_attr("width"):
            if int(img["width"]) >= 200:
                imgs += 1

    # Количество заголовков, первая буква текста внутри которых соответствует заглавной букве E, T или C.
    header_tags = ['h1', 'h2', 'h3', 'h4', 'h5']
    headers = len([h for h in soup.find_all(header_tags, text=re.compile(r"E.+|T.+|C.+"))])

    # Длину максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
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


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]))

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    # unittest.main()
    parse('wiki/Python_(programming_language)')
