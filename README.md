# CamGateway
All integration for backend with fridgecamera 2 will be incorporated here
Also all code related to ML pipeline initiation will be included here
Includes;
  - ML Gateway - Quality checks/conditions/ data passing to pipeline
  - Device states APi
  - Websocket integrations
Running on chefling Kubernetes cluster  
Refer [ML DataFlow - Implementation Plan for details](https://smarteram.atlassian.net/wiki/spaces/MD/pages/4209311786/Implementation+plan+ML+Integration)
  
## Functionalities
API Server that
- Accept ml processing jobs from IOT Core and initiate ml preprocessing step (  /job/new endpoint)
- Accept pre processed image from ML - preprocessing step and push the result to mobile client
- Save job details in Mysql data base
- Provide job status/history for ml jobs that were already run

## Setup

```bash
pip install poetry
poetry shell
python app.py [-p PORT]
```

## TODO

- [X] Choose Framework/server combo: uvicorn/fastapi
- [X] Write mockup for endpoints
- [X] Choose Docker Image
- [X] Structured logging
- [X] Add Config Class(dev/stage/prod) - pydantic-settings
- [X] Disable swagger for prod
- [X] Add linting/formatting framework locally and then in CI: locally done
- [X] Add JWT Authentication
- [X] Add model classes
- [X] Deploy with Jenkins in kubernetes: Jenkinsfile created. Building pipeline in jenkins is left
- [X] Integrate Shivam's code in API server
- [X] Integrate With DB - ml_jobs
- [X] Integrate with Queue (Choose a queue as well)
- [ ] Integrate with socketconnect
- [ ] Write unit tests
- [ ] HTTPIE based mocked API sanity tests into CI
- [ ] Stresstesting scripts with API data mocking 

## References
https://github.com/tiangolo/uwsgi-nginx-flask-docker  
https://github.com/dmontagu/fastapi-utils ```pip install fastapi-utils```  
https://github.com/zhanymkanov/fastapi-best-practices -> https://github.com/zhanymkanov/fastapi_production_template  
