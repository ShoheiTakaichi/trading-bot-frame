FROM python:3.10

RUN pip install --upgrade pip
RUN pip install git+https://github.com/ShoheiTakaichi/ccxws.git
RUN pip install loguru
RUN pip install jwt

WORKDIR /src
COPY . /src

CMD ["python", "test.py"]
