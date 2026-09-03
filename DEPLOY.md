# FavvMenuz — Production Deployment Manual

This manual provides complete, step-by-step instructions for deploying **FavvMenuz** to a single **AWS Lightsail Linux instance** running Docker Compose and Caddy.

---

## 1. Deployment Architecture

The production environment runs on a single AWS Lightsail Linux VPS using Docker Compose. All components reside on the same host:

- **Frontend Container (`frontend`)**: Caddy v2 serving the pre-compiled React Single Page Application and proxying `/api/*`, `/admin/*`, and `/healthz` requests to Django. Handles automatic HTTPS certificate provisioning and renewal.
- **Backend Container (`backend`)**: Django 5.1 running under Gunicorn with 3 workers on internal port 8000.
- **Database Container (`db`)**: PostgreSQL 16 Alpine with a persistent named Docker volume (`postgres_prod_data`).
- **Cache Container (`redis`)**: Redis 7 Alpine on an internal bridge network (`internal_prod_net`).

### Architectural Trade-Offs
- **Simplicity & Low Cost**: Running the web app, database, and cache on a single $10–$20/month instance keeps operational complexity low.
- **No Multi-Region Redundancy**: This setup is tailored for portfolio demonstrations and hobby projects. It does not provide automated multi-host horizontal scaling or multi-region failover.

---

## 2. AWS Prerequisites

