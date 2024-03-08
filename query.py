import json
from utils import *
from api import *
from threading import Thread
from queue import Queue

def search_query(data, query):
    result = []
    for item in data["data"]:
        if check_similarity(query, item):
            result.append(item)
    if result == []:
        return result
    first_item = result[0]["url_name"][:-3]
    for item in data["data"]:
        if item["url_name"].startswith(first_item) and item["url_name"][:-3] != first_item:
            result.append(item)
    return result


def add_price(url_name, item, q: Queue):
    result = first_order(url_name)
    result.update(item)
    q.put(result)


def search_price(data, query):
    result = search_query(data, query)
    print("Query done")
    q = Queue()
    t = []
    for i in result:
        tmp = Thread(target=add_price, args=(i["url_name"], i, q))
        tmp.start()
        t.append(tmp)
    result = []
    for i in t:
        i.join()
        result.append(q.get())
    return result


if __name__ == "__main__":
    print(first_order("arcane grace"))