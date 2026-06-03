# Usage Guide

## Quick Start

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

### 3. Check Results

Output CSV will be created in `results/` directory:

```csv
phone_number,carrier,status,timestamp
07911123456,Sky UK Limited,success,2026-06-03 10:30:45
07700900123,Vodafone,filtered,2026-06-03 10:35:22
02031851000,Sky UK Limited,success,2026-06-03 10:40:10
```

## Command Line Options

```bash
python lookup.py --input FILE [OPTIONS]
```

### Required Arguments

- `--input, -i FILE` - Input file with phone numbers (one per line)

### Optional Arguments

- `--output, -o FILE` - Output CSV filename
- `--delay, -d SECONDS` - Delay between requests (default: 8)
- `--no-filter` - Return all carriers (not just Sky UK)
- `--debug` - Enable debug logging

## Examples

```bash
# Basic usage
python lookup.py --input numbers.txt

# Custom output file
python lookup.py --input numbers.txt --output my_results.csv

# Slower (safer) - 15 second delays
python lookup.py --input numbers.txt --delay 15

# See all carriers
python lookup.py --input numbers.txt --no-filter

# Debug mode
python lookup.py --input numbers.txt --debug
```

## Understanding Results

### Status Values

- **success** - Successfully found Sky UK Limited carrier
- **filtered** - Found carrier but not Sky UK
- **error_navigate** - Failed to navigate to website
- **error_input** - Failed to find input field
- **error_submit** - Failed to submit form
- **error_captcha** - CAPTCHA handling failed
- **error_parsing** - Failed to parse results
- **error_exception** - Unexpected error occurred

## CAPTCHA Handling

When a CAPTCHA is detected:

1. The browser will pause and wait
2. You have 60 seconds to solve it manually
3. Look for the browser window with the CAPTCHA
4. Solve it
5. The script will continue automatically

## Logging

All operations are logged to `logs/lookup.log`. View in real-time:

```bash
# macOS/Linux
tail -f logs/lookup.log

# Windows
Get-Content logs/lookup.log -Wait
```