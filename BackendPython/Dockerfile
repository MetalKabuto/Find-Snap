FROM python:3.11

# Set the env and working directory according to Google Cloud

ENV PYTHONBUFFERED True
WORKDIR /app

# Copy the requirements file into the container at $APP_HOME
COPY . ./

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to build and run the Flask app using green unicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app