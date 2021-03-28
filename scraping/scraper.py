from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
from time import sleep

def search_tesco(search_item, driver=None):
    url = "https://www.tesco.com/groceries/en-GB/search?query="
    search_url = url+search_item
    
    driver = webdriver.Chrome('./chromedriver') if not driver else driver
    driver.get(search_url)
#     cookie_clicked = False
#     while not cookie_clicked:
#         try:
#             driver.find_element_by_xpath("//*[@id=\"onetrust-accept-btn-handler\"]").click()
#             cookie_clicked = True
#         except:
#             sleep(0.5)
            
    column_names = ["product_name", "total_price", "unit_price", "img", "link"]
    data = pd.DataFrame(columns = column_names)
    
    sleep_count = 0
    sleep_len = 0.5
    max_sleep_count = 5 // sleep_len
    sleep(0.5)
    
    while True:
        soup = bs(driver.page_source)
    
        try:
            section = soup.find("ul", {"class": "product-list grid"})
            products = section.find_all("li", {"class": "product-list--list-item"})
            if (len(products)!=0):
                break
            sleep_count += 1
            sleep(0.5)
            if (sleep_count >= max_sleep_count):
                print("Can't find product!")
                return data
        except IndexError:
            return data
        except:
            print("Unknown error")
        
    domain = "https://www.tesco.com"
   
    for product in products[:24]:
        try:
            name = product.find("a", {"class": "ui__StyledLink-sc-18aswmp-0 bfYkKW"}).text
            link = product.find("a", {"class": "ui__StyledLink-sc-18aswmp-0 bfYkKW"})["href"]
            product_link = domain+link
            total_price_element = product.find("div", {"class": "price-per-sellable-unit"})
            currency = total_price_element.find("span", {"class":"currency"}).text
            price = total_price_element.find("span", {"class": "value"}).text
            total_price_info = currency+price
            unit_price_element = product.find("div", {"class": "price-per-quantity-weight"})
            unit_currency = unit_price_element.find("span", {"class":"currency"}).text
            unit_price = unit_price_element.find("span", {"class": "value"}).text
            unit_weight = unit_price_element.find("span", {"class": "weight"}).text
            unit_price_info = unit_currency+unit_price+unit_weight
            image = product.find("img", {"class": "product-image"})['src']
            data_row = pd.Series([name, total_price_info, unit_price_info, image, product_link], index = column_names)
            data = data.append(data_row, ignore_index = True)
        except: 
            continue
    
    return data


def search_sainsburys(search_item, driver = None):
    url = "https://www.sainsburys.co.uk/gol-ui/SearchDisplayView?filters[keyword]="
    search_url = url+search_item
    
    driver = webdriver.Chrome('./chromedriver') if not driver else driver

    sleep_count = 0
    sleep_len = 0.5
    max_sleep_count = 2 // sleep_len
        
    driver.get(search_url)
    cookie_clicked = False
    while not cookie_clicked:
        try:
            driver.find_element_by_xpath("//*[@id=\"onetrust-accept-btn-handler\"]").click()
            cookie_clicked = True
        except:
            sleep_count += 1
            sleep(sleep_len)
            if (sleep_count >= max_sleep_count):
                break
            
    column_names = ["product_name", "total_price", "unit_price", "img", "link"]
    data = pd.DataFrame(columns = column_names)

    sleep_len = 0.5
    
    soup = bs(driver.page_source)
    header_ele = soup.find("h1", {"class": "si__title"})
    header = header_ele.text if header_ele else "Fetching results"
    while "Fetching results" in header:
        print(header)
        sleep(sleep_len)
        soup = bs(driver.page_source)
        header_ele = soup.find("h1", {"class": "si__title"})
        header = header_ele.text if header_ele else "Fetching results"
        
    print(header)
    
    if "0 results" in header:
        return data

    section_ele = soup.find_all("section", {"class": "ln-o-section ln-o-section"})
    while not section_ele:
        sleep(sleep_len)
        section_ele = soup.find_all("section", {"class": "ln-o-section ln-o-section"})
    section = section_ele[0]
    products = section.find_all("li", {"class": "pt-grid-item ln-o-grid__item ln-u-6/12@xs ln-u-3/12@md ln-u-2/12@xl"})
        
    for product in products[:60]:
        text_bar = product.find("h2", {"class": "pt__info__description"})
        img = product.find("img", {"class": "pt-image pt-image__product"})["src"]
        costs_bar = product.find("div", {"class": "pt__cost"})
        total_price = costs_bar.find("div").text
        unit_price = costs_bar.find("span").text
        name = text_bar.text
        link = text_bar.find("a", href=True)["href"]
        data_row = pd.Series([name, total_price, unit_price, img, link], index = column_names)
        data = data.append(data_row, ignore_index = True)
    
    return data

if __name__ == '__main__':
    supported_supermarkets = ["Sainsburys", "Tesco"]
    scraping_funcs = [search_sainsburys, search_tesco]

    supermarket_dict = {supermarkets:scraping_funcs[idx] for idx, supermarkets in enumerate(supported_supermarkets)}
    driver = webdriver.Chrome('./chromedriver')

    shopping_cart = ["eggs", "banana", "cumin powder", "spatula", "frog"]
    scraped_data = {i:{} for i in shopping_cart}


    for item in shopping_cart:
        for supermarket in supermarket_dict:
            scrape_func = supermarket_dict[supermarket]
            scraped_data[item][supermarket] = scrape_func(item, driver)
    
    print(scraped_data)