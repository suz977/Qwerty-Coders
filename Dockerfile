# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code and input folder
COPY app/ .

# Set default command
CMD ["python", "main.py"]
