import json
import requests

from datetime import datetime

url = "https://api.warframe.market/v1/"

def get_data():
    r = requests.get(url + "items", headers={"language": "zh-hant"})
    data = r.json()["payload"]["items"]
    for i in data:
        del i["thumb"]
        del i["id"]

    data = {"time": int(datetime.now().timestamp()), "data": data}

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data


def get_order(url_name):
    r = requests.get(url + f"items/{url_name}/orders")
    data = list(r.json()["payload"]["orders"])
    for i in list(data):
        if i["user"]["status"] != "ingame" or i["order_type"] != "sell":
            data.pop(data.index(i))

    for i in data:
        del i["region"]
        del i["visible"]
        del i["id"]
        del i["order_type"]
        del i["creation_date"]
        del i["user"]["avatar"]
        del i["user"]["id"]
        del i["user"]["region"]
        del i["user"]["status"]

    data = sorted(data, key=lambda i:i["platinum"])
    return data


def first_order(url_name):
    return get_order(url_name)[0]


if __name__ == "__main__":
    print(first_order("arcane grace"))