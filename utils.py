from datetime import datetime
from difflib import SequenceMatcher


def replace_utils(a):
    return a.replace(" ", "").replace("_", "").lower()


def similar(a: str, b: str):
    return max(SequenceMatcher(None, a, b).ratio(), SequenceMatcher(None, replace_utils(a), replace_utils(b)).ratio())


def check_similarity(query, item, threshold=0.858):
    return similar(query, item["url_name"]) >= threshold or similar(query, item["item_name"]) >= threshold


def int_to_time(a: int):
    return datetime.fromtimestamp(a).strftime('%Y/%m/%d %H:%M:%S')