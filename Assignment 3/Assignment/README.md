# How to Open Quiz Club

These instructions work on Windows, macOS, and Linux. You need Python 3.9 or newer and an internet connection the first time you install Flask.

## 1. Open the program folder

In VS Code, choose **File → Open Folder** and open the Assignment folder that contains `webapp_quiz.py`.

Open **Terminal → New Terminal**. The terminal should start in that same folder. If it does not, use `cd` to move into the folder; the folder's location can be different on each computer.

## 2. Create a Python environment

Run the command for your computer:

**Windows PowerShell**

```powershell
py -m venv .venv
```

If `py` is not recognized, try `python -m venv .venv`.

**macOS or Linux**

```sh
python3 -m venv .venv
```

## 3. Activate the environment and install Flask

Run the activation command for your terminal:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**macOS or Linux**

```sh
source .venv/bin/activate
```

Then, on all systems, install the required package:

```sh
python -m pip install -r requirements.txt
```

If your computer uses `python3` instead of `python`, use `python3 -m pip install -r requirements.txt`.

You only need to create the environment and install Flask the first time. Later, open a terminal in the Assignment folder and activate the environment again.

## 4. Start and open the website

In the terminal, run:

```sh
python webapp_quiz.py
```

If needed, use `python3 webapp_quiz.py`. Keep the terminal open while playing, then open <http://127.0.0.1:5000> in your browser. Register or log in, choose a topic, and start the quiz. You can request one hint during each quiz; after it is used, the hint button is disabled for the rest of that round.

To stop the app, return to the terminal and press **Ctrl+C**.

## Where your data is saved

The quiz questions are in `data/questions.json`. The app creates `data/users.json` when someone registers and `data/scores.json` when someone completes a quiz. These files are stored in the Assignment folder on the computer running the app.
