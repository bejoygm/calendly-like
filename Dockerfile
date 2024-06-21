FROM python:3.9-slim

COPY . /app/

WORKDIR /app/

RUN pip install -U pip && pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]