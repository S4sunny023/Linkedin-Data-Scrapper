# Linkedin-Data-Scrapper



## Description

The LinkedIn Experience Scraper is a Python script designed to automate the process of logging into LinkedIn, navigating to a user's profile, and scraping the details from the experience section of the profile. The scraped data includes role, company, duration, location, work responsibilities, and skills, which are then stored in a CSV file.

## Features

- **Automated LinkedIn Login:** Automatically logs into LinkedIn using provided credentials.
- **Profile URL Validation:** Validates the provided LinkedIn profile URL.
- **Experience Section Scraping:** Extracts detailed experience information from the user's profile.
- **CSV Export:** Saves the scraped data to a CSV file.

## Setup

### Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.
- Google Chrome installed on your system.

### Creating a Conda Environment

1. **Create a new conda environment:**

   ```bash
   conda create -p venv python=3.9 -y
