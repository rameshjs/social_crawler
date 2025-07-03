FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting application with uvicorn..."\n\
exec uvicorn main:app --host 0.0.0.0 --port 8000' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
