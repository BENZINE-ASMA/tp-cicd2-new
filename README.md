# tp-examen

## Excercice1: 
l'objectif de cette exercice est de lancer une API qui permet de récuperer des informations d'une adresse par code postal, et de mettre en place une pipeline ci/cd pour automatiser la creation et le deploiement de votre solution

***Question 1***

Votre developpeur a besoin d'un environnement de developpement dans un 1er temps afin de valider le fonctionnement de l'API. 

Les conteneurs utiliseront un network appelé elastic .  

vous devez lancer 4 conteneurs :

* Un conteneur api pour lancer api : 
  * L'image utilisée est python:3.11-slim-buster
  * Le port 8080 de la machine hote sur le port 8080 de votre conteneur api
  * Votre repertoire de travail est /app dans le conteneur qui contiendra l'ensemble des fichiers nécéssaire pour lancer l'application
  * Il faudra lancer le script 'run.py' pour demarrer votre api (python run.py) 
  * Vous pouvez ouvrir votre swager http://localhost:8080/docs et effectuer un test du endpoint /postcode/{postcode} (72000 par exemple). 

* Un conteneur load pour importer les données adresse dans cotre cluster elastic :
  * L'image utilisée est python:3.11-slim-buster
  * Votre repertoire de travail est /load dans le conteneur qui contiendra l'ensemble des fichiers nécéssaire pour lancer l'application
  * Il faudra lancer le script 'address.py' pour charger les données adresses (python address.py) 
  * Le script 'verify.py' vous permet de vérifier si les données sont bien load dans elastic 
* Un conteneur es01 pour lancer votre cluster elastic :
  * L'image utilisée est : docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:9.2.1
  * Le port 9200 de la machine hote sur le port 9200 de votre conteneur elastic
  * il faudra trouver une solution pour eviter son arret soudain 
* Un conteneur kib01 pour kibana :
  * Le port 5601 de la machine hote sur le port 5601 de votre conteneur kibana 
  * l'image utilisée est : docker.elastic.co/kibana/kibana:8.5.2

***Question 2*** 
Creer un docker-compose-dev.yml pour lancer vos contneurs.

Vous devez trouver une méthode qui permettera à votre developpeur de travailler directement à l'interieur du conteneur api sans créer d'image ou lancer un nouveau up à chaque changement/modification. 

**Attention !!!** le conteneur load est à lancer en one shot, il faudra trouver un moyen de persister les données de votre cluster .

voici l'arborescence de votre projet : 

```
excercice1
├── /api
│   ├── app.py
│   ├── run.py
│   ├── requirements_api.txt
│   └── Dockerfile
│
├── docker-compose-dev.yml
│
├── /load_address
│    ├── requirements_adresse.txt
│    ├── address.py
│    └── Dockerfile

``` 






### CI/CD – Pipeline GitHub Actions (à mettre en place)

Objectif: automatiser contrôle qualité + sécurité + construction et publication de l'image Docker de l'API.

CI (phase intégration) à exécuter sur chaque push / PR:
1. isort (ordre imports)
2. black (formatage)
3. flake8 (lint – doit échouer tant que le code n'est pas nettoyé)
4. bandit (analyse sécurité – échecs attendus: B105 mot de passe en dur, B307 eval, B602 shell=True)
5. pytest + couverture (pytest-cov) – un test échoue volontairement, à corriger
6. génération rapport coverage (coverage.xml)

CD (phase delivery) uniquement sur branche main ou tag version:
1. build image Docker multi-stage (API)
2. scan Docker Scout (fail si vulnérabilités high/critical)
3. push registry (Docker Hub) avec tags: latest + sha ou version tag

Secrets GitHub requis:
- DOCKER_USERNAME
- DOCKER_PASSWORD

Exigences:
- Corriger style/lint (imports, variables inutiles, wildcard import, longueur lignes)
- Supprimer / sécuriser endpoints ou patterns vulnérables (eval, mot de passe en dur, subprocess shell=True)
- Faire passer le test en ajustant assertion ou données
- Ajouter tests supplémentaires (404, health, auth_enabled True)
- Optimiser Dockerfile (taille, user non-root, cache)
- Ajouter badge de couverture (ex: via shields.io + action upload coverage)

Commandes locales utiles:
```
isort .
black .
flake8 .
bandit -r api
pytest -q --cov=api --cov-report=term
```

Critères de validation:
- Pipeline vert (CI) après corrections
- Image poussée avec deux tags
- Rapport coverage > 80% (objectif indicatif)
- Plus aucune alerte critique/high Docker Scout

Livrables:
- Fichier .github/workflows/ci-cd.yml
