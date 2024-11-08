#!/bin/bash
time=`date +%Y-%m-%d-%H-%M-%S`
pg_dump -h localhost -U "postgres" -Fc "postgres" > $time.dump
aws s3 cp $time.dump s3://construx-backup