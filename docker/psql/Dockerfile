FROM postgres:14-bullseye

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends awscli locales cron

# Set Locale
RUN cat /etc/locale.gen | grep "# pt_BR.UTF-8" | cut -d ' ' -f2- >> /etc/locale.gen
RUN locale-gen
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8


RUN mkdir /root/.aws
WORKDIR /root/.aws
COPY credentials credentials

RUN mkdir /scripts
WORKDIR /scripts
COPY backup.sh backup.sh
RUN chmod +x backup.sh

# Cleanup
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /var/tmp/*
RUN rm -rf /tmp/*

# Create a cron job to run the backup script every day at 12:00 AM
RUN crontab -l | { cat; echo "0 12 * * * bash /scripts/backup.sh"; } | crontab -
