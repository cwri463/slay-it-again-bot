# Use official Python slim image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main bot script
CMD ["python", "bots/slayer/main.py"]
