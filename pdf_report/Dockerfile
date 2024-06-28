FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY queries.py .
COPY charts.py .
COPY styles.css .
COPY generate_pdf.py .
COPY mailer.py .
COPY pdf_report.py .

CMD [ "pdf_report.main" ]