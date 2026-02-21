FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port
EXPOSE 16000

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=16000", "--server.headless=true"]