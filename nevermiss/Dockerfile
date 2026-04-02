FROM python:3.11-slim

WORKDIR /app

RUN pip install flask requests

COPY twilio_handler.py .

ENV TWILIO_ACCOUNT_SID=
ENV TWILIO_AUTH_TOKEN=
ENV TWILIO_PHONE_NUMBER=
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "twilio_handler.py"]