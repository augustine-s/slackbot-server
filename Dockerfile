FROM python:3.10

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt


CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
