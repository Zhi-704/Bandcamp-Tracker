FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN  mkdir ./pages

COPY ./pages ./pages

COPY charts.py .
COPY database.py .
COPY tracker.py .

CMD [ "pipeline.main" ]