# backend API with FastAPI
Python version - 3.12.3
## get started: for devs
1. spin up a virtual environment in `/backend/`. we're using `virtualenv`.
>[!WARNING]
>instructions below assume that your working directory is `/backend/`
```bash
virtualenv venv
source venv/bin/activate
```
2. install dependencies
```bash
pip3 install -r requirements.txt
```
3. setup PostgreSQL database

4. run the backend application using fastapi cli
```bash
fastapi dev app/main.py
```
happy coding!
