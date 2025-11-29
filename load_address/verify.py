import os

from elasticsearch import Elasticsearch

ES_URL = os.environ["ES_URL"]
INDEX = os.environ["ES_INDEX"]
print(ES_URL)
print(INDEX)
# see if load done with success
es = Elasticsearch(hosts = [ES_URL], verify=False)
print(es.ping())
res = es.search(index = INDEX, query={"term": {"id":{"value":72000}}})
print(f"the data is loaded with index {INDEX}, return value is: {res}")