import os

from utils import *
from api import *


async def load_data():
    data = {}
    if os.path.exists("data/data.json"):
        with open("data/data.json", "r") as f:
            data = json.load(f)
    if data == {} or datetime.now().timestamp() > data["time"] + 60 * 60 * 6:
        data = await get_data()
        with open("data/data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Updated in {int_to_time(data['time'])}")
    else:
        print(f"Used data in {int_to_time(data['time'])}")
    return data


async def search_query(data, query, content="data"):
    result = []
    for item in data[content]:
        if check_similarity(query, item):
            result.append(item)
    if not result or content == "riven":
        return result
    first_item = result[0]["url_name"][:-3]
    result = [result[0]]
    for item in data[content]:
        if item["url_name"].startswith(first_item) and item["url_name"][:-3] != first_item:
            result.append(item)
    return result


async def search_set(data, prime):
    result = []
    for item in data["data"]:
        if item["url_name"].endswith("_set") and not prime or item["url_name"].endswith("prime_set"):
            result.append(item)
    return result


async def search_price(data, query, prime=False):
    if query == "all":
        result = await search_set(data, prime)
    else:
        result = await search_query(data, query)
    print("Query done")

    return await get_prices(result)


async def search_riven_price(data, query, amount=1):
    result = await search_query(data, query, "riven")
    print("Query done")
    return await get_prices(result, amount, True)


if __name__ == "__main__":
    async def main():
        import time
        from formatting import format_query
        data = await load_data()
        s = time.time()
        print(format_query(await search_price(data, "khora prime")))
        print("done" + str(time.time() - s))
        s = time.time()
        print(format_query(await search_riven_price(data, "ceramic dagger", 3), riven=True))
        print("done" + str(time.time() - s))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

