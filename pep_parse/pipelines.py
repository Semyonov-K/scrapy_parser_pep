from datetime import datetime
from .settings import BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.count_of_status = {}

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%dT%H-%M-%S')
        file_name = f'status_summary_{timestamp}.csv'
        file_path = results_dir / file_name
        total = sum(self.count_of_status.values())
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for key, value in self.count_of_status.items():
                f.write(f'{key},{value}\n')
            f.write(f'Total,{total}\n')

    def process_item(self, item, spider):
        status = item['status']
        if status not in self.count_of_status:
            self.count_of_status[status] = self.count_of_status.get(status, 0) + 1
        else:
            self.count_of_status[status] += 1
        return item
