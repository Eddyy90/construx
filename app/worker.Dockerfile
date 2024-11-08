FROM python:3.12-bookworm as base

ENV PYTHONUNBUFFERED=1
ENV PRODUCTION=True
ENV Worker=True

RUN apt-get clean && apt-get update

RUN apt-get install -y --no-install-recommends locales
# Installs deps for PDF generation
RUN apt-get install -y --no-install-recommends \
    poppler-utils libpoppler-dev libpango-1.0-0 \
    wkhtmltopdf
    # libreoffice default-jre libreoffice-java-common \

# Libreoffice for file conversion
RUN apt install -y --no-install-recommends \
    libreoffice-base-nogui libreoffice-calc-nogui \
    libreoffice-draw-nogui libreoffice-impress-nogui \
    libreoffice-math-nogui libreoffice-writer-nogui

RUN apt install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config

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

# Cleanup
RUN rm -rf /var/tmp/*
RUN rm -rf /tmp/*

# WORKER
FROM app as worker

WORKDIR /code
COPY . .
RUN rm -rf /code/media/*
RUN mkdir /var/log/construx
CMD [ "celery", "--app", "construx.celery", "worker", "-l" , "info", "--beat", "--scheduler", "redbeat.RedBeatScheduler" ]