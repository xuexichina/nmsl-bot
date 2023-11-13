FROM python:slim
WORKDIR /app
COPY requirements.txt .
COPY nmsl.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./tg_inline_bot ./tg_inline_bot
CMD ["python", "-m", "tg_inline_bot.__main__"]
