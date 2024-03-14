import json

from utils import *
from api import *


with open("data/test.json", "w") as f:
    json.dump(get_data(), f, indent=4, ensure_ascii=False)