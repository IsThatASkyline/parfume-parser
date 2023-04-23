import csv, requests
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=t9d7d50idhn0poe9lirmhdkvh2; _ym_uid=1678647398247951180; _ym_d=1678647398; _ym_isad=1; _ym_visorc=w; browsed_products=2277%2C6606%2C7291%2C7281%2C7398%2C6923%2C6947%2C7151%2C7189%2C7361%2C2244',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

# def get_brands():
#     url = 'http://parfume-opt.ru/catalog'
#     r = requests.get(url=url, headers=headers).text
#     soup = BeautifulSoup(r, 'lxml')
#     brands = soup.find('ul', class_='brandlist').find_all('li')
#     brand_list = []
#     for brand in brands:
#         brand_name = brand.get_text().strip('\n').strip()
#         brand_list.append(brand_name)
#     print(brand_list)
#     return brand_list
#
# brand_list = get_brands()

cat_name = 'kosmetika'

with open(f'{cat_name}_new.csv', 'w', encoding='utf8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ('Название', 'Категория')
    )


with open(f'{cat_name}.csv', encoding='utf8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tags = ['новинки парфюмерии 2021-2022', 'Селективная (нишевая) парфюмерия', 'Тестер', 'Качество LUXE', 'оригинальная упаковка', 'Мужские тестеры', 'Женские тестеры']
        try:
            title = row['Название']
            for tag in tags:
                try:
                    if tag in title:
                        try:
                            title = title.lstrip(tag)
                        except:
                            pass

                except Exception as ex:
                    print(ex)
                    continue
        #     try:
        #         brand = [x for x in brand_list if x in title][0]
        #     except:
        #         brand = None
        except Exception:
            title = None

        # new_price = int(int(row['Цена']) * 1.2)
        # print(title, row['Название'], new_price, brand, row['Категория'], row['Описание'], row['Картинки'], row['Ссылка на товар'])
        with open(f'{cat_name}_new.csv', 'a', encoding='utf8') as file:
            writer = csv.writer(file)

            writer.writerow(
                [title, row['Категория']]
            )
