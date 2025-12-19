FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir "fastapi==0.115.6" "uvicorn[standard]==0.32.1" \
  "SQLAlchemy==2.0.36" "asyncpg==0.30.0" "pydantic-settings==2.6.1"

# Copy the project into `/app/app`. The Dockerfile lives inside the project
# root for this repo, so use the current build context (`.`) instead of
# referring to a non-existent `app` subfolder.
COPY . /app/app

# Copy an entrypoint script that will run DB initialization before starting
# the application server.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
