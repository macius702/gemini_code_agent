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
```

### Raw commands (optional)

```bash
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
```

https://www.boot.dev/lessons/7a603e06-4517-4842-9a19-4f4b65adb410


---

## 🛠️ Agent Bugfix Demo

Use the agent to automatically diagnose and fix a deliberate operator-precedence bug in the calculator, then verify the result.

- Trigger the agent to fix the bug and capture logs:
  - `uv run main.py "fix the bug: 3 - 7 * 2 shouldn't be -8, code is in calculator/pkg/calculator.py" --verbose > ai.log`
- Verify the behavior by running the calculator directly:
  - `uv run calculator/main.py "3 - 7 * 2"`

Notes:
- The agent iteratively uses tools (list files, read content, run tests, write file) restricted to the `calculator` directory to make and validate changes in `calculator/pkg/calculator.py`.
- The `ai.log` file captures the model’s reasoning, tool calls, and outputs for auditing.
