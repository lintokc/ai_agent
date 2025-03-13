FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV TOGETHER_AI_API_KEY=${TOGETHER_AI_API_KEY}
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
