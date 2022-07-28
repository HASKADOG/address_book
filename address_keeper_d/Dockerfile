FROM python:3.10
WORKDIR /address_keeper

RUN python -m pip install pipenv
COPY . .
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["gunicorn", "address_keeper.wsgi:application", "--bind", "0.0.0.0:8000"]