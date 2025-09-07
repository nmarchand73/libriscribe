# src/libriscribe/utils/llm_client.py
import openai
from openai import OpenAI  # For OpenAI
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential
from libriscribe.settings import Settings

import anthropic  # For Claude
import google.generativeai as genai  # For Google AI Studio
import requests  # For DeepSeek and Mistral
import ollama  # For Ollama

# ADDED THIS: Import the function
from libriscribe.utils.file_utils import extract_json_from_markdown

logger = logging.getLogger(__name__)

# Configure httpx logger to be less verbose
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)  # Or ERROR, to suppress even warnings


class LLMClient:
    """Unified LLM client for multiple providers."""

    def __init__(self, llm_provider: str):
        self.settings = Settings()
        self.llm_provider = llm_provider
        self.client = self._get_client()  # Initialize the correct client
        self.model = self._get_default_model()

    def _get_client(self):
        """Initializes the appropriate client based on the provider."""
        if self.llm_provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OpenAI API key is not set.")
            return OpenAI(api_key=self.settings.openai_api_key)
        elif self.llm_provider == "claude":
            if not self.settings.claude_api_key:
                raise ValueError("Claude API key is not set.")
            return anthropic.Anthropic(api_key=self.settings.claude_api_key)
        elif self.llm_provider == "google_ai_studio":
            if not self.settings.google_ai_studio_api_key:
                raise ValueError("Google AI Studio API key is not set.")
            genai.configure(api_key=self.settings.google_ai_studio_api_key)
            return genai  # We don't instantiate a client, we use the module directly
        elif self.llm_provider == "deepseek":
             if not self.settings.deepseek_api_key:
                raise ValueError("DeepSeek API key is not set.")
             return None  # No client object, we'll use requests directly
        elif self.llm_provider == "mistral":
             if not self.settings.mistral_api_key:
                raise ValueError("Mistral API key is not set")
             return None
        elif self.llm_provider == "ollama":
            # Check if Ollama service is running
            if not self._check_ollama_availability():
                raise ValueError("Ollama service is not running. Please start Ollama first.")
            return ollama
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def _get_default_model(self):
        """Gets the default model name for the selected provider."""
        if self.llm_provider == "openai":
            return "gpt-4o-mini"
        elif self.llm_provider == "claude":
            return "claude-3-opus-20240229" # Or another appropriate Claude 3 model
        elif self.llm_provider == "google_ai_studio":
            return "gemini-1.5-pro-002"
        elif self.llm_provider == "deepseek":
             return "deepseek-coder-6.7b-instruct"
        elif self.llm_provider == "mistral":
            return "mistral-medium-latest"
        elif self.llm_provider == "ollama":
            return self.settings.ollama_default_model
        else:
            return "unknown"  # Should not happen, but good for safety
    def set_model(self, model_name: str):
      self.model = model_name

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate_content(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7, language: str = "English") -> str:
        """
        Generates text using the selected LLM provider.
        Now supports specifying the output language explicitly.
        """
        try:
            # Append language instruction to prompt if not already included
            if "IMPORTANT: The content should be written entirely in" not in prompt and language != "English":
                prompt += f"\n\nIMPORTANT: Generate the response in {language}."
                
            if self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response.choices[0].message.content.strip()

            elif self.llm_provider == "claude":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()

            elif self.llm_provider == "google_ai_studio":
                model = self.client.GenerativeModel(model_name=self.model)
                response = model.generate_content(prompt) # No need for messages list with genai
                return response.text.strip()

            elif self.llm_provider == "deepseek":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.deepseek_api_key}"
                }
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=120) # Timeout
                response.raise_for_status() # Raise for HTTP errors
                return response.json()["choices"][0]["message"]["content"].strip()
            elif self.llm_provider == "mistral":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.mistral_api_key}"
                }
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data, timeout=120)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content'].strip()

            elif self.llm_provider == "ollama":
                response = self.client.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                )
                return response['message']['content'].strip()

            else:
                return "" #  Should not happen, provider checked in init

        except Exception as e:
            logger.exception(f"Error during {self.llm_provider} API call: {e}")
            print(f"ERROR: {self.llm_provider} API error: {e}")
            return ""
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def generate_content_with_json_repair(self, original_prompt: str, max_tokens:int = 2000, temperature:float=0.7) -> str:
        """Generates content and attempts to repair JSON errors."""
        response_text = self.generate_content(original_prompt, max_tokens, temperature)
        if response_text:
            json_data = extract_json_from_markdown(response_text)
            if json_data is not None:
                return response_text # Return the original markdown
            else:
                repair_prompt = f"You are a helpful AI that only returns valid JSON.  Fix the following broken JSON:\n\n```json\n{response_text}\n```"
                repaired_response = self.generate_content(repair_prompt, max_tokens=max_tokens, temperature=0.2) #Low temp for corrections
                if repaired_response:
                    repaired_json = extract_json_from_markdown(repaired_response)
                    if repaired_json is not None:
                        # CRITICAL CHANGE:  Return the JSON *string*, not wrapped in Markdown.
                        return repaired_response 
        logger.error("JSON repair failed.")
        return "" # Return empty

    def _check_ollama_availability(self) -> bool:
        """Check if Ollama service is running."""
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def list_available_models(self) -> list:
        """List available models for the current provider."""
        if self.llm_provider == "ollama":
            try:
                models = self.client.list()
                # Handle different response formats
                if hasattr(models, 'models'):
                    return [model.model for model in models.models]
                elif isinstance(models, dict) and 'models' in models:
                    return [model['model'] for model in models['models']]
                else:
                    return []
            except Exception as e:
                logger.error(f"Failed to list Ollama models: {e}")
                return []
        else:
            # For other providers, return empty list or implement as needed
            return []

    def pull_model(self, model_name: str) -> bool:
        """Pull a new model (Ollama specific)."""
        if self.llm_provider == "ollama":
            try:
                self.client.pull(model_name)
                return True
            except Exception as e:
                logger.error(f"Failed to pull model {model_name}: {e}")
                return False
        return False

    def generate_content_streaming(self, prompt: str, callback=None) -> str:
        """Stream content generation (useful for long responses)."""
        if self.llm_provider == "ollama":
            try:
                stream = self.client.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                full_response = ""
                for chunk in stream:
                    content = chunk['message']['content']
                    full_response += content
                    if callback:
                        callback(content)
                return full_response
            except Exception as e:
                logger.error(f"Error during Ollama streaming: {e}")
                return ""
        else:
            # Fallback to regular generation for other providers
            return self.generate_content(prompt)