FROM python:3
COPY ./app /etc/usr/src/app
WORKDIR /etc/usr/src/app
RUN pip install paho-mqtt requests pyyaml
ENTRYPOINT ["python3"]
CMD ["subscriptor.py"]