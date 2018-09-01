FROM python:3-alpine
WORKDIR "/usr/src"
ADD requirements.txt .
ADD src/ .
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app.py"]
