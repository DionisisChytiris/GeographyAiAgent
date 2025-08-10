FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy app code
COPY api/ ./api/

# Expose port
EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Start FastAPI with uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]