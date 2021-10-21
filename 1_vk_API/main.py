import requests
import numpy as np
import matplotlib.pyplot as plt


from collections import Counter
from datetime import date, datetime as dt
from dateutil import relativedelta as rdelta


"""
    This project is first work in Coursera's course. 
    This is VK API for calculating number of user's friends.

    We get user_id and return list like 
        [(age1, count1), (age2, count2), ...]  sorting by age. 
"""

VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": "",                                                               # insert your access_token
    "version": "5.131",
}


# get user_id if we have shortname
def get_user_id(uid) -> int:
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    query = f"{domain}/users.get?access_token={access_token}&user_ids={uid}&v={v}"
    response = requests.get(query)

    return response.json()["response"][0]["id"]


# get information about user's friends
def get_friends(uid: int, fields: str = "bdate") -> list[dict]:
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    query = f"{domain}/friends.get?access_token={access_token}&user_id={uid}&fields={fields}&v={v}"
    response = requests.get(query)

    list_of_friends = response.json()["response"]["items"]
    return list_of_friends


# calculate number of friends without bdate or correct bdate and create new ages' list
def friends_small_correct_info(friends: list[dict]) -> list:
    correct_ages = []
    for friend_info in friends:
        if "bdate" in friend_info.keys():
            if Counter(friend_info["bdate"])["."] == 2:
                day, month, year = tuple(map(int, friend_info["bdate"].split(".")))
                bdate = date(year, month, day)
                correct_ages.append(bdate)

    return correct_ages


# calculate number of friends for a certain ages
def calc_age(bdates: list[date]) -> list:
    now = date.today()

    diff_years = []
    for bdate in bdates:
        age = rdelta.relativedelta(now, bdate).years
        diff_years.append(age)

    counter_ages = Counter(diff_years)
    counter_ages_sorted = sorted(counter_ages.items(), key=lambda pair: pair[1], reverse=True)
    return counter_ages_sorted


# draw a graph of the distribution of the age of friends
def draw_distribution(distribution: list) -> None:
    x = []
    y = []
    for pair in distribution:
        x.append(pair[0])
        y.append(pair[1])

    plt.title("Distribution count of friends by age")
    plt.xlabel("age")
    plt.ylabel("count")

    plt.bar(x, y)
    plt.show()


if __name__ == "__main__":
    # user_ids = "danya_milokhin"                                                     # testing

    user_ids = input("Please, give me your interested user id: ")                     # shortname or id
    if not user_ids.isdigit():                                                        # if we have shortname
        user_id = get_user_id(user_ids)
    else:
        user_id = user_ids

    friends_info = get_friends(user_id)                                               # get information about friends
    friends_bdates = friends_small_correct_info(friends_info)                         # get corrects ages of his friends
    friends_info.clear()                                                              # freeing up excess memory

    result = calc_age(friends_bdates)                                                 # calculate distribution
    draw_distribution(result)                                                         # draw distribution














