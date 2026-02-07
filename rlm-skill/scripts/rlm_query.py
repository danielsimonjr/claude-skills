#!/usr/bin/env python3
"""
rlm_query.py - Execute a single sub-LLM query for RLM processing.

This is the core building block for Recursive Language Model processing.
It calls the Anthropic API to get a response from a sub-model.

Usage:
    python rlm_query.py "Your prompt here"
    python rlm_query.py "Your prompt" --model claude-haiku-4-5-20251001
    python rlm_query.py --file prompt.txt

API Key locations (checked in order):
    1. ANTHROPIC_API_KEY environment variable
    2. ~/.claude/api_key.txt (Linux/Mac) or %USERPROFILE%\\.claude\\api_key.txt (Windows)
    3. ~/.claude/config.json with {"api_key": "sk-ant-..."} format

Based on: arXiv:2512.24601 - Recursive Language Models
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from typing import Optional
from pathlib import Path


# Default models - use cheaper models for sub-calls
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
FAST_MODEL = "claude-haiku-4-5-20251001"  # For high-volume chunk processing


def get_claude_config_dir() -> Path:
    """Get the .claude config directory path (cross-platform)."""
    if sys.platform == 'win32':
        # Windows: %USERPROFILE%\.claude
        base = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    else:
        # Linux/Mac: ~/.claude
        base = os.path.expanduser('~')
    
    return Path(base) / '.claude'


def load_api_key() -> Optional[str]:
    """
    Load API key from various sources.
    
    Checks in order:
    1. ANTHROPIC_API_KEY environment variable
    2. ~/.claude/api_key.txt (plain text file)
    3. ~/.claude/config.json (JSON with api_key field)
    
    Returns:
        API key string or None if not found
    """
    # 1. Environment variable (highest priority)
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key.strip()
    
    # 2. Check .claude folder
    claude_dir = get_claude_config_dir()
    
    # 2a. Plain text file: api_key.txt
    api_key_file = claude_dir / 'api_key.txt'
    if api_key_file.exists():
        try:
            api_key = api_key_file.read_text().strip()
            if api_key:
                return api_key
        except Exception:
            pass
    
    # 2b. JSON config file: config.json
    config_file = claude_dir / 'config.json'
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            api_key = config.get('api_key', '').strip()
            if api_key:
                return api_key
        except Exception:
            pass
    
    return None


def llm_query(
    prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    system: Optional[str] = None
) -> str:
    """
    Execute a sub-LLM query via Anthropic API.
    
    Args:
        prompt: The user prompt to send
        model: Model to use (default: claude-sonnet-4)
        max_tokens: Maximum response tokens
        temperature: Sampling temperature (0.0 = deterministic)
        system: Optional system prompt
        
    Returns:
        The model's text response
        
    Raises:
        ValueError: If API key not set
        Exception: If API call fails
    """
    api_key = load_api_key()
    if not api_key:
        claude_dir = get_claude_config_dir()
        raise ValueError(
            f"Anthropic API key not found.\n\n"
            f"Set it using ONE of these methods:\n\n"
            f"Option 1 - Environment variable (Windows PowerShell):\n"
            f"  $env:ANTHROPIC_API_KEY = 'sk-ant-api03-your-key-here'\n\n"
            f"Option 2 - Environment variable (Windows CMD):\n"
            f"  set ANTHROPIC_API_KEY=sk-ant-api03-your-key-here\n\n"
            f"Option 3 - Config file (recommended for persistence):\n"
            f"  Create: {claude_dir / 'api_key.txt'}\n"
            f"  Contents: sk-ant-api03-your-key-here\n\n"
            f"Option 4 - JSON config:\n"
            f"  Create: {claude_dir / 'config.json'}\n"
            f'  Contents: {{"api_key": "sk-ant-api03-your-key-here"}}'
        )
    
    # Build the request payload
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    if system:
        payload["system"] = system
    
    if temperature != 1.0:
        payload["temperature"] = temperature
    
    # Use curl for maximum compatibility (available on Windows 10+)
    payload_json = json.dumps(payload)

    # Write payload to temp file to avoid Windows command-line length limits (~32K)
    tmp_file = None
    try:
        if len(payload_json) > 20000 or sys.platform == 'win32':
            tmp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
            tmp_file.write(payload_json)
            tmp_file.close()
            data_arg = f'@{tmp_file.name}'
        else:
            data_arg = payload_json

        cmd = [
            'curl', '-s',
            'https://api.anthropic.com/v1/messages',
            '-H', 'Content-Type: application/json',
            '-H', f'x-api-key: {api_key}',
            '-H', 'anthropic-version: 2023-06-01',
            '-d', data_arg
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding='utf-8', errors='replace',
            shell=(sys.platform == 'win32')
        )
    finally:
        if tmp_file and os.path.exists(tmp_file.name):
            os.unlink(tmp_file.name)
    
    if result.returncode != 0:
        raise Exception(f"curl failed: {result.stderr}")
    
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response: {result.stdout[:500]}")
    
    if 'error' in response:
        raise Exception(f"API error: {response['error']}")
    
    if 'content' not in response or not response['content']:
        raise Exception(f"Unexpected response format: {response}")
    
    return response['content'][0]['text']


def llm_query_fast(prompt: str, **kwargs) -> str:
    """Execute a fast sub-query using the cheaper/faster model."""
    kwargs['model'] = kwargs.get('model', FAST_MODEL)
    return llm_query(prompt, **kwargs)


def main():
    parser = argparse.ArgumentParser(
        description='Execute a sub-LLM query for RLM processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
API Key Setup (Windows):
    
    Option 1 - PowerShell (temporary):
        $env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
    
    Option 2 - System Environment (permanent):
        Settings > System > About > Advanced system settings
        > Environment Variables > New User Variable
        Name: ANTHROPIC_API_KEY
        Value: sk-ant-api03-...
    
    Option 3 - Config file (recommended):
        Create file: {get_claude_config_dir() / 'api_key.txt'}
        Just paste your API key in the file (nothing else)

Examples:
    python rlm_query.py "What is the capital of France?"
    python rlm_query.py --file my_prompt.txt
    python rlm_query.py "Summarize this..." --fast
        """
    )
    
    parser.add_argument('prompt', nargs='?', help='The prompt to send')
    parser.add_argument('--file', '-f', help='Read prompt from file')
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL, help=f'Model to use (default: {DEFAULT_MODEL})')
    parser.add_argument('--fast', action='store_true', help=f'Use fast model ({FAST_MODEL})')
    parser.add_argument('--max-tokens', '-t', type=int, default=4096, help='Max response tokens')
    parser.add_argument('--temperature', type=float, default=0.0, help='Sampling temperature')
    parser.add_argument('--system', '-s', help='System prompt')
    parser.add_argument('--json', action='store_true', help='Output raw JSON response')
    parser.add_argument('--check-key', action='store_true', help='Check if API key is configured')
    
    args = parser.parse_args()
    
    # Check API key configuration
    if args.check_key:
        api_key = load_api_key()
        if api_key:
            # Show masked key
            masked = api_key[:10] + '...' + api_key[-4:] if len(api_key) > 20 else '***'
            print(f"[OK] API key found: {masked}")
            print(f"  Config dir: {get_claude_config_dir()}")
        else:
            print("[X] API key not found")
            print(f"  Config dir: {get_claude_config_dir()}")
        return
    
    # Get the prompt
    if args.file:
        with open(args.file, 'r') as f:
            prompt = f.read()
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)
    
    # Override model if --fast specified
    model = FAST_MODEL if args.fast else args.model
    
    try:
        response = llm_query(
            prompt=prompt,
            model=model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            system=args.system
        )
        
        if args.json:
            print(json.dumps({"response": response}, indent=2))
        else:
            print(response)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
