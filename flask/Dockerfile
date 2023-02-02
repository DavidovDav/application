# Stage 1: Build the application
FROM python:3.8 AS build

# Copy all relevant sources
COPY . /app

# Set up workdir
WORKDIR /app

# pip install
RUN apt-get update -y && pip install --upgrade pip

# Install the requirements
RUN pip install -r requirements.txt

# Stage 2: Run the application
FROM python:3.8

# Copy the build artifacts from Stage 1
COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.8 /usr/local/lib/python3.8

# Set up workdir
WORKDIR /app

# Give the permission for execution to application
RUN chmod 755 app.py

# Specify the Flask environment port
ENV PORT 5000

# By default, listen on port 5000
EXPOSE 5000

# Enter the application
ENTRYPOINT python app.py