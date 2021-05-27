from pathlib import Path
import json
import time
import requests


class Parse5ka:
    headers = {"User-Agent": "Philipp Kirkorov2"}

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

    def __init__(self, save_dir: Path, category_url: str):
        self.save_dir = save_dir
        self.category_url = category_url

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            yield from data["results"]

    def run(self):
        response = requests.get(self.category_url, headers=self.headers)

        data = response.json()
        for p in data:

            d = {'name': p['parent_group_name'], 'code': p['parent_group_code'], "products": []}
            parent_group_name = p['parent_group_name']
            parent_group_code = p['parent_group_code']
            url = f'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories={parent_group_code}&ordering=&price_promo__gte=&price_promo__lte=&search'

            file_name = f"{parent_group_name + ' ' + parent_group_code}.json"
            file_path = self.save_dir.joinpath(file_name)

            for product in self._parse(url):
                d["products"].append(product)
                # d["products"].append(product['name'])

            file_path.write_text(json.dumps(d, ensure_ascii=False), 'utf8')


def get_dir_path(dir_name: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"

    # save_dir = get_dir_path("products")
    # parser = Parse5ka(url, save_dir)
    # parser.run()

    category_url = 'https://5ka.ru/api/v2/categories/'
    save_dir = get_dir_path("products_by_category")

    parser = Parse5kae(save_dir, category_url)
    parser.run()
