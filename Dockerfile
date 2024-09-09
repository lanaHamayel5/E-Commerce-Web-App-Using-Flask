# Use the official Python image, slim version (smaller and lightweight)
FROM python:3.9-slim 

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required Python packages without using cache to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . .

# Expose port 5000 for the Flask application to be accessible
EXPOSE 5000

# Set the environment variable to tell Flask which app to run (app.py)
ENV FLASK_APP=app.py

# Command to start the Flask application, accessible on all network interfaces (0.0.0.0)
CMD ["flask", "run", "--host=0.0.0.0"]
