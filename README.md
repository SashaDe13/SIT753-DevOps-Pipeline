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

Create a Pipeline from SCM and select this repository's Jenkinsfile.

## Evidence to capture
Use only evidence from your own run: full Jenkins stage view; build artefact/image; pytest and
coverage; SonarQube result; Bandit/Trivy result; staging health response; versioned production
release; and monitoring/dashboard/alert evidence.

The included Monitoring stage provides a container health check baseline. For the strongest match
to the assessment's top monitoring criterion, add a real monitoring/alerting platform and demonstrate
a meaningful alert in the video.
