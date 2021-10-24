def calculate(data, findall):
    def get_right_matches(lst: list) -> list:
        right_lst = []
        for elem in lst:
            elem = list(elem)

            for i in (0, -1):
                while elem[i] == '':
                    elem.pop(i)

            right_lst.append(elem)

        return right_lst

    r1 = r"([abc])([+-]?)=([abc])([+-]\d+)"
    r2 = r"([abc])([+-]?)=([abc])[^+-]"
    r3 = r"([abc])([+-]?)=([+-]?\d+)"

    matches = findall(f"{r1}|{r2}|{r3}")
    right_matches = get_right_matches(matches)

    for lst in right_matches:
        if len(lst) == 4:
            v1, s, v2, n = lst
        else:
            v1, s, v2 = lst
            n = 0

        comp1 = data.get(v2, 0) if v2.isalpha() else int(v2)
        if s:
            if s == '+':
                data[v1] += comp1 + int(n or 0)
            else:
                data[v1] -= comp1 + int(n or 0)
        else:
            data[v1] = comp1 + int(n or 0)

    return data
