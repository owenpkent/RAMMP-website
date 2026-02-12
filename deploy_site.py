#!/usr/bin/env python3
"""
Deploy RAMMP Website to Cloudflare Pages with Password Protection

Wraps all HTML files with password protection and deploys to Cloudflare Pages.

Usage:
    python deploy_site.py              # Deploy to Cloudflare Pages
    python deploy_site.py --no-open    # Deploy without opening browser
    python deploy_site.py --local-only # Generate protected files only, no deploy

Setup:
    1. Install Wrangler: npm install -g wrangler
    2. Login: wrangler login
    3. Create .env file with:
       DASHBOARD_PASSWORD=your-password
       CLOUDFLARE_ACCOUNT_ID=your-account-id
       CLOUDFLARE_PROJECT_NAME=rammp-website
"""

import os
import sys
import shutil
import hashlib
import tempfile
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# Files/folders to include in deployment
INCLUDE_FILES = ['index.html', 'people.html', 'what-is-rammp.html', 'publications.html', 'contact.html', 'progress.html']
INCLUDE_DIRS = ['assets', 'dist']

# Password wrapper template - injected into each HTML file
PASSWORD_WRAPPER = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAMMP - Protected Preview</title>
    <link rel="icon" type="image/png" href="assets/images/RAMMP Logo favicon.png">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a365d 0%, #22a9ff 100%);
            color: #e6e6e6;
            min-height: 100vh;
        }
        .login-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, #1a365d 0%, #22a9ff 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }
        .login-overlay.hidden { display: none; }
        .login-box {
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            max-width: 380px;
            width: 90%;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .login-box h1 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: #1a365d;
        }
        .login-box .subtitle {
            color: #666;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
        .login-box input {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #f9f9f9;
            color: #333;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }
        .login-box input:focus { border-color: #22a9ff; }
        .login-box button {
            width: 100%;
            padding: 0.875rem;
            margin-top: 1rem;
            background: linear-gradient(135deg, #22a9ff, #1a365d);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: transform 0.1s, box-shadow 0.2s;
        }
        .login-box button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(34, 169, 255, 0.4);
        }
        .login-box button:active { transform: translateY(0); }
        .error {
            color: #e53e3e;
            margin-top: 1rem;
            font-size: 0.9rem;
            display: none;
        }
        .error.visible { display: block; }
        .logo { max-width: 200px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="login-overlay" id="loginOverlay">
        <div class="login-box">
            <img src="assets/images/rammp-logo-transparent.png" alt="RAMMP" class="logo">
            <h1>Preview Access</h1>
            <p class="subtitle">Enter password to view the website mockup</p>
            <input type="password" id="passwordInput" placeholder="Password" autofocus
                   onkeypress="if(event.key==='Enter')checkPassword()">
            <button onclick="checkPassword()">Enter</button>
            <p class="error" id="errorMsg">Incorrect password</p>
        </div>
    </div>
    
    <div id="siteContent" style="display: none;">
        %%SITE_CONTENT%%
    </div>

    <script>
        const PASSWORD_HASH = '%%PASSWORD_HASH%%';
        
        // Check session storage for existing auth
        if (sessionStorage.getItem('rammp_preview_auth') === PASSWORD_HASH) {
            showSite();
        }
        
        async function sha256(message) {
            const msgBuffer = new TextEncoder().encode(message);
            const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        }
        
        async function checkPassword() {
            const input = document.getElementById('passwordInput').value;
            const hash = await sha256(input);
            
            if (hash === PASSWORD_HASH) {
                sessionStorage.setItem('rammp_preview_auth', PASSWORD_HASH);
                showSite();
            } else {
                document.getElementById('errorMsg').classList.add('visible');
                document.getElementById('passwordInput').value = '';
                document.getElementById('passwordInput').focus();
            }
        }
        
        function showSite() {
            document.getElementById('loginOverlay').classList.add('hidden');
            document.getElementById('siteContent').style.display = 'block';
            document.body.innerHTML = document.getElementById('siteContent').innerHTML;
        }
    </script>
</body>
</html>'''


def parse_env_file() -> dict:
    """Parse .env file into a dictionary."""
    env_vars = {}
    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        content = env_file.read_text()
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env_vars[key.strip()] = value
    return env_vars


def get_config() -> dict:
    """Get configuration from .env file and environment variables."""
    env_vars = parse_env_file()
    
    return {
        'password': env_vars.get('DASHBOARD_PASSWORD') or os.environ.get('DASHBOARD_PASSWORD', ''),
        'account_id': env_vars.get('CLOUDFLARE_ACCOUNT_ID') or os.environ.get('CLOUDFLARE_ACCOUNT_ID', ''),
        'project_name': env_vars.get('CLOUDFLARE_PROJECT_NAME') or os.environ.get('CLOUDFLARE_PROJECT_NAME', ''),
    }


def hash_password(password: str) -> str:
    """Generate SHA-256 hash of password."""
    return hashlib.sha256(password.encode()).hexdigest()


def wrap_html_with_password(html_content: str, password_hash: str) -> str:
    """Wrap HTML content with password protection."""
    wrapper = PASSWORD_WRAPPER.replace('%%PASSWORD_HASH%%', password_hash)
    wrapper = wrapper.replace('%%SITE_CONTENT%%', html_content)
    return wrapper


def wrap_site_files(password_hash: str, output_dir: Path):
    """Wrap all HTML files with password protection."""
    print("🔒 Adding password protection...")
    
    # Copy and wrap HTML files
    for html_file in INCLUDE_FILES:
        src = SCRIPT_DIR / html_file
        if src.exists():
            content = src.read_text(encoding='utf-8')
            wrapped = wrap_html_with_password(content, password_hash)
            output_file = output_dir / html_file
            output_file.write_text(wrapped, encoding='utf-8')
            print(f"   ✓ {html_file}")
    
    # Copy asset directories
    for dir_name in INCLUDE_DIRS:
        src_dir = SCRIPT_DIR / dir_name
        if src_dir.exists():
            dest = output_dir / dir_name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src_dir, dest)
            print(f"   ✓ {dir_name}/ (copied)")


def check_wrangler_installed() -> bool:
    """Check if Wrangler CLI is installed."""
    try:
        result = subprocess.run(
            ["wrangler", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def run_wrangler_command(cmd: str, account_id: str) -> tuple:
    """Run a wrangler command and return (success, stdout, stderr)."""
    env = os.environ.copy()
    env['CLOUDFLARE_ACCOUNT_ID'] = account_id
    env['CI'] = 'true'
    
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        env=env,
        text=False
    )
    
    stdout_bytes, stderr_bytes = process.communicate()
    
    try:
        stdout = stdout_bytes.decode('utf-8')
    except UnicodeDecodeError:
        stdout = stdout_bytes.decode('utf-8', errors='replace')
    
    try:
        stderr = stderr_bytes.decode('utf-8')
    except UnicodeDecodeError:
        stderr = stderr_bytes.decode('utf-8', errors='replace')
    
    return (process.returncode == 0, stdout, stderr)


def create_pages_project(project_name: str, account_id: str) -> bool:
    """Create a new Cloudflare Pages project."""
    print(f"   Creating project '{project_name}'...")
    cmd = f'wrangler pages project create {project_name} --production-branch main'
    success, stdout, stderr = run_wrangler_command(cmd, account_id)
    
    if success:
        print(f"   ✓ Project created")
        return True
    elif "already exists" in stderr.lower() or "already exists" in stdout.lower():
        print(f"   ✓ Project already exists")
        return True
    else:
        print(f"   Failed to create project: {stderr}")
        return False


def deploy_to_cloudflare(source_dir: Path, project_name: str, account_id: str) -> str:
    """Deploy the wrapped site to Cloudflare Pages."""
    print(f"🚀 Deploying to Cloudflare Pages ({project_name})...")
    
    create_pages_project(project_name, account_id)
    
    cmd = f'wrangler pages deploy "{source_dir}" --project-name {project_name} --branch main --commit-dirty=true'
    success, stdout, stderr = run_wrangler_command(cmd, account_id)
    
    if not success:
        print(f"❌ Deployment failed:")
        print(stderr)
        sys.exit(1)
    
    print(stdout)
    
    output = stdout + stderr
    import re
    for line in output.split('\n'):
        if '.pages.dev' in line:
            match = re.search(r'https://[^\s]+\.pages\.dev', line)
            if match:
                return match.group(0)
    
    return f"https://{project_name}.pages.dev"


def main():
    no_open = "--no-open" in sys.argv
    local_only = "--local-only" in sys.argv
    
    print("=" * 60)
    print("🚀 RAMMP Website Deployment (Cloudflare Pages)")
    print("=" * 60)
    
    config = get_config()
    
    if not config['password']:
        print("\n❌ No password configured!")
        print("\nAdd to .env file:")
        print("  DASHBOARD_PASSWORD=your-password")
        sys.exit(1)
    
    if not local_only:
        if not config['account_id']:
            print("\n❌ No Cloudflare Account ID configured!")
            print("\nSetup steps:")
            print("  1. Install Wrangler: npm install -g wrangler")
            print("  2. Login: wrangler login")
            print("  3. Get Account ID: wrangler whoami")
            print("  4. Add to .env: CLOUDFLARE_ACCOUNT_ID=your-id")
            sys.exit(1)
        
        if not config['project_name']:
            print("\n❌ No Cloudflare project name configured!")
            print("\nAdd to .env:")
            print("  CLOUDFLARE_PROJECT_NAME=rammp-website")
            sys.exit(1)
        
        if not check_wrangler_installed():
            print("\n❌ Wrangler CLI not found!")
            print("\nInstall with:")
            print("  npm install -g wrangler")
            print("\nThen login:")
            print("  wrangler login")
            sys.exit(1)
    
    password_hash = hash_password(config['password'])
    print(f"\n🔑 Password configured (hash: {password_hash[:8]}...)")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        
        wrap_site_files(password_hash, output_dir)
        
        if local_only:
            local_output = SCRIPT_DIR / "site-protected"
            if local_output.exists():
                shutil.rmtree(local_output)
            shutil.copytree(output_dir, local_output)
            print(f"\n✓ Protected site saved to: {local_output}")
        else:
            pages_url = deploy_to_cloudflare(
                output_dir,
                config['project_name'],
                config['account_id']
            )
            
            print("\n" + "=" * 60)
            print("✅ Deployment complete!")
            print("=" * 60)
            
            print(f"\n📍 Site URL: {pages_url}")
            print("\nShare with your team:")
            print(f"  URL: {pages_url}")
            print(f"  Password: (share securely)")
            
            if not no_open:
                import webbrowser
                print(f"\nOpening {pages_url} ...")
                webbrowser.open(pages_url)


if __name__ == "__main__":
    main()
