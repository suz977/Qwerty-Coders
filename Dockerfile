# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only what's needed
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script (not PDFs!)
COPY app/main.py .

# Create output directory inside container
RUN mkdir -p input_pdfs output

# Set default command
CMD ["python", "main.py"]
