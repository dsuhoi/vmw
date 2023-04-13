FROM python:3.10-slim

WORKDIR /vmw

COPY *.py articles.db requirements.txt ./
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY tests/ ./tests/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]
