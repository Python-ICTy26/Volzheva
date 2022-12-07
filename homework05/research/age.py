import datetime
import statistics
import typing as tp
from vkapi import session, config
import time
import re

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    ages = []
    now_year = datetime.datetime.now().year
    friends = get_friends(user_id).items
    print(friends)
    for each in friends:
        got_info = False
        while not got_info:
            # resp = session.get(
            #     "users.get",
            #     user_id=each["id"],
            #     fields="bdate",
            #     access_token=config.VK_CONFIG["access_token"],
            #     v=config.VK_CONFIG["version"],
            # )
            resp = session.get(
                "users.get",
                v=config.VK_CONFIG["version"],
                access_token=config.VK_CONFIG["access_token"],
                user_ids=each,
                fields="bdate"
            )
            info_main = resp.json()
            if "error" in info_main:
                time.sleep(1)
                continue

            got_info = True

        info_personal = resp.json()["response"][0]
        if "bdate" in info_personal:
            b_date = info_personal["bdate"]
            if re.findall(r"\d[.]\d[.]\d", b_date):
                year_of_birth = int(b_date.split(".")[-1])
                ages.append(now_year - year_of_birth)
            print(info_personal["bdate"])

    return statistics.median(ages)


print(age_predict(322122))
