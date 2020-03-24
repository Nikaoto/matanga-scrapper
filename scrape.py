#from xvfbwrapper import Xvfb
import json
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as conds

GECKODRIVER_PATH = "/usr/local/bin/geckodriver"
EUR_TO_USD = 1.08
RUB_TO_USD = 0.01
UAH_TO_USD = 0.04

RUB_SIGN = "ք"
EUR_SIGN = "€"
UAH_SIGN = "₴"

NEXT_PAGE_BUTTON_TEXT = "Следующая →"
RUS_NO = "нет"
RUS_GRAM = "гр"

NOW = datetime.now().isoformat(timespec="seconds")

if len(sys.argv) < 2:
    print("save directory not specified")
    print("usage: python3 scrape.py save_dir")
    sys.exit(1)

OUT_FILE_DIR = sys.argv[1]
OUT_FILE_NAME = "{}/{}.json".format(OUT_FILE_DIR, NOW)

def ignore_non_utf(s):
    return bytes(s, "utf-8").decode("utf-8", "ignore")

def log(*args, **kwargs):
    print("{}: ".format(NOW), *args, **kwargs)

def scrape_items(driver):
    items = driver.find_elements_by_css_selector("div.banners>div.banner_item>div.banner_wrapper")
    if not items:
        return []

    ret_item_list = []
    for item in items:
        title_links = item.find_elements_by_css_selector("span.banner_title>a")
        seller_code = title_links[0].text.strip()
        seller_name = title_links[1].text.strip()
        item_name_raw = item.find_element_by_css_selector("div.banner_content_name>p").text.strip()
        item_name = ignore_non_utf(item_name_raw)
        description = item.find_elements_by_css_selector("ul.description>li")

        # Unit count
        unit_count_text = description[0].find_element_by_css_selector("span").text.strip()
        unit_count = 0
        if unit_count_text != RUS_NO:
            unit_count = int(unit_count_text)

        order_in_advance = description[1].find_element_by_css_selector("span").text.strip()
        unit_weight = float(description[3].find_element_by_css_selector("span").text.replace(RUS_GRAM, "").strip())
        #btc_price = prices[0].text.replace("BTC", "").strip()
        #ruble_price = prices[1].text.replace(RUBLE_SIGN, "").strip()

        # Unit price
        price_part_1 = item.find_element_by_css_selector("div.buy>div.price2>p").text.strip()
        price_part_2 = item.find_element_by_css_selector("div.buy>div.price2>span").text.strip()
        price_currency = price_part_2[-1]
        price_part_2 = price_part_2[:-1:]

        # Parse unit price number
        unit_price = 0
        if price_part_1:
            unit_price = float("{}{}".format(price_part_1, price_part_2))
        else:
            unit_price = float(price_part_2)
        unit_price = round(unit_price, 2)

        # Convert currency to USD if necessary
        if price_currency == RUB_SIGN:
            unit_price *= RUB_TO_USD
        elif price_currency == EUR_SIGN:
            unit_price *= EUR_TO_USD
        elif price_currency == UAH_SIGN:
            unit_price *= UAH_TO_USD
        elif price_currency != "$":
            log("Unknonw currency \"{}\"".format(price_currency))
        unit_price = round(unit_price, 2)

        total_weight = round(unit_weight * unit_count, 2)
        gram_price = round(unit_price / unit_weight, 2)
        new_item = {
            "date": NOW,
            "item_name": item_name,
            "seller_code": seller_code,
            "seller_name": seller_name,
            "order_in_advance": "no" if order_in_advance == RUS_NO else "yes",
            "unit_count": unit_count,
            "unit_weight": unit_weight,
            "usd_unit_price": unit_price,
            "usd_gram_price": gram_price,
            "total_weight": total_weight
        }
        ret_item_list.append(new_item)
    return ret_item_list

