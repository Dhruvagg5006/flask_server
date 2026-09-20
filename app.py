import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Application Metadata
APP_VERSION = os.environ.get("APP_VERSION", "2.0.0")
ENVIRONMENT = os.environ.get("FLASK_ENV", "production")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask CI/CD Deployment</title>
    <style>
        :root {
            --primary: #2563eb;
            --success: #16a34a;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 36px;
            max-width: 580px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 16px;
        }
        .badge {
            background-color: rgba(22, 163, 74, 0.2);
            color: var(--success);
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid var(--success);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .badge::before {
            content: "";
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
        }
        h1 {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }
        p.subtitle {
            color: var(--text-muted);
            margin-top: 6px;
            font-size: 14px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 24px 0;
        }
        .info-item {
            background-color: #0f172a;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        .info-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .info-value {
            font-size: 18px;
            font-weight: 600;
            color: #38bdf8;
        }
        .pipeline-steps {
            background: #0f172a;
            border-radius: 8px;
            padding: 16px;
            border: 1px solid var(--border);
            margin-top: 20px;
        }
        .pipeline-steps h3 {
            font-size: 14px;
            margin-bottom: 12px;
            color: var(--text-muted);
        }
        .step {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 13px;
        }
        .step-icon {
            color: var(--success);
            font-weight: bold;
        }
        footer {
            margin-top: 24px;
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Flask App CI/CD Demo</h1>
                <p class="subtitle">Automated Build, Test & Deployment to AWS EC2</p>
            </div>
            <span class="badge">Live & Healthy</span>
        </div>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Application Version</div>
                <div class="info-value">{{ version }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Environment</div>
                <div class="info-value">{{ environment }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Host Platform</div>
                <div class="info-value">AWS EC2</div>
            </div>
            <div class="info-item">
                <div class="info-label">Current Server Time</div>
                <div class="info-value" style="font-size: 14px; font-weight: normal; color: #cbd5e1;">{{ server_time }}</div>
            </div>
        </div>

        <div class="pipeline-steps">
            <h3>Automated Pipeline Workflow:</h3>
            <div class="step"><span class="step-icon">?</span> 1. Git Push trigger on <code>main</code> branch</div>
            <div class="step"><span class="step-icon">?</span> 2. GitHub Actions runner executes Pytest unit tests</div>
            <div class="step"><span class="step-icon">?</span> 3. Automated SSH handshake with EC2</div>
            <div class="step"><span class="step-icon">?</span> 4. Pull latest code & restart systemd Gunicorn daemon</div>
        </div>

        <footer>
            Project 6: Cloud & DevOps Demonstration
        </footer>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML_TEMPLATE,
        version=APP_VERSION,
        environment=ENVIRONMENT,
        server_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route("/health")
def health():
    """Health check endpoint used by CI/CD smoke tests and load balancers."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route("/api/info")
def api_info():
    """Information endpoint for testing API responses."""
    return jsonify({
        "project": "Flask CI/CD on AWS EC2",
        "description": "Automated deployment pipeline using GitHub Actions and AWS EC2",
        "status": "running"
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
