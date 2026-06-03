# UK Sky Carrier Lookup System

A free, automated CLI tool to identify UK phone numbers belonging to **Sky UK Limited** using browser automation (Selenium).

## Features

- ✅ **Free CAPTCHA Handling** - Uses browser automation, no API keys needed
- ✅ **Slow & Safe** - Built-in delays to avoid detection
- ✅ **CSV Export** - Results saved to CSV file
- ✅ **Error Handling** - Comprehensive logging for all errors
- ✅ **Sky UK Only** - Filters only Sky UK Limited carriers
- ✅ **Retry Logic** - Automatic retry on failures

## Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver

## Installation

```bash
# Clone repository
git clone https://github.com/jacksonjaike94-eng/uk-sky-carrier-lookup.git
cd uk-sky-carrier-lookup

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Prepare Input File

Create `numbers.txt` with UK phone numbers (one per line):

```
07911123456
07700900123
02031851000
```

### 2. Run the Tool

```bash
python lookup.py --input numbers.txt --output results.csv
```

### 3. Results

Output CSV (`results.csv`):

```
phone_number,carrier,status,timestamp
07911123456,Sky UK Limited,success,2026-06-03 10:30:45
07700900123,Vodafone,filtered,2026-06-03 10:35:22
02031851000,Sky UK Limited,success,2026-06-03 10:40:10
```

## Configuration

Edit `config.py`:

```python
DELAY_BETWEEN_REQUESTS = 8  # seconds
RETRY_ATTEMPTS = 3
CAPTCHA_TIMEOUT = 60  # seconds
HEADLESS_MODE = True  # False for debugging
```

## Logging

Logs are saved to `logs/lookup.log`

## Error Handling

- **Invalid numbers** → Logged, skipped
- **CAPTCHA failure** → Manual solving required
- **Network errors** → Auto-retry
- **Session timeout** → Browser restarts automatically

## Legal Notice

This tool is for educational purposes only. Ensure compliance with website terms of service and UK data protection laws.