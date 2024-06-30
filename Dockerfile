FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
ARG VISITORS_PORT 9099
ENV VISITORS_PORT $VISITORS_PORT
ENV STATIC_DIR /var/www/alldata/spectacular/static
ENV DJANGO_SETTINGS_MODULE config.settings.production
ENV SECRET_KEY DummySecret
ENV DJANGO_ADMIN_URL admin/
ENV DJANGO_ALLOWED_HOSTS *
ENV DATABASE_URL=postgresql://dummy:dummy@dummy/dummy

# Install system dependencies and clean up in one layer
RUN useradd -m user && apt-get update && apt-get install -y curl nano procps apt-transport-https gunicorn nginx python-is-python3 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements/* /tmp/
RUN pip install --no-cache-dir -r /tmp/production.txt

# Set work directory
WORKDIR /code

# Copy your application code
COPY --chown=user . /code/
COPY --chown=user nginx/nginx.conf /etc/nginx/
COPY --chown=user nginx/dhparam.pem /code/
COPY --chown=user nginx/ssl-params.conf /etc/nginx/snippets/

# Expose the ports your application uses
EXPOSE 8443

# Create necessary directories and set permissions in one layer
RUN mkdir -p /var/www/alldata/spectacular/static /var/log/spectacular /var/spectacular/run /var/lib/nginx \
    && chown -R user:user /var/www/alldata /var/log/spectacular /var/spectacular/run /var/lib/nginx /code

# Set the user
USER user

# Collect each application static files into STATIC_ROOT folder
RUN python manage.py collectstatic --no-input --clear

# Mark directories with shared data
VOLUME /var/www/alldata
VOLUME /var/log/spectacular

# Command to run
ENTRYPOINT ["/code/entrypoint_visitors.sh"]
