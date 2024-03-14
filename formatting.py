def format_item(data, simplify=False):
    result = f"{data['url_name']} ({data['item_name']})"
    if simplify:
        result += f" price: {data['platinum']} p\n"
    else:
        result = "```" + result
        result += f"\nprice: {(str(data['platinum']) + 'p').ljust(19, ' ')}, quantity: {data['quantity']}\n"
        result += f"user: {data['user']['ingame_name'].ljust(20, ' ')}, locate: {data['user']['locale'].ljust(7, ' ')}```\n"
    return result


def format_riven(data):
    result = f"```{data['item']['weapon_url_name']} ({data['item_name']}) price: {data['buyout_price']} p\n"
    result += f"Rank: {data['item']['mod_rank']}, rolls: {data['item']['re_rolls']}\n"
    for i in sorted(data["item"]["attributes"], key=lambda i: i["positive"], reverse=True):
        result += f"type: {i['url_name'].ljust(27, ' ')}, value: {i['value']}\n"
    result += f"Seller: {data['owner']['ingame_name']}, locate: {data['owner']['locale']}, platform: {data['platform']}```\n"
    return result


def format_query(data, simplify=False, riven=False):
    result = ""
    for i in data:
        if riven:
            result += format_riven(i)
        else:
            result += format_item(i, simplify)
    return result
