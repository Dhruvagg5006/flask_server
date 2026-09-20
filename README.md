# Project 6: CI/CD Pipeline for a Flask Application on AWS EC2

An end-to-end automated Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Python Flask web application deployed to an Amazon Web Services (AWS) EC2 instance.

---

## ?? Project Overview

This project demonstrates a production-grade automated DevOps pipeline:
1. **Source Code Change**: A developer pushes new code or updates to the GitHub repository `main` branch.
2. **Continuous Integration (CI)**: GitHub Actions runner automatically checks out the code, configures the Python environment, installs dependencies, and runs automated unit tests with Pytest.
3. **Quality Gate**: If any unit test fails, the pipeline immediately halts and prevents broken code from being deployed.
4. **Continuous Deployment (CD)**: Upon test success, GitHub Actions securely establishes an SSH connection with the AWS EC2 instance, fetches the latest commits, updates Python virtual environment packages, and restarts the systemd application service with zero downtime.
5. **Live Verification**: The live EC2 application reflects the updates instantly at `http://<EC2-PUBLIC-IP>:5000`.

```
               ??????????????????????????????????????????????????????????
               ?                  DEVELOPER WORKSTATION                 ?
               ?         git commit -m "update" && git push             ?
               ??????????????????????????????????????????????????????????
                                           ?
                                           ?
               ??????????????????????????????????????????????????????????
               ?                  GITHUB REPOSITORY                     ?
               ?               Trigger: Push to `main`                  ?
               ??????????????????????????????????????????????????????????
                                           ?
                                           ?
???????????????????????????????????????????????????????????????????????????????????????????
?                           GITHUB ACTIONS CI/CD PIPELINE                                 ?
?                                                                                         ?
?   ?????????????????????????????????????       ???????????????????????????????????????   ?
?   ?   STAGE 1: Build & Test (CI)      ?       ?   STAGE 2: Deploy to EC2 (CD)       ?   ?
?   ?   - Setup Python 3.11             ? ????? ?   - Authenticate via SSH Key        ?   ?
?   ?   - Install dependencies          ? (Pass)?   - Pull latest git commit on EC2   ?   ?
?   ?   - Run Pytest unit tests         ?       ?   - Update venv & restart systemd   ?   ?
?   ?????????????????????????????????????       ???????????????????????????????????????   ?
???????????????????????????????????????????????????????????????????????????????????????????
                                                                   ? SSH (Port 22)
                                                                   ?
                                        ???????????????????????????????????????????????????
                                        ?               AWS EC2 INSTANCE                  ?
                                        ?       (Ubuntu Server Free Tier t2.micro)        ?
                                        ?                                                 ?
                                        ?   - App Directory: ~/flask-cicd-ec2             ?
                                        ?   - Service: flaskapp.service (Systemd)         ?
                                        ?   - WSGI Server: Gunicorn (3 workers)           ?
                                        ?   - Port: 5000 (accessible via Public IP)       ?
                                        ???????????????????????????????????????????????????
```

---

## ?? Repository Structure

```
flask-cicd-ec2/
??? app.py                      # Flask web application with health & version routes
??? test_app.py                 # Pytest & unittest test cases (quality gate)
??? requirements.txt            # Python dependencies (Flask, Gunicorn, Pytest)
??? .gitignore                  # Git ignore rules for virtual environments & cache
??? .github/
?   ??? workflows/
?       ??? deploy.yml          # GitHub Actions automated workflow specification
??? ec2-setup/
?   ??? flaskapp.service        # Systemd unit file for running Gunicorn on boot
?   ??? setup.sh                # One-click EC2 server initialization script
?   ??? deploy.sh               # Server-side update & restart script
??? README.md                   # Complete implementation and demonstration guide
```

---

## ??? Step-by-Step Guide for AWS & GitHub Setup

### Step 1: Launch an AWS EC2 Instance (Free Tier)

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Navigate to **EC2** and click **Launch Instance**.
3. Configure the instance settings:
   - **Name**: `flask-cicd-server`
   - **Application and OS Images (AMI)**: Select **Ubuntu** (Choose *Ubuntu Server 24.04 LTS* or *22.04 LTS*, Free Tier eligible).
   - **Instance Type**: Select `t2.micro` (or `t3.micro` depending on region, Free Tier eligible).
   - **Key Pair**: Click **Create new key pair**:
     - Key pair name: `flask-ec2-key`
     - Key pair type: `RSA`
     - Private key file format: `.pem` (for OpenSSH)
     - Click **Create key pair** (Save the downloaded `flask-ec2-key.pem` file securely on your computer).
4. **Network Settings (Firewall / Security Group)**:
   - Select **Create security group**.
   - Check **Allow SSH traffic from** -> Select **Anywhere (0.0.0.0/0)** (or My IP).
   - Click **Add security group rule**:
     - **Type**: Custom TCP
     - **Port Range**: `5000`
     - **Source**: `Anywhere (0.0.0.0/0)`
     - **Description**: Allow inbound Flask traffic.
5. Click **Launch Instance**.
6. Wait for the instance state to change to **Running** and copy the **Public IPv4 address** (e.g. `54.210.45.120`).

---

### Step 2: Initialize the GitHub Repository

1. On your local machine or terminal, navigate to this project folder:
   ```bash
   cd flask-cicd-ec2
   ```
2. Initialize git, commit all files, and push to your GitHub account:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Flask app and CI/CD workflow"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

---

### Step 3: Configure EC2 Instance (One-Time Setup)

