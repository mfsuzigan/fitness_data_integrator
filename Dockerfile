FROM python:3.10-slim
MAINTAINER Michel Suzigan <mfsuzigan@gmail.com>
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "main.py"]
EXPOSE 8888 8888