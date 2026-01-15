# AI Model Pipeline

An interactive Python script to prompt AI models via OpenRouter API.

## Setup

1. Install dependencies:
```bash
pip install requests
```

2. Set your API key as an environment variable:
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key-here"

# Windows CMD
set OPENROUTER_API_KEY=your-api-key-here

# Linux/Mac
export OPENROUTER_API_KEY=your-api-key-here
```

3. Copy the example file and add your key:
```bash
cp access_key.py.example access_key.py
# Then edit access_key.py and add your API key
```

## Usage

Run the script:
```bash
python access_key.py
```

Enter your prompts at the `You:` prompt. Type `quit` or `exit` to stop.

## Security Note

Never commit your API key to version control. The `access_key.py` file is in `.gitignore` for your protection.
