# hack_telekom_gigabit_challenge

Welcome to our submission for deutsche Tekekom hackathon 2024, specifically the Gigabit challenge.

The data persists in data/sqlite (added in the gitignore)
pip install -r requirements.txt
docker-compose up --build

TODO:

## Development

- create backend APIs
  - create the fill the SQLite database
  - create and fill the FAISS database
    - create "standard" implementations
    - find what tools to actually use
  - setup the service to generate the scripts

## Documentation

- create Requirements
- documents external dependacies
- create the actual README
  - setup docs
- create the Devpost
- create slides

## Requirements.txt

pandas
playwright
faiss-cpu
langchain-community
transformers
torch
httpx
sqlalchemy
fastapi
sqlmap-api
cryptography
requests
jwt
beautifulsoup4
owasp-zap-api

## Can be automated with Playwright:

_Broken Access Control (testing endpoints)_
_Identification and Authentication Failures_
_Security Misconfiguration_
_Vulnerable and Outdated Components (version checking)_
_XSS Testing_
_Some SQL Injection variants_

## Needs specialized packages

_sqlmap-api (SQL Injection)_
_cryptography (Crypto failures)_
_requests (API testing)_
_beautifulsoup4 (HTML parsing)_
_owasp-zap-api (For deeper scanning)_
