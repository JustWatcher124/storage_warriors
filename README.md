# Storage Warriors -- The Solution for Storage Optimization

We are a team of hip and cool Data Scientist that wants to bring prediction via Machine Learning models to the masses.

# Overview

**Storage Warriors** is a high-performing solution for data analysis and management that aims to improve business processes by optimizing data usage. Our platform allows for efficient analysis and management of data in various formats and offers a user-friendly interface for handling large amounts of data.

Our main goal is to help businesses make precise predictions about future orders based on the analysis of historical order data. This enables you to act promptly, manage inventory efficiently, and secure significant competitive advantages.

# Team Members / Participants

| Member Name    | Student Number |
| -------------- | -------------- |
| Hendrik Träber | 6367227        |
| Paul Brüderle  | 3224687        |
| David Kleiner  | 1622864        |
| Gülbahar Cogac | 5801309        |

# Installation

To install our program, clone or download the REPO and go to the directory

```
git clone https://github.com/JustWatcher124/storage_warriors
cd storage_warriors
```

It is recommended to install all dependencies in a separate python virtual environment.
To achieve this recommendation:

```
python -m venv ./venv_storage_warriors
## For Windows
# In cmd.exe
./venv_storage_warriors\Scripts\activate.bat
# In PowerShell
./venv_storage_warriors\Scripts\Activate.ps1

## For GNU+Linux / MacOs Systems
source ./venv_storage_warriors/bin/activate
```

We supply a `requirements.txt` file that contains all necessary python modules.

You can install from this file with

```
pip install -r requirements.txt
```

See _Usage_ to see how to use the software

# Usage

You can now start the Platform by:

```
cd showcase
streamlit run startpage.py
```

The Platform will guide you through the usage.

## Usage Disclaimer

The Platform was only properly tested with \*Nix systems and may lead to unforeseen, and unwanted behaviour.

If you are on Windows 10 and above, you can use WSL to ensure the platform runs without errors.
