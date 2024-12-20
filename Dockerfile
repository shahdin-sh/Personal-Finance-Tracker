FROM python:3.12.6

# Create a non-root user and group named 'none-root-shahdin'
RUN groupadd -r nonroot-shahdin && useradd -r -g nonroot-shahdin nonroot-shahdin

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Change ownership of the code directory to the non-root user 'none-root-shahdin'
RUN chown -R nonroot-shahdin:nonroot-shahdin /app

# Switch to the non-root user
USER nonroot-shahdin

# Expose port 8000 (Django default)
EXPOSE 8000

# Command to run the Django development server
ENTRYPOINT [ "python", "manage.py" ]
CMD ["runserver", "0.0.0.0:8000"]