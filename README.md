# Important information

If the app doesn't start immediately, it's because the server is hosted on Render's free tier it may take 15 to 50 seconds to wake up from sleep. Wait or reload the window

# How to run app localy
Make sure you have Python installed.

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

On windows

```bash
venv\Scripts\activate
```
On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

# Optional: Fixing Import Issues in VS Code

## Use this step only if you encounter import issues

Run this command to find the exact path to your Python interpreter:

```bash
python -c "import sys; print(sys.executable)"
```

Copy the output path. In VS Code, press Ctrl + Shift + P (or Cmd + Shift + P on Mac), then search for: Python: Select Interpreter. Choose the option to "Enter interpreter path manually", and paste the path you copied.


My app link can be found here: https://vocal-blini-e77de3.netlify.app

My api link can be found here: https://mini-webshop-server.onrender.com





