"""
start.py — One-click launcher for AI Fake Detector
----------------------------------------------------
Run this file from the project root:
    python start.py

It will AUTOMATICALLY:
  ✔ Create Python virtual environment if missing
  ✔ Install Python packages from requirements.txt if missing
  ✔ Install Node.js frontend packages if missing
  ✔ Start FastAPI backend  →  http://localhost:8000
  ✔ Start React frontend   →  http://localhost:5173
"""

import subprocess
import sys
import os
import time
import platform

# ── Helpers ────────────────────────────────────────────────────────────────────

def step(icon, text):
    print(f"\n  {icon}  {text}")

def ok(text):
    print(f"      ✅  {text}")

def info(text):
    print(f"      ℹ️   {text}")

def warn(text):
    print(f"      ⚠️   {text}")

def run(cmd, cwd=None, capture=False):
    """Run a command, streaming output unless capture=True."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture,
        text=True,
        check=True,
    )

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR     = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR  = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
REQ_FILE     = os.path.join(ROOT_DIR, "requirements.txt")
IS_WINDOWS   = platform.system() == "Windows"

VENV_DIR     = os.path.join(BACKEND_DIR, ".venv")
if IS_WINDOWS:
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_PIP    = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    NPM_CMD     = "npm.cmd"
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
    VENV_PIP    = os.path.join(VENV_DIR, "bin", "pip")
    NPM_CMD     = "npm"

NODE_MODULES = os.path.join(FRONTEND_DIR, "node_modules")

# ── Banner ─────────────────────────────────────────────────────────────────────
# ANSI color codes
CYAN    = "\033[96m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
MAGENTA = "\033[95m"
WHITE   = "\033[97m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

# Enable ANSI colors on Windows
if IS_WINDOWS:
    os.system("color")

print()
print(CYAN + BOLD + "  ╔══════════════════════════════════════════════════════════════╗" + RESET)
print(CYAN + BOLD + "  ║                                                              ║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ██████╗ ███████╗███████╗██████╗                           " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ██╔══██╗██╔════╝██╔════╝██╔══██╗                          " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ██║  ██║█████╗  █████╗  ██████╔╝                          " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝                           " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ██████╔╝███████╗███████╗██║                               " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + YELLOW + BOLD + "  ╚═════╝ ╚══════╝╚══════╝╚═╝                               " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║                                                              ║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗" + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝" + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗" + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║" + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + MAGENTA + BOLD + "  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝" + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║                                                              ║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + GREEN + "        🧠  AI-Based Fake Image & Video Detector  🧠         " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║" + RESET + WHITE + "                  Powered by FastAPI + React                 " + CYAN + BOLD + "║" + RESET)
print(CYAN + BOLD + "  ║                                                              ║" + RESET)
print(CYAN + BOLD + "  ╚══════════════════════════════════════════════════════════════╝" + RESET)
print()
print(GREEN + "  Checking all requirements before launch..." + RESET)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Python virtual environment
# ══════════════════════════════════════════════════════════════════════════════
step("🐍", "Checking Python virtual environment...")

if not os.path.exists(VENV_PYTHON):
    info("Virtual environment not found. Creating it now...")
    try:
        run([sys.executable, "-m", "venv", VENV_DIR])
        ok("Virtual environment created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n  ❌  Failed to create virtual environment: {e}")
        sys.exit(1)
else:
    ok("Virtual environment already exists.")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Python packages from requirements.txt
# ══════════════════════════════════════════════════════════════════════════════
step("📦", "Checking Python packages (requirements.txt)...")

# Check if all packages are already installed
try:
    result = run(
        [VENV_PIP, "freeze"],
        capture=True
    )
    installed_raw = result.stdout.lower()

    # Read required packages
    with open(REQ_FILE, "r") as f:
        required = [
            line.strip().lower()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    # Simple check: see if any required package name is missing from pip freeze
    missing = []
    for pkg in required:
        pkg_name = pkg.split(">=")[0].split("==")[0].split("[")[0].strip()
        if pkg_name and pkg_name not in installed_raw:
            missing.append(pkg)

    if missing:
        info(f"Missing packages: {', '.join(missing)}")
        info("Installing from requirements.txt ...")
        run([VENV_PIP, "install", "-r", REQ_FILE])
        ok("All Python packages installed successfully.")
    else:
        ok("All Python packages already installed.")

except Exception as e:
    warn(f"Could not verify packages. Attempting install anyway... ({e})")
    try:
        run([VENV_PIP, "install", "-r", REQ_FILE])
        ok("Python packages installed.")
    except subprocess.CalledProcessError as e2:
        print(f"\n  ❌  pip install failed: {e2}")
        sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Node.js / npm check
# ══════════════════════════════════════════════════════════════════════════════
step("🟢", "Checking Node.js / npm...")

try:
    result = run([NPM_CMD, "--version"], capture=True)
    ok(f"npm version {result.stdout.strip()} found.")
except (subprocess.CalledProcessError, FileNotFoundError):
    print()
    print("  ❌  npm (Node.js) not found!")
    print("      Please install Node.js from https://nodejs.org/")
    print("      Then re-run:  python start.py")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Frontend node_modules
# ══════════════════════════════════════════════════════════════════════════════
step("📦", "Checking frontend Node packages (node_modules)...")

if not os.path.exists(NODE_MODULES):
    info("node_modules not found. Running npm install ...")
    try:
        run([NPM_CMD, "install"], cwd=FRONTEND_DIR)
        ok("Frontend packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n  ❌  npm install failed: {e}")
        sys.exit(1)
else:
    ok("node_modules already exists.")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Launch servers
# ══════════════════════════════════════════════════════════════════════════════
print()
print("=" * 62)
print("  🚀  All requirements satisfied! Starting servers...")
print("=" * 62)

step("⚙️ ", "Starting FastAPI backend  →  http://localhost:8000")
backend_proc = subprocess.Popen(
    [VENV_PYTHON, "api.py"],
    cwd=BACKEND_DIR,
)

# Give the backend time to fully start
time.sleep(2)

step("🌐", "Starting React frontend   →  http://localhost:5173")
frontend_proc = subprocess.Popen(
    [NPM_CMD, "run", "dev"],
    cwd=FRONTEND_DIR,
)

# Give Vite time to print its startup info
time.sleep(3)

# ── Final URLs ─────────────────────────────────────────────────────────────────
print()
print("=" * 62)
print("  ✅  BOTH SERVERS ARE RUNNING!")
print()
print("  🌐  Open your browser:  http://localhost:5173")
print()
print("  ⚙️   Backend API:        http://localhost:8000")
print("  📄  API Docs:           http://localhost:8000/docs")
print()
print("  Press  Ctrl+C  to stop both servers.")
print("=" * 62)
print()

# ── Wait & Graceful Shutdown ───────────────────────────────────────────────────
try:
    backend_proc.wait()
except KeyboardInterrupt:
    print("\n\n  [INFO] Shutting down servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
    try:
        backend_proc.wait(timeout=5)
        frontend_proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backend_proc.kill()
        frontend_proc.kill()
    print("  [INFO] All servers stopped. Goodbye! 👋\n")
