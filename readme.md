# Project Setup

This project involves web scraping, content chunking, and generating text using Google's Generative AI. The instructions below will guide you through setting up the project environment, installing the necessary dependencies, and running the code.

## Prerequisites

Before you begin, ensure that you have Python 3.x installed on your system. You can check the version of Python installed by running the following command:

```bash
python3 --version
```
# Step 1: Set Up a Virtual Environment
It's recommended to use a virtual environment to manage the dependencies for this project. Run the following commands to create and activate a virtual environment:

```bash
python3 -m venv path/to/venv
source path/to/venv/bin/activate
```

The source command activates the virtual environment, ensuring that the installed packages remain isolated from your global Python environment.

# Step 2: Install Dependencies
Once the virtual environment is activated, install the necessary Python packages using pip.

2.1 Install requests Library
The requests library is required for making HTTP requests to fetch web content.

```bash
sudo pip3 install requests
```
2.2 Install BeautifulSoup4
The BeautifulSoup4 package is used for parsing and extracting data from HTML pages.

```bash
pip install BeautifulSoup4
```

2.3 Install Google API Client
To interact with Google's services, install the google-api-python-client.
```bash
pip install --upgrade google-api-python-client
```

2.4 Install Google Generative AI Library
To use Google's Generative AI for text generation, install the google-generativeai package.
```bash
pip install google-generativeai
```

# Running the Project

Once you have installed all the required dependencies, you can run the Python scripts as per the project instructions. Ensure that your virtual environment is active (run source path/to/venv/bin/activate if needed), and execute the scripts with:

```bash
python scrapeNChunk.py
```

