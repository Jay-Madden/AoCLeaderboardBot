FROM python:3.8-slim-buster

COPY config.json /config.json

RUN apt-get update && apt-get upgrade -y

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN bash -c "source $HOME/.poetry/env"

RUN poetry install

# if "python main.py" is how you want to run your server
ENTRYPOINT ["python", "main.py"]