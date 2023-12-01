# Random Database Generator README

## Table of Contents
1. [Introduction](#Introduction)
2. [Prerequisites](#Prerequisites)
3. [Installation](#Installation)
4. [Usage](#Usage)
5. [Project Structure](#Project-Structure)

## 1. Introduction

Welcome to the Random Database Generator repository! This tool allows you to create a database with custom tables and populate them with fake data easily. This README will guide you through the setup and usage of the project.

## 2. Prerequisites

Before you can use this project, make sure you have the following dependencies installed on your system:

- Git
- Python (3.x)
- MySQL server

## 3. Installation

### 3.1 Installing Git

If you don't have Git installed, follow the instructions below based on your operating system:

#### Linux (Ubuntu/Debian)

```
sudo apt update
sudo apt install git
```

#### macOS

```
brew install git
```

#### Windows

Download the Git installer from [Git for Windows](https://gitforwindows.org/) and follow the installation steps.


### 3.2 Installing Python

You can download Python from the official website [Python.org](https://www.python.org/downloads/) and follow the installation instructions for your specific OS.


### 3.3 Installing MySQL Server

Follow the official installation instructions for MySQL based on your OS:

- [MySQL Installation Guide for Linux](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/linux-installation.html)
- [MySQL Installation Guide for macOS](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/macos-installation.html)
- [MySQL Installation Guide for Windows](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/windows-installation.html)


## 4. Usage

### 4.1 Clone the Repository

To get started, clone this repository using Git:

    git clone https://github.com/Anil-Gehlot/Random-Database-Generator

### 4.2 Navigate to the Project Directory

Change your working directory to the project folder:

    cd Random-Database-Generator

### 4.3 Update Database Credentials in app.py

Before running the application, make sure to update the database credentials in the `app.py` file. Open the `app.py` file and locate the following section:


    # Define your MySQL database configuration
    db_config = {
        'host': 'Your-localhost',
        'user': 'your-root',
        'password': 'Your-password'
    }

### 4.4 Installing Python Modules

Once you have Git, Python, and MySQL installed, you'll need to install Python modules required for this project. You can do this using pip, Python's package manager.
Open your terminal and run the following commands:

    pip install -r requirements.txt


### 4.5 Run the Application
You can run the application using Flask. Simply execute the following command:

    flask --app app.py run

This will start the Flask development server, and you can access the Random Database Generator application in your web browser at http://localhost:5000.



## 5. Project Structure

Here's an overview of the project's directory structure:

- `app.py` : The main Flask application.
- `templates/ `: HTML templates for the web interface.
- `static/` : Static assets (CSS, JavaScript, images).
- `README.md` : You are here!
