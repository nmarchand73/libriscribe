# Ollama Integration for Libriscribe

This document explains how to use the new Ollama integration with Libriscribe, which allows you to run AI models locally without API costs.

## What is Ollama?

Ollama is a tool that allows you to run large language models locally on your machine. This provides several benefits:

- **No API costs** - Run models locally without paying for API calls
- **Privacy** - Your data never leaves your machine
- **Offline capability** - Works without internet connection
- **Model variety** - Access to many open-source models
- **Custom models** - Use fine-tuned models for specific domains

## Installation

### 1. Install Ollama

First, install Ollama on your system:

- **Windows**: Download from [ollama.com](https://ollama.com/download)
- **macOS**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

### 2. Install Python Dependencies

The Ollama Python library is already included in the requirements:

```bash
pip install -r requirements.txt
```

### 3. Start Ollama Service

Start the Ollama service:

```bash
ollama serve
```

### 4. Install a Model

Install a model to use with Libriscribe:

```bash
# Install a popular model (recommended for book writing)
ollama pull llama3.1

# Or install other models
ollama pull mistral
ollama pull codellama
ollama pull gemma2
```

## Usage

### 1. Check Ollama Status

Before using Libriscribe with Ollama, check if everything is working:

```bash
libriscribe check-ollama
```

This command will:
- Check if Ollama service is running
- List available models
- Provide troubleshooting information

### 2. Start a New Project

Start Libriscribe and select Ollama as your AI provider:

```bash
libriscribe start
```

When prompted to select an AI model, choose "ollama" from the list.

### 3. List Available Models

To see what models are available:

```bash
libriscribe list-models
```

### 4. Install New Models

To install additional models:

```bash
libriscribe pull-model llama3.1
libriscribe pull-model mistral
libriscribe pull-model codellama
```

## Configuration

### Environment Variables

You can configure Ollama settings in your `.env` file:

```env
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.1
```

### Model Selection

When using Ollama, you can specify which model to use by setting the `OLLAMA_DEFAULT_MODEL` environment variable or by modifying the model in the settings.

## Recommended Models for Book Writing

Here are some recommended models for different types of content:

### General Writing
- `llama3.1` - Excellent for creative writing and storytelling
- `mistral` - Good for balanced creative and technical content
- `gemma2` - Fast and efficient for various writing tasks

### Technical Writing
- `codellama` - Great for technical documentation
- `deepseek-coder` - Excellent for programming-related content

### Creative Writing
- `llama3.1` - Best overall for fiction and creative content
- `mistral` - Good alternative with different writing style

## Troubleshooting

### Ollama Service Not Running

If you get an error that Ollama service is not running:

```bash
# Start Ollama service
ollama serve

# Check if it's running
libriscribe check-ollama
```

### No Models Installed

If you have no models installed:

```bash
# Install a basic model
ollama pull llama3.1

# Verify installation
libriscribe check-ollama
```

### Performance Issues

If Ollama is running slowly:

1. **Check system resources**: Ollama requires significant RAM and CPU
2. **Use smaller models**: Try `gemma2:2b` instead of `llama3.1:8b`
3. **Close other applications**: Free up system resources
4. **Check GPU support**: Ollama can use GPU acceleration if available

### Model Not Found

If a model is not found:

```bash
# List available models
ollama list

# Pull the specific model
ollama pull <model-name>
```

## Advanced Features

### Streaming Responses

The integration supports streaming responses for long content generation, which can be useful for writing long chapters.

### Custom Models

You can create and use custom models with Ollama:

```bash
# Create a custom model
ollama create my-book-writer -f Modelfile

# Use it in Libriscribe
# Set OLLAMA_DEFAULT_MODEL=my-book-writer in your .env file
```

### Model Management

The integration includes several model management features:

- List available models
- Pull new models
- Check model status
- Switch between models

## Benefits of Using Ollama

1. **Cost Savings**: No API costs for local models
2. **Privacy**: All processing happens on your machine
3. **Offline Work**: No internet required once models are installed
4. **Customization**: Use domain-specific models
5. **Performance**: Potentially faster for repeated operations
6. **Control**: Full control over model versions and updates

## Comparison with Cloud Providers

| Feature | Ollama (Local) | Cloud APIs |
|---------|----------------|------------|
| Cost | Free (after setup) | Pay per use |
| Privacy | Complete | Data sent to provider |
| Internet | Not required | Required |
| Speed | Depends on hardware | Consistent |
| Model variety | Many open-source | Provider-specific |
| Customization | Full control | Limited |

## Getting Help

If you encounter issues:

1. Run the test script: `python test_ollama_integration.py`
2. Check Ollama status: `libriscribe check-ollama`
3. Review the troubleshooting section above
4. Check the [Ollama documentation](https://ollama.com/docs)
5. Ensure your system meets the hardware requirements

## Hardware Requirements

Ollama requires significant system resources:

- **RAM**: 8GB minimum, 16GB+ recommended
- **Storage**: 4GB+ per model
- **CPU**: Modern multi-core processor
- **GPU**: Optional but recommended for better performance

The exact requirements depend on the model size and your system configuration.
