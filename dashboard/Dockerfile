FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN  mkdir ./pages
COPY ./pages ./pages

RUN mkdir ./streamlit
COPY ./.streamlit ./.streamlit

COPY charts.py .
COPY database.py .
COPY tracker.py .

EXPOSE 8501

CMD ["streamlit", "run", "tracker.py", "--server.port=8501"]
