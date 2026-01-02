# Set PowerShell as the default shell for all recipes
set shell := ["powershell.exe", "-Command"]

# Configuration variables - change these paths as needed
PROJECT_ROOT := "E:/Projects/pelicanwebsitebuilder"
PELICAN_DIR := PROJECT_ROOT + "/user_area/smbanaie/smbanaie"
CONTENT_DIR := PELICAN_DIR + "/content"

# Justfile for Pelican Website Builder

# Activate virtual environment and run the application
start:
  .\.venv\Scripts\Activate.ps1; uv run start.py

# Alternative: Run without activating venv (if uv handles it)
run:
  uv run start.py

# Install dependencies
install:
  uv pip install -r requirements.txt

# Development setup
dev:
  uv pip install -r requirements.txt
  uv run start.py

# Clean build
clean:
  uv cache clean
  Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
  Remove-Item -Force *.pyc -ErrorAction SilentlyContinue

# Generate static site with Pelican
generate:
  Set-Location {{PELICAN_DIR}}; uv run pelican {{CONTENT_DIR}}; Set-Location {{PROJECT_ROOT}}

# Serve the generated site locally
serve:
  Set-Location {{PELICAN_DIR}}; uv run pelican {{CONTENT_DIR}} --listen; Set-Location {{PROJECT_ROOT}}

# Full build and serve
build-and-serve:
  just generate
  just serve

# Quick development workflow
dev-workflow:
  just start
  just generate
  just serve