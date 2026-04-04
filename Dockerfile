FROM python:3.10-slim 
 
 WORKDIR /app 
 
 # Copy root requirements (ensure all dependencies including uvicorn/fastapi are here) 
 COPY requirements.txt . 
 RUN pip install --no-cache-dir -r requirements.txt 
 
 # Copy the rest of the repository 
 COPY . . 
 
 # Set PYTHONPATH to the root so Python can find your folders 
 ENV PYTHONPATH=/app:$PYTHONPATH 
 
 # Expose the port (Hugging Face requirement) 
 EXPOSE 7860 
 
 # Run the app (Assuming app.py is in the root 'server' folder) 
 CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
