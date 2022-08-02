FROM python:3.10
WORKDIR /address_keeper

RUN python -m pip install pipenv

COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

COPY ./address_keeper_d/entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]

