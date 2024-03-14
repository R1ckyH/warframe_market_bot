from formatting import *
from query import *


if __name__ == "__main__":
    async def main():
        s = time.time()
        data = await search_price(await load_data(), "all", True)
        print(len(data))
        data = sorted(data, key=lambda i: i["platinum"], reverse=True)
        with open("data/price.txt", "w") as f:
            f.write(format_query(data, True))
        print("done" + str(time.time() - s))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
