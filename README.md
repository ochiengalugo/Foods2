# Inventory Management System — Administrator Portal

A Python-based RESTful API developed with Flask, paired with an interactive Command Line Interface (CLI) front-end tool designed for an e-commerce website administrator portal. This system manages local inventory items via an in-memory database list and integrates seamlessly with mock OpenFoodFacts product data streams.

---

## Project Architecture

The system is separated into two decoupled layers:
1. **Back-End API (`app.py`)**: A Flask-based REST service managing CRUD operations on items structured like OpenFoodFacts registry items.
2. **Front-End CLI (`cli.py`)**: A text-based, terminal-driven administrative dashboard utilizing Python's `requests` package to execute live operations.

---

## Installation & Setup Instructions

Follow these instructions to clone, configure, and execute the portal on your system.

### Step 1: Clone the Repository
Open your terminal and run the following commands to clone the source code and navigate into your project root directory:
```bash
git clone <your-github-repo-url>
cd <your-repo-directory>