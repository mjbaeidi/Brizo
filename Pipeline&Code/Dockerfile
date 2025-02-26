# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final stage
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the virtual environment and application code from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Set the environment variables
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]