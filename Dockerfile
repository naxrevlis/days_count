FROM python:3.10.5-slim

ENV PIP_NO_CACHE_DIR=True
ENV POETRY_VIRTUALENVS_CREATE=False

RUN apt-get update
RUN apt install -y \
gcc g++ python-dev librocksdb-dev build-essential \
libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev \
liblz4-dev libzstd-dev curl

RUN pip install -U \
    pip \
    setuptools \
    wheel \
    poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev && rm -rf ~/.cache/pypoetry/{cache,artifacts}

COPY ./days_count /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

CMD poetry run python main.py