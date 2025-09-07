#!/usr/bin/env python3
"""
Simple test script to verify Ollama integration with Libriscribe.
Run this script to test if Ollama is properly integrated.
"""

import sys
import os

# Add the src directory to the path so we can import libriscribe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ollama_import():
    """Test if Ollama can be imported."""
    try:
        import ollama
        print("✅ Ollama library imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Ollama: {e}")
        return False

def test_ollama_service():
    """Test if Ollama service is running."""
    try:
        import ollama
        models = ollama.list()
        print("✅ Ollama service is running")
        if models and models.get('models'):
            print(f"📋 Found {len(models['models'])} models:")
            for model in models['models']:
                print(f"  • {model['name']}")
        else:
            print("⚠️ No models installed. You can install one with: ollama pull llama3.1")
        return True
    except Exception as e:
        print(f"❌ Ollama service not accessible: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

def test_libriscribe_ollama_integration():
    """Test if Libriscribe can use Ollama."""
    try:
        from libriscribe.utils.llm_client import LLMClient
        from libriscribe.settings import Settings
        
        # Test LLMClient initialization with Ollama
        client = LLMClient("ollama")
        print("✅ LLMClient initialized with Ollama provider")
        
        # Test model listing
        models = client.list_available_models()
        if models:
            print(f"✅ Found {len(models)} models via LLMClient")
        else:
            print("⚠️ No models found via LLMClient")
        
        return True
    except Exception as e:
        print(f"❌ Libriscribe Ollama integration failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Ollama Integration with Libriscribe")
    print("=" * 50)
    
    tests = [
        ("Ollama Import", test_ollama_import),
        ("Ollama Service", test_ollama_service),
        ("Libriscribe Integration", test_libriscribe_ollama_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed! Ollama integration is working correctly.")
        print("\n💡 You can now use Ollama with Libriscribe by:")
        print("   1. Running: libriscribe start")
        print("   2. Selecting 'ollama' as your AI model provider")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install Ollama: https://ollama.com/download")
        print("   2. Start Ollama service: ollama serve")
        print("   3. Install a model: ollama pull llama3.1")
        print("   4. Install Python library: pip install ollama")

if __name__ == "__main__":
    main()
