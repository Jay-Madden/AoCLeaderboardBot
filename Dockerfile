FROM python:3.8-slim-buster

COPY config.json /config.json

WORKDIR /Bot
ADD . /Bot

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

RUN poetry install

# if "python main.py" is how you want to run your server
ENTRYPOINT ["python", "main.py"]