# Production Deployment Guide

## Prerequisites

1. A Linux server (Ubuntu 20.04+ recommended)
2. Docker and Docker Compose installed
3. Domain name (optional but recommended)
4. SSL certificate (Let's Encrypt recommended)

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gemini-http-server.git
cd gemini-http-server
```

### 2. Configure Environment Variables

Create a `.env` file based on the example:

```bash
cp examples/.env.example .env
```

Edit the `.env` file with your production settings:

```bash
# .env
HOST=0.0.0.0
PORT=8000
DEV_MODE=False
SECRET_KEY=your-very-secure-secret-key-here
```

### 3. Build and Run with Docker Compose

```bash
docker-compose up -d
```

### 4. Set Up Reverse Proxy (Nginx)

Create an Nginx configuration file:

```nginx
# /etc/nginx/sites-available/gemini-server
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/gemini-server /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL Certificate with Let's Encrypt

```bash
sudo certbot --nginx -d your-domain.com
```

### 6. Monitoring and Maintenance

Check logs:

```bash
docker-compose logs -f
```

Update the server:

```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Scaling Considerations

For high-traffic applications, consider:

1. Using a production-grade WSGI server like Gunicorn
2. Adding a load balancer
3. Using a CDN for static assets
4. Implementing database persistence
5. Setting up automated backups