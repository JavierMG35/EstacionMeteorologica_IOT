FROM python:3.11-slim-bullseye
COPY ./app /etc/usr/src/app
WORKDIR /etc/usr/src/app
RUN pip install mysql-connector-python Flask Flask-Cors pyyaml
ENTRYPOINT ["python3"]
CMD ["api.py"]
