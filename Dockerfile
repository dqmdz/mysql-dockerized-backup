FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk update
RUN apk add --no-cache curl
RUN apk add mysql-client bash
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x app/backup.sh

EXPOSE 5000

CMD ["flask", "--app", "app.app", "run", "--host", "0.0.0.0", "--port", "5000"]