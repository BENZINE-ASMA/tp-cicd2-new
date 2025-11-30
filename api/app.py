import os, sys
from math import *
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

def create_app(elastic_host, elastic_index, elastic_user=None, elastic_pass=None):
    print("starting api ...")
    elastic_host = elastic_host
    elastic_index = elastic_index
    app = FastAPI(title="Exposition API adresse postale")
    
    # Ajout du middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En production, spécifiez les domaines autorisés
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("connect to elastic cluster ...")
    if elastic_user and elastic_pass:
        print("using authenticated connection ...")
        es = Elasticsearch(hosts=[elastic_host], verify_certs=False, http_auth=(elastic_user, elastic_pass))
    else:
        es = Elasticsearch(hosts=[elastic_host], verify_certs=False)
    print(f"connection verify : {es.ping()}")
    
    @app.get("/postcode/{postcode}", summary="get information by postcode")
    def get_postcode(postcode):
        res = es.search(index=elastic_index, query={"term": {"id": {"value": postcode}}})
        if len(res["hits"]["hits"]) == 0:
            raise HTTPException(status_code=404, detail="postcode information not found")
        return res["hits"]["hits"]
    
    @app.get("/health", summary="healthcheck")
    def health():
        return {
            "elastic_ok": es.ping(),
            "index": elastic_index,
            "auth_enabled": bool(elastic_user and elastic_pass)
        }
    
    # SUPPRIMÉ : L'endpoint /debug avec eval() est une FAILLE DE SÉCURITÉ MAJEURE
    # Il permettait l'exécution de code arbitraire sur le serveur
    # Si vous avez vraiment besoin de debug, utilisez des logs appropriés
    
    return app