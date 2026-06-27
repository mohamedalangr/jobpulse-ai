# Deployment Guide

This guide describes how to deploy **JobPulse AI** to a production Linux VPS (e.g., Ubuntu 24.04 on Hetzner or DigitalOcean) using Docker Compose and Nginx.

## Prerequisites

1. A clean Linux VM (Ubuntu 24.04 LTS recommended).
2. Root or `sudo` access.
3. A registered domain name pointing to your VM's public IP address (e.g., `jobpulse.yourdomain.com`).

## 1. System Setup

SSH into your server and install Docker and Git:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```
*Note: Log out and log back in to apply the docker group changes.*

## 2. Clone the Repository

```bash
git clone https://github.com/yourusername/jobpulse-ai.git
cd jobpulse-ai
```

## 3. Configuration

Copy the example environment variables and configure them:

```bash
cp .env.example .env
nano .env
```

Ensure the following variables are set for production:
```env
API_ENV=production
API_KEY=your_secure_random_key_here
POSTGRES_USER=jobpulse
POSTGRES_PASSWORD=your_secure_db_password
POSTGRES_DB=jobpulse
```

## 4. Run the Application

JobPulse AI uses a multi-container Docker Compose architecture. The `docker-compose.prod.yml` override applies memory limits and restart policies.

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

This will spin up:
- **postgres**: The relational database.
- **api**: FastAPI backend.
- **dashboard**: Streamlit frontend.
- **nginx**: Reverse proxy handling port 80 routing.

### Bootstrapping the Database
On the first run, the database migrations run automatically. However, you should ingest a seed dataset to populate the dashboards:

```bash
docker compose exec api python ops/scripts/seed_database.py
```
*(See RC-03 documentation for details on seeding the dataset).*

## 5. Enable HTTPS with Let's Encrypt

By default, Nginx is serving traffic on port 80. To secure your site with HTTPS, install Certbot on the host machine and configure it to proxy traffic to your Dockerized Nginx instance.

Stop the Nginx container temporarily or simply map a host-level Nginx to the internal Docker network. A robust approach is installing Nginx and Certbot on the host to act as the primary gateway:

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

# Create a host Nginx config
sudo nano /etc/nginx/sites-available/jobpulse
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name jobpulse.yourdomain.com;

    location / {
        # Proxy to the Docker Nginx container (port 80 exposed as 8080 or directly via Docker network)
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSockets for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable the site and run Certbot:
```bash
sudo ln -s /etc/nginx/sites-available/jobpulse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d jobpulse.yourdomain.com
```

Your deployment is now live, secure, and ready for use!
