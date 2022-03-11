FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY issue_minimum_response /issue_minimum_response

CMD ["python", "issue_minimum_response"]

