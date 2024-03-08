def format_item(data):
    result = f"```item: {data['url_name']} ({data['item_name']})\n"
    result += f"price: {(str(data['platinum']) + 'p').ljust(19, ' ')}, quantity: {data['quantity']}\n"
    result += f"user: {data['user']['ingame_name'].ljust(20, ' ')}, locate: {data['user']['locale'].ljust(7, ' ')}, like:{data['user']['reputation']}```\n"
    return result


def format_query(data):
    result = ""
    for i in data:
        result += format_item(i)
    return result
