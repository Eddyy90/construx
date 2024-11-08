FROM python:3.12-bookworm as base

ENV PYTHONUNBUFFERED=1
ENV PRODUCTION=True
ENV Worker=False

RUN apt-get clean && apt-get update

RUN apt-get install -y --no-install-recommends locales
RUN apt install -y poppler-utils

# Cleanup
RUN apt-get clean
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/*

# Set Locale
RUN cat /etc/locale.gen | grep "# pt_BR.UTF-8" | cut -d ' ' -f2- >> /etc/locale.gen
RUN locale-gen
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

# APP
FROM base as app

# Python Requirements
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN rm -rf /var/tmp/*
RUN rm -rf /tmp/*

# SYSTEM
FROM app as daemon

WORKDIR /code
COPY . .
RUN rm -rf /code/media/*
RUN mkdir /var/log/construx
RUN python manage.py collectstatic --noinput
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]