### A. Create an AWS Lightsail Instance
1. Log in to the [AWS Lightsail Console](https://lightsail.aws.amazon.com/).
2. Click **Create instance**.
3. Choose **Linux/Unix** as the platform.
4. Under blueprint, select **OS Only** → **Ubuntu 22.04 LTS** or **Ubuntu 24.04 LTS**.
5. Choose an instance plan: **2 GB RAM, 1 vCPU, 60 GB SSD** (recommended minimum for running Node builds and PostgreSQL).
6. Give your instance a name: e.g. `favvmenuz-production`.
7. Click **Create instance**.

### B. Attach a Static IP
1. In the Lightsail console, go to the **Networking** tab.
2. Click **Create static IP**.
3. Attach the static IP to your `favvmenuz-production` instance. Note down this public IP address.

### C. Configure Firewall Rules
In the **Networking** tab of your instance, configure open firewall ports:
- **Port 80 (HTTP)**: Open to `0.0.0.0/0` (required for Caddy ACME challenges).
- **Port 443 (HTTPS)**: Open to `0.0.0.0/0` (encrypted traffic).
- **Port 22 (SSH)**: Restrict to your developer IP address where practical, or open to trusted networks.
- **DO NOT open ports 5432 (PostgreSQL) or 6379 (Redis)** to the public internet.

### D. SSH Key Access
1. Download the default Lightsail private key (`.pem`) from the **Account** → **SSH keys** page, or upload your own public key.
2. Test SSH connectivity from your local workstation:
   ```bash
   ssh -i ~/.ssh/lightsail_key.pem ubuntu@<STATIC_IP>
   ```

---

## 3. Install Docker and Docker Compose on Server

Run the following commands on the Lightsail Ubuntu server to install official Docker packages:

```bash
# 1. Update existing packages
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install prerequisites
sudo apt-get install -y ca-certificates curl gnupg lsb-release git gzip

# 3. Add Docker official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Set up Docker repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install Docker Engine and Compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Enable Docker service and grant non-root permissions to ubuntu user
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# 7. Verify installations
docker --version
docker compose version
```

Log out and back in to apply group permissions:
```bash
exit
ssh -i ~/.ssh/lightsail_key.pem ubuntu@<STATIC_IP>
```

---

## 4. Prepare the Server

1. **Create the application directory:**
   ```bash
   sudo mkdir -p /opt/favvmenuz
   sudo chown -R ubuntu:ubuntu /opt/favvmenuz
   cd /opt/favvmenuz
   ```

2. **Clone the project repository:**
   ```bash
   git clone https://github.com/budhilnigam/FavvMenuz.git .
   ```

3. **Create the local backups directory:**
   ```bash
   mkdir -p /opt/favvmenuz/backups
   chmod 700 /opt/favvmenuz/backups
   ```

---

## 5. Configure Production Environment

Create the production `.env` file directly on the server:
```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Set the following production values:

```ini
# ==============================================================================
# FavvMenuz Production Configuration
# ==============================================================================

# 1. Django Settings
# Generate with: python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
DJANGO_SECRET_KEY=generate-a-strong-random-50-character-string-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,<STATIC_IP>,localhost,backend
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 2. Site / Caddy Address
# Use your domain to enable automatic Let's Encrypt TLS:
SITE_ADDRESS=https://yourdomain.com
# (If no domain is available yet, use ':80' for plain HTTP over static IP)

# 3. Cookie Security (True for HTTPS production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=False

# 4. PostgreSQL Configuration
POSTGRES_DB=favvmenuz_prod_db
POSTGRES_USER=favvmenuz_prod_user
POSTGRES_PASSWORD=use-a-strong-generated-password-here
POSTGRES_HOST=db
POSTGRES_PORT=5432

# 5. Redis Cache
REDIS_URL=redis://redis:6379/1

# 6. LLM / AI Configuration (Optional: Leave empty for fallback mode)
LLM_PROVIDER=openai-compatible
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
LLM_TIMEOUT_SECONDS=10.0

# 7. Throttling
SEARCH_RATE_LIMIT=60/minute
```

> **Security Guardrail:** Never commit `.env` to Git. Keep file permissions restricted to `600` (`chmod 600 .env`).

---

## 6. Manual Deployment Steps

Once `.env` is configured, start the stack:

1. **Build and start services using production Compose:**
   ```bash
   docker compose -f docker-compose.prod.yml build
   docker compose -f docker-compose.prod.yml up -d db redis
   ```

2. **Wait 10 seconds for the database to complete initialization, then run migrations:**
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend python manage.py migrate
   ```

3. **Collect Django static assets:**
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend python manage.py collectstatic --no-input
   ```

4. **Seed the synthetic restaurant and menu catalog:**
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend python manage.py seed_demo_data
   ```

5. **Create an administrative user:**
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend python manage.py createsuperuser
   ```

6. **Start all application containers:**
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

7. **Verify health check:**
   ```bash
   curl -I http://localhost/healthz/
   ```
   Should return `HTTP/1.1 200 OK` with JSON `{"status": "healthy"}`.

---

## 7. HTTPS and DNS Configuration

FavvMenuz uses Caddy to manage HTTPS certificates automatically through Let's Encrypt / ZeroSSL.

### If You Own a Custom Domain (e.g. `favvmenuz.com`):
1. Go to your DNS registrar (Namecheap, Cloudflare, Route53, GoDaddy).
2. Create an **A Record**:
   - **Host / Name**: `@` (or subdomain like `demo`)
   - **Value / Destination**: `<YOUR_LIGHTSAIL_STATIC_IP>`
   - **TTL**: 300 seconds (or auto)
3. Ensure ports 80 and 443 are open in your Lightsail firewall.
4. Set `SITE_ADDRESS=https://favvmenuz.com` in `/opt/favvmenuz/.env`.
5. Restart Caddy:
   ```bash
   docker compose -f docker-compose.prod.yml restart frontend
   ```
   Caddy automatically completes the ACME HTTP-01 challenge and provisions valid TLS certificates.

### If You Do Not Own a Domain (IP Only):
1. In `.env`, set:
   ```ini
   SITE_ADDRESS=:80
   SESSION_COOKIE_SECURE=False
   CSRF_COOKIE_SECURE=False
   ```
2. Restart services:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```
3. Access your application via `http://<YOUR_STATIC_IP>`.

---

## 8. GitHub Actions Automated CI/CD Deployment

The repository includes a production workflow in `.github/workflows/ci-cd.yml` that runs automated tests and deploys directly to Lightsail on push to `main`.

### A. Generate Deployment SSH Key Pair
On your workstation or server:
```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/favvmenuz_deploy
```

Add the public key (`~/.ssh/favvmenuz_deploy.pub`) to `~/.ssh/authorized_keys` on your Lightsail instance:
```bash
cat ~/.ssh/favvmenuz_deploy.pub | ssh -i ~/.ssh/lightsail_key.pem ubuntu@<STATIC_IP> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### B. Obtain Server Known Hosts String
Run locally:
```bash
ssh-keyscan -H <STATIC_IP>
```
Copy the output line.

### C. Configure GitHub Secrets
In your GitHub repository, navigate to **Settings** → **Secrets and variables** → **Actions**, and add the following repository secrets:

| Secret Name | Value |
| :--- | :--- |
| `LIGHTSAIL_HOST` | Your Lightsail static public IP address |
| `SSH_USERNAME` | `ubuntu` |
| `SSH_PRIVATE_KEY` | Contents of `~/.ssh/favvmenuz_deploy` (including `BEGIN` and `END` headers) |
| `SSH_KNOWN_HOSTS` | Output from `ssh-keyscan -H <STATIC_IP>` |

### D. Deployment Trigger
Whenever code is merged into `main`, GitHub Actions:
1. Runs Django system checks and backend unit tests against PostgreSQL & Redis.
2. Validates frontend TypeScript types and builds the production bundle.
3. Builds Docker images to ensure container sanity.
4. Connects via SSH to Lightsail, pulls the latest code, runs migrations, collectstatic, idempotent seed, and performs a live health check.

---

## 9. Operations & Maintenance

### Checking Status
```bash
cd /opt/favvmenuz
docker compose -f docker-compose.prod.yml ps
```

### Viewing Logs
```bash
# Tail all container logs:
docker compose -f docker-compose.prod.yml logs -f

# View backend API logs:
docker compose -f docker-compose.prod.yml logs -f backend

# View Caddy web server logs:
docker compose -f docker-compose.prod.yml logs -f frontend
```

### Restarting Containers
```bash
docker compose -f docker-compose.prod.yml restart
```

### Applying New Migrations Manually
```bash
docker compose -f docker-compose.prod.yml run --rm backend python manage.py migrate
```

### Reseeding Demo Catalog
```bash
docker compose -f docker-compose.prod.yml run --rm backend python manage.py seed_demo_data --reset
```

### Creating Database Backups
Run the provided backup script:
```bash
bash scripts/backup_db.sh
```
Dumps are created inside `/opt/favvmenuz/backups/favvmenuz_backup_<timestamp>.sql.gz`.

### Restoring a Database Dump
```bash
bash scripts/restore_db.sh backups/favvmenuz_backup_YYYYMMDD_HHMMSS.sql.gz
```
Requires confirmation (`yes`) before overwriting.

---

## 10. Cost and Operational Notes

- **AWS Lightsail Instance**: Standard 2 GB RAM / 1 vCPU instances cost approximately $10 to $20/month.
- **Static IP**: AWS Lightsail provides 1 static IP address attached to a running instance at no additional charge.
- **LLM API Usage**: Outbound calls to OpenAI or other providers are billed by token consumption. The app defaults to deterministic rule-based fallback when `LLM_API_KEY` is not provided.
- **Resource Decommissioning**: When the demo is no longer needed, remember to delete the Lightsail instance and release the static IP in the AWS console to stop recurring charges.
