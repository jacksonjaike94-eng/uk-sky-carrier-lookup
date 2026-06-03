# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Chrome or Chromium browser installed
- pip package manager

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jacksonjaike94-eng/uk-sky-carrier-lookup.git
cd uk-sky-carrier-lookup
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Tool

```bash
python lookup.py --input numbers.txt --output results.csv
```

## Troubleshooting

### Chrome Not Found

Ensure Chrome is installed from: https://www.google.com/chrome/