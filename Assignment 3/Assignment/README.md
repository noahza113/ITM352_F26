# How to Open Quiz Club

## 1. Open the Assignment folder

In VS Code, open this folder:

```text
C:\Users\zneno\OneDrive\Documents\GitHub\ITM352_F26\Assignment 3\Assignment
```

Open **Terminal → New Terminal**. Make sure the terminal is in the folder containing `webapp_quiz.py`. In PowerShell, you can get there with:

```powershell
cd "C:\Users\zneno\OneDrive\Documents\GitHub\ITM352_F26\Assignment 3\Assignment"
```

Do not add another `Assignment 3\Assignment` to the end of the path.

## 2. Install what the program needs

Run these commands the first time:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This makes a local Python environment and installs Flask.

## 3. Start the website

In the same terminal, run:

```powershell
python webapp_quiz.py
```

Leave the terminal open while you use the program.

## 4. Open it in your browser

Go to <http://127.0.0.1:5000>. Create an account or log in, select a quiz topic, and start playing.

To close the program, return to the terminal and press **Ctrl+C**.

## Where your data is saved

The questions are in `data\questions.json`. Accounts are saved in `data\users.json` after someone registers, and quiz scores are saved in `data\scores.json` after completing a quiz. Those two files are created in this Assignment folder when needed.
