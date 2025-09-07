# Model Selection Workflow in Libriscribe

## 📋 **When is the Model Selected?**

The model selection happens **early in the workflow**, right after you provide basic project information but before any AI-generated content is created.

## 🔄 **Complete Workflow with Model Selection**

```
1. 🚀 Start Libriscribe
   libriscribe start
   ↓
2. 📝 Choose Mode
   • Simple (guided process)
   • Advanced (more options)
   ↓
3. 📁 Project Setup
   • Enter project name
   • Enter book title
   ↓
4. 🌐 Language Selection
   • Select language for your book
   ↓
5. 🤖 MODEL SELECTION ← THIS IS WHERE IT HAPPENS!
   • System checks available providers:
     - OpenAI (if API key exists)
     - Claude (if API key exists)
     - Google AI Studio (if API key exists)
     - DeepSeek (if API key exists)
     - Mistral (if API key exists)
     - Ollama (if service is running) ← YOUR CASE!
   • User selects from available options
   • System initializes LLMClient with selected provider
   ↓
6. 📚 Book Configuration
   • Category (Fiction, Non-Fiction, Business, Research)
   • Genre selection
   • Book length
   • Additional details
   ↓
7. 🎯 AI Content Generation
   • Concept generation (uses selected model)
   • Outline creation (uses selected model)
   • Character profiles (uses selected model)
   • Chapter writing (uses selected model)
   • All subsequent AI operations use the selected model
```

## 🎯 **Specific Code Flow**

### **Simple Mode:**
```python
def simple_mode():
    # 1. Get project name and title
    project_name, title = get_project_name_and_title()
    project_knowledge_base = ProjectKnowledgeBase(project_name=project_name, title=title)
    
    # 2. Select language
    select_language(project_knowledge_base)
    
    # 3. 🤖 MODEL SELECTION HAPPENS HERE!
    llm_choice = select_llm(project_knowledge_base)
    project_manager.initialize_llm_client(llm_choice)
    
    # 4. Continue with book configuration...
```

### **Advanced Mode:**
```python
def advanced_mode():
    # 1. Get project name and title
    project_name, title = get_project_name_and_title()
    project_knowledge_base = ProjectKnowledgeBase(project_name=project_name, title=title)
    
    # 2. Select language
    select_language(project_knowledge_base)
    
    # 3. 🤖 MODEL SELECTION HAPPENS HERE!
    llm_choice = select_llm(project_knowledge_base)
    project_manager.initialize_llm_client(llm_choice)
    
    # 4. Continue with advanced configuration...
```

## 🔍 **What Happens During Model Selection**

### **1. Provider Detection:**
```python
def select_llm(project_knowledge_base):
    available_llms = []
    
    # Check each provider
    if settings.openai_api_key:
        available_llms.append("openai")
    if settings.claude_api_key:
        available_llms.append("claude")
    # ... other providers
    
    # Check Ollama specifically
    try:
        import ollama
        models = ollama.list()
        if models:
            available_llms.append("ollama")  # ← This adds Ollama to the list
    except:
        pass  # Ollama not available
```

### **2. User Selection:**
```python
# Present options to user
llm_choice = select_from_list("🤖 Select your preferred AI model:", available_llms)

# Convert selection to provider identifier
if "Ollama" in llm_choice:
    llm_choice = "ollama"
```

### **3. Client Initialization:**
```python
# Initialize the LLM client with selected provider
project_manager.initialize_llm_client(llm_choice)

# This creates the LLMClient with the selected provider
self.llm_client = LLMClient(llm_provider)  # e.g., LLMClient("ollama")
```

### **4. Model Assignment:**
```python
# In LLMClient.__init__()
def __init__(self, llm_provider: str):
    self.llm_provider = llm_provider
    self.client = self._get_client()  # Initialize Ollama client
    self.model = self._get_default_model()  # Set to "llama3.2"

def _get_default_model(self):
    if self.llm_provider == "ollama":
        return self.settings.ollama_default_model  # "llama3.2"
```

## 🎯 **Key Points About Model Selection**

### **⏰ Timing:**
- **Early in workflow** - Before any AI content generation
- **After basic project setup** - Name, title, language
- **Before book configuration** - Category, genre, etc.

### **🔄 Persistence:**
- **Once selected, used throughout the entire project**
- **All AI agents use the same model**
- **Model choice is saved in project data**

### **🎛️ Model Switching:**
- **Can change model between projects**
- **Cannot change model within a single project** (would break consistency)
- **Use `client.set_model()` to switch models programmatically**

### **📊 What Uses the Selected Model:**
- ✅ Concept generation
- ✅ Outline creation
- ✅ Character profiles
- ✅ Worldbuilding details
- ✅ Chapter writing
- ✅ Content editing
- ✅ Style editing
- ✅ Content review
- ✅ Book formatting

## 🚀 **For Your Ollama Setup:**

When you run `libriscribe start` and select Ollama:

1. **System detects** Ollama is running with your models
2. **You select** "ollama" from the provider list
3. **System initializes** LLMClient with "ollama" provider
4. **Default model** is set to "llama3.2" (from settings)
5. **All subsequent AI operations** use llama3.2 locally

## 💡 **Pro Tips:**

- **Check availability first**: `libriscribe check-ollama`
- **Model is selected once per project** - choose wisely!
- **All AI operations use the same model** for consistency
- **You can switch models between different projects**
