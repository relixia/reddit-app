# Use the official Python image as the base image
FROM python:3.9.6

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and other necessary files
COPY . .

# Expose the port that the Flask app will be listening on
EXPOSE 5000

# Set the environment variables
ENV FLASK_APP=den.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app when the container launches
CMD ["flask", "run"]
