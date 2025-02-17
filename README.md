# dash-analytics
This repository contains a web application built with Dash, a Python framework for building interactive analytical web applications. The app sends HTTP requests to an external API, retrieves the data in JSON format, and displays it interactively in various formats such as charts, tables, or cards.

## Features:
- **HTTP Requests to External API:** The app makes requests to an external API to fetch data.
- **Interactive Visualization:** Displays the fetched data dynamically using Dash components (graphs, tables, etc.).
- **User-friendly Interface:** Allows users to interact with the app and explore the data based on various filters and inputs.

---

## Installation Guide

### 1. Clone the repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/j-marroquin/dash-analytics.git
```
Navigate to the project folder:
```bash
cd dash-analytics
```

### 2. Set up a virtual environment

Create and activate a virtual environment, install the dependencies using the `requirements.txt` file:

- **Windows:**
```bash
pipenv install -r requirements.txt
```
### 3. Run the application

You can now run the Dash web application locally using:
```bash
pipenv run python Program.py
```
The app will be accessible at `http://127.0.0.1:8050/`.

---

## Create Executable with PyInstaller

To create an executable for the application using **PyInstaller**, follow these steps:

1. Install PyInstaller if you haven't already
```bash
pipenv run pip install pyinstaller
```
2. Navigate to the root folder of the project and run the following command to generate the executable:
```bash
pyinstaller --onefile --add-data "src\\DashboardApp\\config.ini;." --add-data "src\\DashboardApp\\graphs;graphs" --add-data "src\\DashboardApp\\layout;layout" --add-data "src\\DashboardApp\\assets;assets" --add-data "src\\DashboardApp\\pages;pages" --add-data "C:\\Users\\user\\.virtualenvs\\virtual-env-id\\Lib\\site-packages\\dash_ag_grid;dash_ag_grid" src\\DashboardApp\\Program.py
```
This will create a `dist/` directory with the executable file.

3. You can now run the executable located in the `dist/` folder without needing Python installed.

---

## Documentation with Sphinx

To generate documentation for the project using **Sphinx**, follow these steps:

1. Install Sphinx if you haven't already:
```bash
pipenv run pip install sphinx
```
2. Create a Sphinx documentation structure by running:
```bash
sphinx-quickstart
```
Follow the prompts to configure the documentation.

3. Once the documentation structure is created, add the appropriate documentation files in the `docs/` folder.

4. Build the documentation:
```bash
.\make.bat html
```

This will generate HTML documentation located in the `build/html/` directory.

