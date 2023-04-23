import csv
from bs4 import BeautifulSoup
import asyncio
import aiohttp

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
with open('data2.csv', 'w', encoding='utf8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ('Название', 'Цена', 'Описание', 'Картинки', 'Ссылка на товар')
    )

i = 1

async def gather_data():
    url = 'http://parfume-opt.ru/catalog/'
    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        r = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await r.text(), 'lxml')
        pages_count = int(soup.find('div', class_='pagination').find_all('a')[-2].get_text())
        print(pages_count)

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_card_links(session, page))
            tasks.append(task)

            await asyncio.gather(*tasks)



async def get_card_links(session, page):
    url = f'http://parfume-opt.ru/catalog/?page={page}'
    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find('div', class_='productslist block').find_all('div', class_='ProductWrapper')
        tasks = []
        for card in cards:
            href = HOST + card.find('div', class_='Details').find('a').get('href')
            task = asyncio.create_task(get_card_info(session, href))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def get_card_info(session, href):
    try:
        async with session.get(url=href, headers=headers) as response:

            src = await response.text()
            print(src)
            soup = BeautifulSoup(src, 'lxml')
            card = soup.find('div', class_='ProductCard')

            try:
                title = card.find('div', class_='Information').find('h2').get_text().strip()
            except Exception:
                title = None

            try:
                price = int(card.find('div', class_='PriceProductCard').find('span', class_='color').get_text().replace(' ', '')) + 1000
            except Exception:
                price = None

            try:
                info = card.find('div', class_='Info').find('div', class_='Description').get_text().strip()
            except Exception:
                info = None

            try:
                images = card.find('div', class_='Images').find_all('a')
                img_links = []
                for image in images:
                    img_link = image.get('href')
                    img_links.append(img_link)
            except Exception:
                img_links = None

            print(f'Название: {title}')
            print(f'Цена(старая): {int(price)-1000} руб.')
            print(f'Цена(новая): {int(price)} руб.')
            print(f'Описание: {info}')
            print(f'Картинки: {img_links}')
            print(f'Ссылка на товар: {href}')
            print('-' * 10)


            with open('data2.csv', 'a', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow(
                   [title, price, info, img_links, href]
                )
    except Exception as ex:
        print(ex)
        print(href)
        pass
    global i
    print(f'Обработал {i} товаров')
    i += 1


def main():
    asyncio.run(gather_data())


if __name__ == '__main__':
    main()