"""
Test script to check Claude API connection and available models
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ ANTHROPIC_API_KEY not found in .env file")
    exit(1)

print(f"✓ API Key found (starts with: {api_key[:10]}...)")

# Test different model names
test_models = [
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-latest",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

print("\n🔍 Testing Claude models...\n")

client = Anthropic(api_key=api_key)

for model in test_models:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ {model} - WORKS!")
        print(f"   Response: {response.content[0].text}")
        break
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not_found" in error_msg:
            print(f"❌ {model} - Not found")
        else:
            print(f"⚠️  {model} - Error: {error_msg[:100]}")

print("\n✓ Test complete!")
