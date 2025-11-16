# Lingo.dev Translation Setup Guide

## Current Status
The translation server is running correctly, but you need a **valid API key** from Lingo.dev to use the translation features.

## How to Get a Valid API Key

1. Visit https://lingo.dev
2. Sign up for an account (if you don't have one)
3. Navigate to your API settings/dashboard
4. Generate or copy your API key

## How to Set the API Key

### Option 1: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
$env:LINGO_API_KEY="your_api_key_here"
python lingo_server.py
```

**Windows Command Prompt:**
```cmd
set LINGO_API_KEY=your_api_key_here
python lingo_server.py
```

**Linux/Mac:**
```bash
export LINGO_API_KEY="your_api_key_here"
python lingo_server.py
```

### Option 2: Update in Code

Edit `lingo_server.py` and replace line 28:
```python
API_KEY = "your_valid_api_key_here"
```

Or edit `lingo.html` and replace line 278:
```javascript
const apiKey = 'your_valid_api_key_here';
```

## Testing

Once you've set a valid API key:

1. Make sure `lingo_server.py` is running (it should be running on http://127.0.0.1:5000)
2. Open `lingo.html` in your browser
3. Click any language button or "Translate to All Languages"
4. Translations should work!

## Troubleshooting

- **"Invalid API key" error**: Make sure your API key is correct and active
- **"Failed to fetch" error**: Make sure `lingo_server.py` is running
- **Server not starting**: Check that Flask and flask-cors are installed: `pip install flask flask-cors`

## Current Files

- `lingo_server.py` - Flask server that handles translation requests
- `lingo.html` - Web interface for the translation app
- `lingo_translate.py` - Python script example using the SDK

