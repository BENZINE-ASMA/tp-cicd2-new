import os

import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ES_URL = os.environ["ES_URL"]
INDEX = os.environ["ES_INDEX"]
print(ES_URL)
print(INDEX)
url = "https://api-adresse.data.gouv.fr/search"


adresses = [
    "8+bd+du+port",
    "12+rue+emil+renaud",
    "5+rue+thomas+edison",
    "12+rue+marechal+ney",
]
es = Elasticsearch(hosts=["http://es01:9200"], verify_certs=False)
print(es.ping())

for adresse in adresses:
    params = {"q": adresse}
    res = requests.get(url, params=params)
    for record in res.json()["features"]:
        print(record["properties"])
        id = int(record["properties"]["postcode"])
        requests.post(
            f"{ES_URL}/{INDEX}-2022-12-07/_doc/{id}",
            json={"id": id, "data": record},
        )

requests.post(
    f"{ES_URL}/_aliases",
    json={
        "actions": [
            {"add": {"index": f"{INDEX}-2022-12-07", "alias": f"{INDEX}"}}
        ]
    },
    verify=False,
)
