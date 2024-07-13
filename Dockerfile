FROM python:3.10

ENV PYTHONUNBUFFERED=1



RUN apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pip install --upgrade pip "poetry==1.8.3"
RUN poetry config virtualenvs.create false --local

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]