#!/usr/bin/env python3
"""
Demonstration script showing how to use Ollama with Libriscribe.
This script shows the key features without requiring interactive input.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_ollama_integration():
    """Demonstrate Ollama integration with Libriscribe."""
    print("🎯 Ollama Integration Demo with Libriscribe")
    print("=" * 50)
    
    try:
        # Import Libriscribe components
        from libriscribe.utils.llm_client import LLMClient
        from libriscribe.settings import Settings
        
        print("\n1. 📋 Checking Ollama Status...")
        
        # Initialize LLM client with Ollama
        client = LLMClient("ollama")
        print("✅ LLMClient initialized with Ollama provider")
        
        # List available models
        models = client.list_available_models()
        print(f"📚 Available models ({len(models)}):")
        for model in models:
            print(f"   • {model}")
        
        print("\n2. 🧪 Testing Content Generation...")
        
        # Test content generation
        test_prompt = "Write a short opening paragraph for a science fiction novel about AI consciousness."
        print(f"📝 Prompt: {test_prompt}")
        print("\n🤖 Generating response with llama3.2...")
        
        response = client.generate_content(test_prompt, max_tokens=300, temperature=0.7)
        
        print("\n📖 Generated Content:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
        print("\n3. 🎨 Testing Different Models...")
        
        # Test with different model if available
        if len(models) > 1:
            other_model = models[1]  # Use second model
            print(f"🔄 Switching to {other_model}...")
            client.set_model(other_model)
            
            test_prompt2 = "Write a haiku about programming."
            print(f"📝 Prompt: {test_prompt2}")
            
            response2 = client.generate_content(test_prompt2, max_tokens=100, temperature=0.5)
            print(f"\n📖 Response from {other_model}:")
            print("-" * 40)
            print(response2)
            print("-" * 40)
        
        print("\n4. 🚀 Testing Streaming (if supported)...")
        
        # Test streaming
        def print_chunk(chunk):
            print(chunk, end='', flush=True)
        
        print("📝 Streaming a short story...")
        stream_prompt = "Write a very short story about a robot learning to dance."
        
        try:
            streamed_response = client.generate_content_streaming(stream_prompt, callback=print_chunk)
            print("\n✅ Streaming completed successfully!")
        except Exception as e:
            print(f"⚠️ Streaming not available: {e}")
            # Fallback to regular generation
            regular_response = client.generate_content(stream_prompt, max_tokens=200)
            print("📖 Regular generation result:")
            print("-" * 40)
            print(regular_response)
            print("-" * 40)
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Key Benefits of Using Ollama:")
        print("   • No API costs - runs locally")
        print("   • Complete privacy - data stays on your machine")
        print("   • Works offline - no internet required")
        print("   • Multiple models available")
        print("   • Fast response times")
        
        print("\n🔧 How to Use in Libriscribe:")
        print("   1. Run: libriscribe start")
        print("   2. Choose Simple or Advanced mode")
        print("   3. When prompted for AI model, select 'ollama'")
        print("   4. Libriscribe will use your local Ollama models")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_instructions():
    """Show detailed usage instructions."""
    print("\n📚 Complete Usage Guide:")
    print("=" * 50)
    
    print("\n1. 🚀 Starting a New Project:")
    print("   libriscribe start")
    print("   → Choose 'Simple' or 'Advanced' mode")
    print("   → Enter project name and book title")
    print("   → Select 'ollama' as your AI provider")
    
    print("\n2. 📋 Available Commands:")
    print("   libriscribe check-ollama     # Check Ollama status")
    print("   libriscribe list-models      # List available models")
    print("   libriscribe pull-model <name> # Install new model")
    
    print("\n3. 🎯 Recommended Models for Book Writing:")
    print("   • llama3.2:latest    - Best for creative writing")
    print("   • phi4-mini:latest   - Good for balanced content")
    print("   • deepseek-r1:latest - Excellent for technical writing")
    
    print("\n4. ⚙️ Configuration:")
    print("   Set in .env file:")
    print("   OLLAMA_BASE_URL=http://localhost:11434")
    print("   OLLAMA_DEFAULT_MODEL=llama3.2")
    
    print("\n5. 🔧 Troubleshooting:")
    print("   • If Ollama not found: ollama serve")
    print("   • If no models: ollama pull llama3.2")
    print("   • Check status: libriscribe check-ollama")

if __name__ == "__main__":
    success = demo_ollama_integration()
    show_usage_instructions()
    
    if success:
        print("\n🎉 Ready to use Ollama with Libriscribe!")
    else:
        print("\n⚠️ Please check the error messages above.")
