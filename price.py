import requests

vendor_name = {
    "ayyareh": "عیاره",
    "bazaretala": "بازارطلا",
    "daric": "داریک",
    "digikala": "دیجیکالا",
    "eqlimagold": "اقلیما",
    "faragold": "فراگلد",
    "geram": "گرم",
    "goldbaan": "گلدبان",
    "goldenfa": "گلدنفا",
    "goldika": "گلدیکا",
    "hamrahgold": "همراه گلد",
    "igolden": "آیگلدن",
    "melligold": "ملی گلد",
    "milli": "میلی",
    "saraf": "صراف",
    "talaavan": "طلاوان",
    "talajet": "طلاجت",
    "talapp": "طلاپ",
    "talasaan": "طلاسان",
    "talasea": "طلاسی",
    "technogold": "تکنوگلد",
    "tlyn": "طلاین",
    "up": "آپ",
    "wallgold": "والگلد",
    "zarafza": "زرافزا",
    "zarminex": "زرمینکس",
    "zarpaad": "زرپاد",
    "zarpay": "زرپی",
}


def get_available_vendors():
    url = "https://gold-price-modopod.liara.run/api/v1/prices/get_available_vendors?sort_by=best_price"
    response = requests.get(url)
    return response.json()["data"]


def get_price_by_vendor(vendor):
    url = f"https://gold-price-modopod.liara.run/api/v1/prices/get_vendor_prices/1h?vendor_name={vendor}"
    response = requests.get(url)
    data = response.json()
    prices = data["prices"]
    if not prices:
        return None
    prices = prices[-1]
    del prices["timestamp"]
    return prices


def get_all_vendors_prices():
    vendors = get_available_vendors()
    data = []
    for vendor in vendors:
        print(vendor)
        prices = get_price_by_vendor(vendor)
        if not prices:
            continue
        if prices["buy_price"] == 0 or prices["sell_price"] == 0:
            continue
        prices["vendor"] = vendor_name[vendor]
        data.append(prices)

    return data


print(get_all_vendors_prices())
