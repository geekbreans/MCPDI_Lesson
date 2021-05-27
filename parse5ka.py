from pathlib import Path
import json
import time
import requests


class Parse5ka:
    headers = {"User-Agent": "Philipp Kirkorov2"}
    params = "store=None, records_per_page=12, page=1, categories=698, ordering=None, price_promo__gte=None, price_promo__lte=None, search=None"

    def __init__(self, start_url: str, save_dir: Path):
        self.start_url = start_url
        self.save_dir = save_dir

    def _get_response(self, url: str) -> requests.Response:
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.2)

    def run(self):
        for product in self._parse(self.start_url):
            file_name = f"{product['id']}.json"
            file_path = self.save_dir.joinpath(file_name)
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            yield from data["results"]

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), 'utf8')




class Parse5kae(Parse5ka):

    def __init__(self, start_url: str, save_dir: Path, category_url:str):
        self.start_url = start_url
        self.save_dir = save_dir
        self.category_url = category_url

    def _parselevel0(self):
        response = requests.get(self.categoris_url, headers=self.headers)
        # data = json.load(response.json())
        data = response.json()
        for p in data:
            print('group_name: ' + p['parent_group_name'])
            print('group_code: ' + p['parent_group_code'])
            parent_group_code= p['parent_group_code']
            url = f'url="https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories={parent_group_code}&ordering=&price_promo__gte=&price_promo__lte=&search="'

        # print(response.json())
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            yield from data["results"]


    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            yield from data["results"]

    def _add_dict(self, data: dict):
        # print(type(data))
        # print(data)
        str_json = json.dumps(data, ensure_ascii=False)
        # print(str_json)
        # print(type(str_json))
        # file_path.write_text(json.dumps(data))
        # file_path.write_text(str_json, 'utf8')
        # file_path.write_text(json.dumps(data, ensure_ascii=False), 'utf8')


        # print(type(data))
        # print(data)
        # for key, val in data.items():
        #     print(key, val)


    def run(self):
        response = requests.get(self.category_url, headers=self.headers)
        # data = json.load(response.json())
        data = response.json()
        for p in data:

            d = {'name': p['parent_group_name'], 'code': p['parent_group_code'], "products": []}

            print('group_name: ' + p['parent_group_name'])
            print('начало ________________________________________________________')
            # print('group_code: ' + p['parent_group_code'])
            parent_group_name = p['parent_group_name']
            parent_group_code = p['parent_group_code']
            url = f'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories={parent_group_code}&ordering=&price_promo__gte=&price_promo__lte=&search'
            # print(url)
            file_name = f"{parent_group_name + ' '+parent_group_code}.json"
            file_path = self.save_dir.joinpath(file_name)
            print('file_path  ', file_path)

            for product in self._parse(url):
                # file_name = f"{product['id']}.json"
                # file_path = self.save_dir.joinpath(file_name)
                # print('file_path  ', file_path)
                # list.append(product)
                # print(product['name'])
                d["products"].append(product)
                # d["products"].append(product['name'])

            print('конец ________________________________________________________')
            # if d["products"] is not None:
            #     print(d)
            file_path.write_text(json.dumps(d, ensure_ascii=False), 'utf8')


def get_dir_path(dir_name: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"

    # url="https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories=698&ordering=&price_promo__gte=&price_promo__lte=&search="
    # save_dir = get_dir_path("products")
    # parser = Parse5ka(url, save_dir)
    # parser.run()

    category_url = 'https://5ka.ru/api/v2/categories/'
    save_dir = get_dir_path("products_by_category")
    # print ( 'save_dir ', save_dir)

    parser = Parse5kae(url, save_dir, category_url)
    parser.run()

