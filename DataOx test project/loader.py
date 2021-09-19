import requests, csv
import calendar, time
from contextlib import closing
from info import Info
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['DataOx_DB']
collection = db['main_collection']

main_company = ''


class Loader:

    def __init__(self):
        self.url = "https://query1.finance.yahoo.com/v7/finance/download/{company}?period1=0&period2={now}&interval=1d&events=history&includeAdjustedClose=true"
        self.headers = {
            "referer": "https://finance.yahoo.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    def current_timestamp(self):
        return calendar.timegm(time.gmtime())

    def generate_url(self, company_name, current_timestamp):
        return self.url.format(company=company_name, now=current_timestamp)

    def load_data(self, url):
        result = []

        with closing(requests.get(url, headers=self.headers)) as r:
            lines = (line.decode('utf-8') for line in r.iter_lines())

            reader = csv.reader(lines)
            next(reader)

            for row in reader:
                result.append(self.handle_row(row))

        return result

    def toDB(self, row):
        data = {"_id": main_company + ' ' + row[0],
                "date": row[0],
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
                "adj_close": row[5],
                "volume": row[6],
                }
        try:
            collection.insert_one(data)
        except Exception:
            pass

    def handle_row(self, row):
        self.toDB(row)
        return Info(row).__dict__

    def load(self, company):
        date = self.current_timestamp()
        url = self.generate_url(company, date)
        return self.load_data(url)


data_loader = Loader()
