# 🚀 Project Setup

This project requires two tools to set up the environment:

- [uv](https://docs.astral.sh/uv/) → for Python environment management  
- [bootdev](https://github.com/bootdotdev/bootdev) → for running tasks  

Follow the steps below to get started.

---

## 🔧 Install `uv`

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version

# Initialize project environment
uv init mojprojekcik

# Activate the virtual environment
source .venv/bin/activate

# Install Go (required for bootdev)
curl -sS https://webi.sh/golang | sh
source ~/.config/envman/PATH.env

# Verify Go installation
go version
echo $PATH

# Install bootdev
go install github.com/bootdotdev/bootdev@latest

# Verify installation
bootdev --version

# Login to bootdev
bootdev login

# Run your project
bootdev run 4695fb05-cb7c-44e4-b206-0ed8eac44588


##################################################################### raw #############################3

curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
uv init mojprojekcik
source .venv/bin/activate

curl -sS https://webi.sh/golang | sh
source ~/.config/envman/PATH.env
go version
echo $PATH
go install github.com/bootdotdev/bootdev@latest
bootdev --version
bootev login
bootdev run 4695fb05-cb7c-44e4-b206-0ed8eac44588

https://www.boot.dev/lessons/7a603e06-4517-4842-9a19-4f4b65adb410


