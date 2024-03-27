FROM python:3.9-slim

WORKDIR /usr/src/app

# TODO: Adjust layers to be more efficient
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