1. Connect to your EC2 instance from your terminal (PowerShell, Command Prompt, or Bash):
   ```bash
   # On Windows PowerShell or Linux/macOS
   ssh -i "flask-ec2-key.pem" ubuntu@<YOUR-EC2-PUBLIC-IP>
   ```
   *(If prompted "Are you sure you want to continue connecting?", type `yes` and press Enter).*

2. On the EC2 terminal, clone your GitHub repository into `/home/ubuntu/flask-cicd-ec2`:
   ```bash
   git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git /home/ubuntu/flask-cicd-ec2
   ```

3. Run the automated initialization script:
   ```bash
   chmod +x /home/ubuntu/flask-cicd-ec2/ec2-setup/setup.sh
   /home/ubuntu/flask-cicd-ec2/ec2-setup/setup.sh
   ```

   **What `setup.sh` does automatically:**
   - Installs Python 3, `python3-venv`, `pip`, and `git`.
   - Creates a dedicated virtual environment in `/home/ubuntu/flask-cicd-ec2/venv`.
   - Installs dependencies from `requirements.txt`.
   - Registers and starts the `flaskapp.service` systemd service.

4. Open your web browser and navigate to:
   ```
   http://<YOUR-EC2-PUBLIC-IP>:5000
   ```
   You should see the **Flask App CI/CD Demo** web page displaying version `1.0.0` and status `Live & Healthy`!

---

### Step 4: Configure GitHub Actions Secrets

To allow GitHub Actions to securely deploy to your EC2 instance, add 3 repository secrets:

1. In your GitHub repository, navigate to **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret** for each of the following:

| Secret Name | Value Description | Example Value |
| :--- | :--- | :--- |
| `EC2_HOST` | The Public IPv4 address or Public DNS of your EC2 instance | `54.210.45.120` |
| `EC2_USER` | The default SSH username for Ubuntu instances | `ubuntu` |
| `EC2_SSH_KEY` | The **entire contents** of your downloaded `flask-ec2-key.pem` file | Include `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` |

> [!TIP]
> To copy the exact contents of your `.pem` key:
> - On Windows (PowerShell): `Get-Content .lask-ec2-key.pem | Set-Clipboard`
> - On Linux / macOS: `cat flask-ec2-key.pem | pbcopy` (or `xclip`)

---

## ?? Step 5: Demonstration & Verification Workflow

This section outlines how students can demonstrate automated CI/CD for course evaluation:

### Demonstration 1: Automated Build, Test, and Deployment on Push

1. Open `app.py` in your code editor and modify the application version:
   ```python
   APP_VERSION = os.environ.get("APP_VERSION", "2.0.0")
   ```
2. Commit and push the change to GitHub:
   ```bash
   git add app.py
   git commit -m "Feature: Bump application version to 2.0.0"
   git push origin main
   ```
3. Open GitHub in your browser and click on the **Actions** tab:
   - You will see a new workflow run triggered by your commit.
   - Click on the workflow to observe the two pipeline stages:
     - **Stage 1: Build & Test (CI)**: Checks out code, installs dependencies, and runs `pytest` (shows all 4 tests passing).
     - **Stage 2: Deploy to AWS EC2 (CD)**: Connects to EC2 via SSH, pulls the latest commit, and restarts `flaskapp.service`.
4. Refresh your browser at `http://<YOUR-EC2-PUBLIC-IP>:5000`:
   - Notice that the version now immediately shows **2.0.0** without any manual SSH or terminal commands!

---

### Demonstration 2: Quality Gate Demonstration (Preventing Broken Deployments)

An essential part of CI/CD is demonstrating that failing tests block deployment:

1. Open `test_app.py` and modify an assertion to fail intentionally:
   ```python
   def test_health_endpoint(self):
       response = self.client.get("/health")
       self.assertEqual(response.status_code, 500) # Intentionally wrong!
   ```
2. Commit and push:
   ```bash
   git add test_app.py
   git commit -m "Test: Intentionally introduce failing test"
   git push origin main
   ```
3. Check the **Actions** tab:
   - **Stage 1 (Build & Test)** will fail with a red cross (?).
   - **Stage 2 (Deploy to EC2)** will be automatically **cancelled/skipped**.
4. Refresh `http://<YOUR-EC2-PUBLIC-IP>:5000`:
   - The production server remains completely unaffected and healthy!
5. Revert the test back to `200`, commit, push, and observe the pipeline turn green again.

---

## ?? Useful Commands & Troubleshooting

### On the EC2 Server
- **Check application logs in real time**:
  ```bash
  sudo journalctl -u flaskapp -f
  ```
- **Check service status**:
  ```bash
  sudo systemctl status flaskapp
  ```
- **Manually restart the service**:
  ```bash
  sudo systemctl restart flaskapp
  ```

### Common Issues & Fixes
- **Cannot access `http://<EC2-PUBLIC-IP>:5000` in browser**:
  - Verify your EC2 Security Group has an Inbound Rule allowing **Custom TCP port 5000** from source `0.0.0.0/0`.
  - Make sure you are using `http://` and **not** `https://`.
- **GitHub Actions Deploy Stage times out / SSH connection refused**:
  - Verify that `EC2_HOST` contains the exact current public IP of your EC2 instance (note: restarting an EC2 instance without an Elastic IP assigns a new public IP).
  - Verify that `EC2_SSH_KEY` secret contains the complete `.pem` text with no missing lines.
- **Git permissions error during pull**:
  - Run `git config --global --add safe.directory /home/ubuntu/flask-cicd-ec2` on the EC2 instance.
