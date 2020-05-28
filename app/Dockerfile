# Use Alpine as base
FROM python:alpine

# Image Labels
LABEL org.opencontainers.image.authors = "steven@thwaites.me.uk"
LABEL org.opencontainers.image.description = "A 'Hello, World.', args application."

# Install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# Expose the app on Flask default (5000)
EXPOSE 5000

# Run the application
CMD ["python3", "/usr/src/app/app.py"]