def get_next_page_link_element(driver):
    nav_links = driver.find_elements_by_css_selector("div.paddingthree>a")
    if not nav_links:
        return None
    nav_buttons = driver.find_elements_by_css_selector("div.paddingthree>a>button")
    if not nav_buttons:
        return None
    if nav_buttons[0].text == NEXT_PAGE_BUTTON_TEXT:
        return nav_links[0]
    if len(nav_buttons) < 2:
        return None
    if nav_buttons[1].text == NEXT_PAGE_BUTTON_TEXT:
        return nav_links[1]
    return False

def scrape_region(driver, product_list, url, region_code):
    driver.get(url)
    wait(driver, 30).until(lambda d: d.find_element_by_css_selector("label.RegionName>span"))

    # Check if category id correct
    category_found = False
    checkboxes = driver.find_elements_by_css_selector("label.RegionChild")
    for cb in checkboxes:
        category_id = cb.get_attribute("for")[-len(region_code)::]
        if category_id == region_code:
            category_found = True
            break

    # Exit if not found
    if not category_found:
        log("Category with id not found URL_UPDATE_NEEDED")
        return 1

    # Scrape and navigate to every page in region
    while True:
        items = scrape_items(driver)
        for item in items:
            product_list.append(item)
        next_page_link_element = get_next_page_link_element(driver)
        if next_page_link_element:
            next_page_link_element.click()
            wait(driver, 30).until(lambda d: d.find_element_by_css_selector("label.RegionChild"))
        else:
            break
    return 0

TBILISI_REGION_CODE = "1633"
BATUMI_REGION_CODE = "1634"
KUTAISI_REGION_CODE = "1896"
ANAKLIA_REGION_CODE = "1819"

TBILISI_URL = "https://matanga.guru/?sName=&sCase=all&sSellerID=&sSortType=dWeight_asc&iFirstLevel={}&iSecondLevel=".format(TBILISI_REGION_CODE)
BATUMI_URL = "https://matanga.guru/?sName=&sCase=all&sSellerID=&sSortType=dWeight_asc&iFirstLevel={}&iSecondLevel=".format(BATUMI_REGION_CODE)
KUTAISI_URL = "https://matanga.guru/?sName=&sCase=all&sSellerID=&sSortType=dWeight_asc&iSecondLevel=&iFirstLevel={}#ContentBar".format(KUTAISI_REGION_CODE)
ANAKLIA_URL = "https://matanga.guru/?sName=&sCase=all&sSellerID=&sSortType=dWeight_asc&iFirstLevel={}#ContentBar".format(ANAKLIA_REGION_CODE)

# Set up virtual display (for headless browser)
#vdisplay = Xvfb()
#vdisplay.start()

# Set profile (Tor proxy)
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()

# Set options (headless)
options = webdriver.FirefoxOptions()
options.headless = False

def create_driver():
    return webdriver.Firefox(firefox_profile=profile, options=options, executable_path=GECKODRIVER_PATH)

product_list = []

# Scrap Tbilisi
driver = create_driver()
retcode = scrape_region(driver, product_list, TBILISI_URL, TBILISI_REGION_CODE)
if retcode == 1:
    log("Tbilisi scrapping failed")
driver.quit()

# Scrap Batumi
driver = create_driver()
retcode = scrape_region(driver, product_list, BATUMI_URL, BATUMI_REGION_CODE)
if retcode == 1:
    log("Batumi scrapping failed")
driver.quit()

# Scrap Kutaisi
driver = create_driver()
retcode = scrape_region(driver, product_list, KUTAISI_URL, KUTAISI_REGION_CODE)
if retcode == 1:
    log("Kutaisi scrapping failed")
driver.quit()

# Scrap Anaklia
driver = create_driver()
retcode = scrape_region(driver, product_list, ANAKLIA_URL, ANAKLIA_REGION_CODE)
if retcode == 1:
    log("Anaklia scrapping failed")
driver.quit()

file = open(OUT_FILE_NAME, "w", encoding="utf8")
json.dump(product_list, file, ensure_ascii=False, sort_keys=False, indent=2)
file.close()

#vdisplay.stop()
