# import requests
import aiocsv
import os
import aiohttp
import asyncio
import aiofiles
from aiocsv import AsyncWriter
from gitignore import headers, cookies






async def main(id_chat_message):


    filename = "database.csv"
    if os.path.isfile(filename):
        os.remove(filename)

    async with aiofiles.open(filename, 'w', newline='', encoding='utf-8') as file:
        await file.write('\ufeff')
        new_row = [
            "ІД абітурієнта", "ФІО", 'Конкурсний бал', "Пріоритет чи контракт", 'Квота якщо є'
        ]
        writer = AsyncWriter(file, delimiter=';')
        await writer.writerow(new_row)




    cookies = {
        '_ga': 'GA1.1.870051912.1687180766',
        'PHPSESSID': 'ka9rrac0cb66o70makeiftnqpu',
        '_ga_WLDPX624RK': 'GS1.1.1689312206.6.0.1689312207.0.0.0',
        '_ga_W6WT1K3VXZ': 'GS1.1.1689509036.4.1.1689509594.0.0.0',
        '_ga_YC32TV7WL7': 'GS1.1.1689772565.1.1.1689772576.0.0.0',
        '_ga_96Q7K30V0N': 'GS1.1.1689790129.11.1.1689790311.0.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.1.870051912.1687180766; PHPSESSID=ka9rrac0cb66o70makeiftnqpu; _ga_WLDPX624RK=GS1.1.1689312206.6.0.1689312207.0.0.0; _ga_W6WT1K3VXZ=GS1.1.1689509036.4.1.1689509594.0.0.0; _ga_YC32TV7WL7=GS1.1.1689772565.1.1.1689772576.0.0.0; _ga_96Q7K30V0N=GS1.1.1689790129.11.1.1689790311.0.0.0',
        'Origin': 'https://vstup.edbo.gov.ua',
        'Referer': f'https://vstup.edbo.gov.ua/offer/{id_chat_message}/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Opera";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'id': f'{id_chat_message}',
        'last': '0',
    }
    try:
        async with aiohttp.ClientSession() as session:

            response = await session.post('https://vstup.edbo.gov.ua/offer-requests/', cookies=cookies, headers=headers, data=data)
            info = await response.json(content_type='text/html')
            offer = {}
            for item in info['requests']:
                offer['id_chela'] = item['prid']
                offer['imena'] = item['fio']
                if 'kv' in item and isinstance(item['kv'], float):
                    offer['konk_ball'] = str(item['kv']).replace('.', ',')

                if item['p'] == 0:
                    offer['prior_kontr'] = 'kontrakt'
                else:
                    offer['prior_kontr'] = item['p']
                if len(item['rss']) == 5:
                    offer['kvota'] = item['rss'][4]['sn']
                else:
                    offer['kvota'] = 'nety'


                async with aiofiles.open('database.csv', 'a', newline='', encoding='utf-8') as file:
                    await file.write('\ufeff')
                    writer = AsyncWriter(file, delimiter=';')
                    await writer.writerow([offer['id_chela'], offer['imena'], offer['konk_ball'], offer['prior_kontr'],offer['kvota']])
        return 'database.csv'
        pass
    except KeyError as e:
        print('Ошибка ввода')
    # except aiohttp.client_exceptions.ContentTypeError as e:
    #     print(f"Ошибка декодирования JSON: {e}")


if __name__ == '__main__':
    asyncio.run(main())
