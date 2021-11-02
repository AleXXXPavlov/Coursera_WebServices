from bs4 import BeautifulSoup


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
    soup_body = soup.find("div", id="bodyContent")

    # Количество картинок (img) с шириной (width) не меньше 200.
    imgs = 0
    img_objs = soup_body.find_all('img')
    for img in img_objs:
        if img.has_attr("width"):
            if int(img["width"]) >= 200:
                imgs += 1

    # Количество заголовков, первая буква текста внутри которых соответствует заглавной букве E, T или C.
    headers = []
    for h in ["h1", "h2", "h3", "h4", "h5"]:
        elems = soup_body.find_all(h)
        for elem in elems:
            if elem.text[0] in ["C", "E", "T"]:
                headers.append(elem)

    headers = len(headers)

    # Длина максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
    linkslen = 0
    links = soup_body.find_all("a")

    i = 0
    while i < len(links):
        curr_len = 1
        while links[i].find_next_sibling():
            if links[i].find_next_sibling().name == "a":
                i += 1
                curr_len += 1
            else:
                break

        linkslen = curr_len if linkslen < curr_len else linkslen
        i += 1

    # Количество невложенных списков <ol> и <ul>
    lists = 0
    tag_lists = ["ul", "ol"]
    for tag_list in tag_lists:
        lsts = soup_body.find_all(tag_list)
        for lst in lsts:
            parents = set([tag.name for tag in lst.parents])
            if not set(tag_lists) & parents:
                lists += 1

    return [imgs, headers, linkslen, lists]
