import winsound
import json
import argparse
import time
from datetime import datetime
from typing import Any

import requests

# Käyttäjän tiedot
SLEEP_LENGTH = 0

with open("user.json", "r", encoding="utf-8") as f:
    USER_INFO = json.loads(f.read())
ORDER_URL = 'https://www.luuppi.fi/service/products/orders'
ADD_ITEM_URL = 'https://www.luuppi.fi/service/products/orders/{}/reservations'
HEADERS = {
    'content-type': 'application/json;charset=UTF-8',
    'cookie': USER_INFO["COOKIE"],
}


def parse_cmd() -> int:
    """Parses the command line argument and returns the product ID"""
    parser = argparse.ArgumentParser(description="Sends HTTP request to order the product from Luuppi website")
    parser.add_argument("product_id", type=int, nargs=1)
    parser.add_argument("time", type=int, nargs=1)
    args = parser.parse_args()
    return args.product_id[0]


def read_json(byte_data: bytes) -> Any:
    """Reads byte data and returns the JSON format of the data"""
    return json.loads(byte_data.decode())


def create_order() -> int:
    """Creates the order and returns order ID"""
    kayttaja_data = { "owner_user_id": USER_INFO["USER_ID"] }
    response = requests.post(ORDER_URL, headers=HEADERS, json=kayttaja_data)
    return read_json(response.content)["id"]


def add_item(order_id: int, product_id: int) -> bool:
    """Adds item. Returns the response from the website"""
    url = ADD_ITEM_URL.format(order_id)
    data = { "products": [{ "product_id": product_id, "amount":1 }] }
    response = requests.post(url, headers=HEADERS, json=data)

    return response


def try_order(order_id: int, product_id: int) -> bool:
    """Tries to order the item. Returns True on success otherwise False"""
    response = add_item(order_id, product_id)
    json_data = read_json(response.content)[0]

    print(datetime.now().strftime("%H:%M:%S.%f")[:-4],
          "\t",
          f"status={response.status_code}",
          flush=True)

    if json_data["amount"]:
        return True
    else:
        return False


def main():
    """A"""
    product_id = parse_cmd()
    order_id = create_order()
    print(f"{order_id=} {product_id=}")
    while True:
        try:
            if try_order(order_id, product_id):
                print("Tuote tilattu!", flush=True)
                winsound.Beep(500, 10000)
                # Stop the program for 59 min 55 sec. After that, try to
                # order the outdated order again.
                time.sleep(59*60 + 55)
            time.sleep(SLEEP_LENGTH)
        except requests.exceptions.ConnectionError:
            time.sleep(SLEEP_LENGTH)
            print(flush=True)


if __name__ == "__main__":
    main()
