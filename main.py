import csv, requests
from bs4 import BeautifulSoup
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


imagekit = ImageKit(
    private_key='private_do1FXujbwKzH4nSUNRvZbLephFw=',
    public_key='public_zkN4djyCUZazCOuPLXOHazkJBUw=',
    url_endpoint='https://ik.imagekit.io/q6gbfd9lb'
)

HOST = 'http://parfume-opt.ru/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=t9d7d50idhn0poe9lirmhdkvh2; _ym_uid=1678647398247951180; _ym_d=1678647398; _ym_isad=1; _ym_visorc=w; browsed_products=2277%2C6606%2C7291%2C7281%2C7398%2C6923%2C6947%2C7151%2C7189%2C7361%2C2244',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
cat_name = 'all_categories2'
# url = f'http://parfume-opt.ru/catalog/{cat_name}'
url = 'http://parfume-opt.ru/catalog/'
brand_list = []

def get_brands():
    url = 'http://parfume-opt.ru/catalog'
    r = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(r, 'lxml')
    brands = soup.find('ul', class_='brandlist').find_all('li')
    for brand in brands:
        brand_name = brand.get_text().strip('\n').strip()
        brand_list.append(brand_name)
    print(brand_list)
    return brand_list



def get_pages_count(url):
    with open(f'{cat_name}.csv', 'w', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ('Название', 'Цена', 'Бренд', 'Категория', 'Описание', 'Картинки', 'Ссылка на товар')
        )

    # url = 'http://parfume-opt.ru/catalog/'
    r = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(r, 'lxml')
    try:
        pages_count = int(soup.find('div', class_='pagination').find_all('a')[-2].get_text())
    except Exception:
        pages_count = 1
    print(pages_count)
    return url, pages_count



def get_card_links(url, pages_count):
    all_cards_links = []
    for page in range(1, pages_count + 1):
        link = f'{url}?page={page}'
        print(f'Делаю запрос к странице: {link}')
        r = requests.get(url=link, headers=headers).text
        soup = BeautifulSoup(r, 'lxml')
        cards = soup.find('div', class_='productslist block').find_all('div', class_='ProductWrapper')

        for card in cards:
            href = HOST + card.find('div', class_='Details').find('a').get('href')
            all_cards_links.append(href)

    return all_cards_links

def get_card_info(all_cards_links):
    all_len = len(all_cards_links)
    for i, link in enumerate(all_cards_links):
        try:
            r = requests.get(url=link, headers=headers).text
            soup = BeautifulSoup(r, 'lxml')
            card = soup.find('div', class_='ProductCard')
            tags = ['новинки парфюмерии 2021-2022', 'Селективная (нишевая) парфюмерия', 'Тестер', 'Качество LUXE', 'Женская', 'Мужская', 'оригинальная упаковка', 'Мужские тестеры', 'LUXE', 'TESTER', 'Женские тестеры']
            try:
                title = card.find('div', class_='Information').find('h2').get_text().strip()
                for tag in tags:
                    try:
                        if tag in title:
                            try:
                                title = title.lstrip(tag)
                            except:
                                pass
                            try:
                                title = title.rstrip(tag)
                            except:
                                pass
                    except Exception as ex:
                        print(ex)
                        continue
                try:
                    brand = [x for x in brand_list if x in title][0]
                except:
                    brand = None
            except Exception:
                title = None
                brand = None

            try:
                price = int((int(card.find('div', class_='PriceProductCard').find('span', class_='color').get_text().replace(' ', '')) + 1000) * 1.2)
            except Exception:
                price = int((int(card.find('div', class_='PriceProductCard').find('span').get_text().replace(' ', '')) + 1000) * 1.2)

            try:
                info = card.find('div', class_='Info').find('div', class_='Description').get_text().strip()
            except Exception:
                info = None

            # try:
            #     images = card.find('div', class_='Images').find_all('a')
            #     img_links = []
            #     for image in images:
            #         img_link = image.get('href')
            #         img_links.append(img_link)
            #     img = img_links[0]
            #     img_name = img.split('http://parfume-opt.ru/files/products/')[1].replace(' ', '_').replace('%', '_').replace('?', '_')
            #     imagekit.upload(
            #         file=img,
            #         file_name=f"{img_name}.jpg",
            #         options=UploadFileRequestOptions(
            #             use_unique_file_name=False,
            #         )
            #     )
            #     img_link = f'https://ik.imagekit.io/q6gbfd9lb/{img_name}.jpg'
            # except Exception as ex:
            #     print(ex)
            #     img_link = None
            img_link = None

            print(f'Название: {title}')
            print(f'Бренд: {brand}')
            # print(f'Цена(старая): {int(price)-1000} руб.')
            print(f'Цена(новая): {int(price)} руб.')
            print(f'Описание: {info}')
            print(f'Картинка: {img_link}')
            # print(f'Картинки: {img_links}')
            print(f'Ссылка на товар: {link}')
            print('-' * 10)


            with open(f'{cat_name}.csv', 'a', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow(
                   [title, price, brand, 'Что', info, img_link, link]
                )
        except Exception as ex:
            print(ex)
            print(link)
            pass
        print(f'Обработал {i+1}/{all_len}')



def main():
    get_brands()
    link, pages_count = get_pages_count(url)
    get_card_info(get_card_links(link, pages_count))


if __name__ == '__main__':
    main()