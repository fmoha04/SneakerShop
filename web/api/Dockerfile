FROM python:3.8.18

# Create work dir
WORKDIR /app

# Copy files
COPY web/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run flask
CMD ["python", "app.py"]
