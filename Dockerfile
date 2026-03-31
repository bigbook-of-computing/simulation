# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Build the documentation
RUN mkdocs build

# Expose port for dev server
EXPOSE 8000

# Default command to serve the site
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
