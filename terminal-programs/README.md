# Python Quest — terminal practice

These are worked examples, not tasks you must copy. First try the matching mission on the website. Study the example only when you need it, then close it and rebuild the program yourself.

1. Install Python 3.12 or newer from https://www.python.org/downloads/ (on Windows enable the Python launcher).
2. Open a terminal in this folder.
3. Run a program: `python3 01_hello.py` (Windows: `py 01_hello.py`).
4. Programs using input() wait for you to type a value and press Enter. Supply one value each time; the comments explain the expected inputs.
5. Edit a copy in your editor and rerun it. Ctrl+C stops a running terminal program.

No third-party Python packages are required.

Suggested extensions:
- Bill splitter: reject zero people and invalid amounts.
- Inventory: let the user add or remove items in a menu loop.
- Support desk: repeat until the user chooses quit; keep a running total.
- Add file persistence after completing the foundation course.

These local programs do not automatically report scores to the learning website. Use Check & save in the browser for your practice leaderboard.

## Installation and version check

**Windows:** Open the official https://www.python.org/downloads/windows/ page and install the Python install manager. Reopen PowerShell, run `py install 3.12`, then `py --version`. If a working Python is already installed, you can keep using it. With an older traditional installer, enable Add python.exe to PATH when offered. If `py` is not available but `python --version` works, use `python` in place of `py` below.

**macOS:** Download a supported stable Python 3 macOS .pkg from https://www.python.org/downloads/macos/, install it, open a new Terminal, then run `python3 --version`. Do not remove Apple's system Python.

**Ubuntu / Debian:** Check `python3 --version` first. If needed, run these commands one line at a time:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 --version
```

Other Linux distributions use their own package managers. Do not remove system Python.

A result beginning with Python 3 means the interpreter is available; this course targets 3.12 and these basic programs work with newer stable Python 3 versions too.

## Create and run your own file

1. Create a folder named `python-practice` and open a plain-text/code editor.
2. Save the following as `hello.py`, not `hello.py.txt`:

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

3. Open a terminal in that folder, or use `cd "full folder path"` to get there.
4. List files with `dir` in Windows PowerShell or `ls` on macOS/Linux. You should see `hello.py`.
5. Run `py hello.py` on Windows, or `python3 hello.py` on macOS/Linux.
6. Type your name and press Enter. Edit the greeting, save, and rerun the file.

`pwd` shows your current folder; `cd ..` goes up one folder. Put paths containing spaces in quotes. Do not copy terminal prompt characters such as `$` or `>` into commands.

Running `py` or `python3` without a filename opens interactive Python with a `>>>` prompt. Try `print("Hello")` or `2 + 3`. Type `exit()` before entering terminal commands such as `cd` or `python3 hello.py`.

## Common problems

- Command not found: reopen the terminal, check installation, and use `py`/`python` on Windows or `python3` on macOS/Linux.
- Can't open file: verify the current folder, exact filename, case, and `.py` extension. Extract the ZIP before running its files.
- Waiting for input: type a value and press Enter. Ctrl+C stops a program or infinite loop.
- SyntaxError: check matching quotes, parentheses, and whether a terminal command was typed inside Python.
- IndentationError: use consistent four-space blocks.
- ValueError: check that the input can be converted to the requested number.
- Old output: save your edited file and verify you are running that file.

No pip packages, database or Django installation are needed for these ten programs. On the learning website, choose **Setup & basic help** for the full illustrated-by-code walkthrough and official documentation links.
