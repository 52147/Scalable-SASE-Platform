# Scalable SASE Platform

This is a scalable SASE (Secure Access Service Edge) platform built with Django, configured for load balancing using NGINX and connection pooling using pgBouncer.

## Prerequisites

- Python 3.x
- PostgreSQL
- Redis
- Homebrew (for macOS)
- NGINX
- pgBouncer

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd scalable-sase-platform
```

### Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Setup

1. **Start PostgreSQL**:

   For macOS:
   ```bash
   brew services start postgresql
   ```

2. **Create Databases and Users**:

   Log into PostgreSQL and create the necessary databases and users.

   ```bash
   psql -h localhost -U postgres
   ```

   Inside the PostgreSQL prompt, run:

   ```sql
   CREATE DATABASE sase_db;
   CREATE DATABASE sase_db_shard_1;
   CREATE DATABASE sase_db_shard_2;

   CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sase_db TO your_username;
   GRANT ALL PRIVILEGES ON DATABASE sase_db_shard_1 TO your_username;
   GRANT ALL PRIVILEGES ON DATABASE sase_db_shard_2 TO your_username;
   ```

### Apply Migrations

```bash
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Start Django Development Servers

Start multiple instances of your Django application:

**Terminal 1:**
```bash
python manage.py runserver 127.0.0.1:8001
```

**Terminal 2:**
```bash
python manage.py runserver 127.0.0.1:8002
```

## NGINX Configuration

### Install NGINX

For macOS:
```bash
brew install nginx
```

### Configure NGINX

Create or edit the NGINX configuration file at `/usr/local/etc/nginx/nginx.conf`:

```nginx
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    upstream django {
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

### Start NGINX

```bash
sudo nginx -c /usr/local/etc/nginx/nginx.conf
```

## pgBouncer Configuration

### Install pgBouncer

For macOS:
```bash
brew install pgbouncer
```

### Configure pgBouncer

Create the configuration file at `/usr/local/etc/pgbouncer/pgbouncer.ini`:

```ini
[databases]
sase_db = host=localhost dbname=sase_db

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = md5
auth_file = /usr/local/etc/pgbouncer/userlist.txt
pool_mode = session
max_client_conn = 100
default_pool_size = 20
```

Create the userlist file at `/usr/local/etc/pgbouncer/userlist.txt`:

```plaintext
"your_username" "your_password"
```

### Start pgBouncer

Create a LaunchDaemon for pgBouncer at `/Library/LaunchDaemons/com.pgbouncer.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pgbouncer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/pgbouncer</string>
        <string>/usr/local/etc/pgbouncer/pgbouncer.ini</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/pgbouncer.log</string>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/pgbouncer.log</string>
</dict>
</plist>
```

Load the LaunchDaemon to start pgBouncer:

```bash
sudo launchctl load /Library/LaunchDaemons/com.pgbouncer.plist
```

## Django Settings for pgBouncer

Update your Django `settings.py` to connect to the database through pgBouncer:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sase_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '6432',  # pgBouncer port
    },
    'shard_1': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sase_db_shard_1',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '6432',  # pgBouncer port
    },
    'shard_2': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sase_db_shard_2',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '6432',  # pgBouncer port
    },
}
```

## Access the Application

- Open your browser and navigate to `http://localhost` to access the application through NGINX load balancer.
- Access the Django admin interface at `http://localhost/admin/` and log in with the superuser credentials you created.

## Additional Notes

- **SSL/TLS Configuration:** For secure communication, consider setting up SSL/TLS with Let's Encrypt.
- **Monitoring and Logging:** Set up monitoring tools like Prometheus and Grafana to track the performance and health of your application and infrastructure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
