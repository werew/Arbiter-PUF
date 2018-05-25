FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY images /usr/src/app/images/
COPY app.py /usr/src/app/

EXPOSE 5000
CMD [ "python", "./app.py" ]
