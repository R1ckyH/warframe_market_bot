import aiohttp
import asyncio
import json

from aiohttp_client_rate_limiter.ClientSession import RateLimitedClientSession
from datetime import datetime

url = "https://api.warframe.market/"


async def get_item_data(session: RateLimitedClientSession):
    async with session.get("/v1/items", headers={"language": "zh-hant"}) as r:
        data = (await r.json())["payload"]["items"]
        for i in data:
            del i["thumb"]
            del i["id"]

        data = {"time": int(datetime.now().timestamp()), "data": data}
    print("queried item data")
    return data


async def get_riven_data(session: RateLimitedClientSession):
    async with session.get("/v1/riven/items", headers={"language": "zh-hant"}) as r:
        data = (await r.json())["payload"]["items"]
        for i in data:
            del i["thumb"]
            del i["id"]
            del i["icon"]
            del i["mastery_level"]
            if "icon_format" in i.keys():
                del i["icon_format"]

        data = {"time": int(datetime.now().timestamp()), "riven": data}
    print("queried riven data")
    return data


async def get_data():
    async with RateLimitedClientSession(10, 5, 1, base_url=url) as session:
        datas = await asyncio.gather(get_item_data(session), get_riven_data(session))
        data = {}
        for i in datas:
            data.update(i)
    return data


async def get_order(url_name, session):
    async with session.get(f"/v1/items/{url_name}/orders") as r:
        try:
            data = (await r.json())["payload"]["orders"]
        except KeyError:
            print(await r.text(), r.url)
            return []
        except aiohttp.client_exceptions.ContentTypeError:
            print(r.content)
            return []
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

        data = sorted(data, key=lambda i: i["platinum"])
    return data


async def get_riven_order(url_name, session):
    params = {"type": "riven",
              "buyout_policy": "direct",
              "weapon_url_name": url_name,
              "sort_by": "price_asc"
              }
    async with session.get(f"/v1/auctions/search", params=params) as r:
        try:
            data = (await r.json())["payload"]["auctions"]
        except KeyError:
            print(await r.text(), r.url)
            return []
        except aiohttp.client_exceptions.ContentTypeError:
            print(r.content)
            return []
        for i in list(data):
            if i["owner"]["status"] != "ingame":
                data.pop(data.index(i))

        for i in data:
            del i["note"]
            del i["visible"]
            del i["id"]
            del i["created"]
            del i["closed"]
            del i["note_raw"]
            del i["private"]
            del i["minimal_reputation"]
            del i["starting_price"]
            del i["top_bid"]
            del i["winner"]
            del i["is_marked_for"]
            del i["marked_operation_at"]
            del i["is_direct_sell"]
            del i["owner"]["avatar"]
            del i["owner"]["id"]
            del i["owner"]["region"]
            del i["owner"]["status"]
            del i["item"]["mastery_level"]
        with open("./data/test.json", "w") as f:
            json.dump(data, f, indent=4)

        data = sorted(data, key=lambda i: i["buyout_price"])
    return data


async def first_order(url_name, item, session, amount=1, riven=False):
    if riven:
        data = await get_riven_order(url_name, session)
    else:
        data = await get_order(url_name, session)
    if len(data) <= 0:
        return
    if amount == 1:
        result = data[0]
        result.update(item)
    else:
        result = []
        for i in range(amount):
            now = data[i]
            now.update(item)
            result.append(now)

    return result


async def get_prices(result, amount=1, riven=False):
    tasks = []
    async with RateLimitedClientSession(10, 3, 1, base_url=url) as session:
        for i in result:
            tasks.append(first_order(i["url_name"], i, session, amount, riven))
        result = await asyncio.gather(*tasks)
    if amount != 1:
        result = result[0]
    while None in result:
        result.pop(result.index(None))
    return result


if __name__ == "__main__":
    async def main():
        import time
        from formatting import format_riven
        s = time.time()
        print(len(await get_data()))
        print("done" + str(time.time() - s))
        s = time.time()
        async with RateLimitedClientSession(10, 3, 1, base_url=url) as session:
            r = await asyncio.gather(first_order("khora_prime_set", {}, session),
                                     first_order("ceramic_dagger", {"item_name": "陶瓷匕首"}, session, 1, True))
            for i in r:
                print(json.dumps(i, indent=4))
            print(format_riven(r[1]))
        print("done" + str(time.time() - s))


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
