FROM python:3.8
ENV TZ="Europe/Amsterdam"

ADD pip.conf /etc/pip.conf

ADD requirements*.txt /
RUN pip install -r /requirements.txt

ADD *.py /
ADD instance /instance

ADD application /application
ADD .pylintrc /

ADD tests /tests

## Run pylint and tests
RUN pip install pylint && pylint entrypoint.py application/ && pip uninstall -y pylint
RUN pip install -r /requirements-test.txt && pytest --cov=application/ tests/ && pip uninstall -y -r /requirements-test.txt

EXPOSE 8080

ENV FLASK_ENV="production"

ENTRYPOINT [ "python", "entrypoint.py"]
