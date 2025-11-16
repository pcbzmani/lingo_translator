#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Flask server to proxy Lingo.dev translation requests
This allows the HTML file to use translations via the Python SDK
"""
import sys
import io
# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import threading
from lingodotdev.engine import LingoDotDevEngine
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API key from environment or default
# Set LINGO_API_KEY environment variable with your valid API key
# Get your API key from https://lingo.dev
API_KEY = os.environ.get("LINGO_API_KEY") or os.environ.get("LINGODOTDEV_API_KEY") or "api_oxxxxxx4"

def run_async(coro):
    """Run async function in a new thread with its own event loop"""
    def run_in_thread():
        # Create a new event loop for this thread
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
    
    # Run in a separate thread to avoid event loop conflicts
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = run_in_thread()
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.start()
    thread.join()
    
    if exception[0]:
        raise exception[0]
    return result[0]

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text')
        source_locale = data.get('source_locale', 'en')
        target_locale = data.get('target_locale')
        
        if not text or not target_locale:
            return jsonify({'error': 'Missing text or target_locale'}), 400
        
        # Use safe encoding for Windows console
        try:
            print(f"Translating: '{text}' from {source_locale} to {target_locale}")
            print(f"Using API key: {API_KEY[:10]}...")
        except UnicodeEncodeError:
            # Fallback for Windows console encoding issues
            print(f"Translating text from {source_locale} to {target_locale}")
            print(f"Using API key: {API_KEY[:10]}...")
        
        # Run async function in a separate thread
        try:
            result = run_async(
                LingoDotDevEngine.quick_translate(
                    text,
                    api_key=API_KEY,
                    source_locale=source_locale,
                    target_locale=target_locale
                )
            )
            return jsonify({'translated_text': result})
        except Exception as api_error:
            error_msg = str(api_error)
            # Try to parse JSON error message if present
            import json
            if error_msg.startswith('{') and 'message' in error_msg:
                try:
                    error_json = json.loads(error_msg)
                    error_msg = error_json.get('message', error_msg)
                except:
                    pass
            
            # Safe print for Windows console
            try:
                print(f"Translation error: {error_msg}")
            except UnicodeEncodeError:
                print("Translation error: Invalid credentials or API error")
            
            # Check if it's an authentication error
            if 'credentials' in error_msg.lower() or 'invalid' in error_msg.lower() or '401' in error_msg or '403' in error_msg:
                return jsonify({
                    'error': 'Invalid API key. Please get a valid API key from https://lingo.dev and set it as LINGO_API_KEY environment variable.'
                }), 401
            raise api_error
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Server error: {error_trace}")
        # Don't expose full traceback to client, just the error message
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

