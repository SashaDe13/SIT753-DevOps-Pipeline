# SIT753 7.3HD - Jenkins DevOps Pipeline

## Project
A Flask Task Management REST API with CRUD-style endpoints and a health endpoint.

## Local test
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v --cov=app --cov-report=xml
```

## Docker
```bash
docker build -t sit753-task-api:local .
docker run --rm -p 5000:5000 sit753-task-api:local
curl http://localhost:5000/health
```

## Jenkins prerequisites
Configure Git/Pipeline support, Docker access for the Jenkins agent, SonarQube + SonarScanner
(the Jenkins SonarQube installation name used by the Jenkinsfile is `SonarQube`), and internet
access for the Trivy image.

