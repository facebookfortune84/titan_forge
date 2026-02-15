FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
# Copy the swarm directory as a top-level package
COPY ../swarm /app/swarm 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The entrypoint will be overridden by the docker-compose command,
# but this is good practice for a standalone image.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
