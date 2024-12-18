FROM python:3.11-slim

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


COPY . /code/

WORKDIR /code


CMD ["python", "app/main.py"]