import os

import uvicorn
from app import create_app
from uvicorn.config import LOGGING_CONFIG

if __name__ == "__main__":
    api_port = int(os.environ["API_PORT"])
    api_host = os.environ["API_HOST"]
    elastic_host = os.environ["ES_URL"]
    elastic_index = os.environ["ES_INDEX"]
    elastic_user = os.environ["ES_USERNAME"]
    elastic_pass = os.environ["ES_PASSWORD"]
    app = create_app(elastic_host, elastic_index, elastic_user, elastic_pass)
    print("run api ...")
    import subprocess

    subprocess.Popen(["echo", "secure shell call"], shell=False)
    # intentional for Bandit
    unused_var = "must remove"
    LOGGING_CONFIG["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host=api_host, port=api_port, workers=1)
