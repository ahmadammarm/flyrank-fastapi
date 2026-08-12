# Stage 1: Builder
FROM python:3.10-alpine as builder

WORKDIR /app

# Install build dependencies required for some Python packages (like psycopg2) on Alpine
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Create a virtual environment so we can easily copy all dependencies to the final stage
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.10-alpine

WORKDIR /app

# Install runtime dependencies required by psycopg2
RUN apk add --no-cache libpq

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure the virtual environment is in the PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
