import requests
from bs4 import BeautifulSoup
import json
import datetime


# Функция для получения HTML-кода страницы
def get_html(url):
    response = requests.get(url)
    return response.text



def parse_poizonshop(html):
    soup = BeautifulSoup(html, 'lxml')
    sneakers = []

    # Находим все товары на странице
    products = soup.find_all(class_='product-card_product_card__5aPyG product-grid-pagination_product__LMyN_')
    print(products)
    # Проходимся по каждому товару и извлекаем информацию
    for product in products:
        try:
            brand = product.find(class_='product-card_name__amzGC').text.strip()
            print(brand.lower(), 'nike' in brand.lower())
            if 'nike' in brand.lower() or 'jordan' in brand.lower():
                name = product.find(class_='product-card_name__amzGC').text.strip()
                name = name.replace('"', '')
                price = product.find(class_='product-card-price_product_card_price__ei89N product-card-price_num__5RrTF product-card-price_sale__OOb_5').text.strip()
                price = price.replace('\xa0', ' ')
                link = "https://poizonshop.ru" + product.get('href')
                sneaker = {'name': name, 'price': price, 'link': link}
                sneakers.append(sneaker)
        except AttributeError:
            continue
    return sneakers


# Функция для сохранения данных в JSON файл
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Основная функция
def main():
    url = 'https://poizonshop.ru/february/sale'
    result = requests.get(url).content
    sneakers = parse_poizonshop(result)
    save_to_json(sneakers, f'sneakers_from_poizon_sale{datetime.date.today().isoformat()}.json')


if __name__ == '__main__':
    main()
