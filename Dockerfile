FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repo into the container
COPY . .

# Set PYTHONPATH to include the root and the environment package
ENV PYTHONPATH=/app:/app/email_triage_env:$PYTHONPATH

# Expose the port (Hugging Face requirement)
EXPOSE 7860

# Command to run the FastAPI server binding to all interfaces on port 7860
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
