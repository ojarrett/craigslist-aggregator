import re

def parse_price(price_field):
    return float(price_field.split("$")[1].replace(',',''))

def parse_rooms(rooms_field):
    if rooms_field:
        rooms = re.search(r"([0-9]+)br", rooms_field)
        if rooms:
            rooms = rooms.group(1)
            return int(rooms)

    return -1
