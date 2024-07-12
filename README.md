# Storage Warriors -- The Solution for Storage Optimization

We are a team of hip and cool Data Scientist that wants to bring prediction via Machine Learning models to the masses.
# Overview

**Storage Warriors** t eine leistungsstarke Lösung für die Datenanalyse und -verwaltung, die darauf abzielt, Geschäftsprozesse durch optimierte Datennutzung zu verbessern. Unsere Plattform ermöglicht die effiziente Analyse und Verwaltung von Daten in verschiedenen Formaten und bietet eine benutzerfreundliche Oberfläche für den Umgang mit großen Datenmengen.
Unser Hauptziel ist es, Unternehmen dabei zu unterstützen, durch die Analyse historischer Bestelldaten präzise Vorhersagen für zukünftige Bestellungen zu treffen. So können Sie rechtzeitig agieren, Ihre Lagerbestände effizienter verwalten und sich entscheidende Wettbewerbsvorteile sichern.

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
