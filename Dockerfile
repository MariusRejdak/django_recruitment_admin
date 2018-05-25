FROM python:3.6-alpine3.7

ENTRYPOINT ["/src/example/manage.py"]
CMD runserver 0.0.0.0:8000
WORKDIR /src/example
EXPOSE 8000

COPY . /src/
RUN pip install /src
