# Gradio Chatbot UI
This repository contains a Gradio-based Chatbot UI that allows users to interact with OpenAI's GPT models dynamically. The UI provides an intuitive interface for selecting models and configuring parameters to tailor the chatbot responses.

## Features
- 🌐 **Gradio-powered UI** for seamless chatbot interaction
- 🛠️ **Dynamically configurable parameters**
- 🔄 **Supports different OpenAI models** (GPT-4, GPT-3.5-Turbo, etc.)
- 💬 **User-friendly interface** with minimal setup

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bharatsharma19/Gradio-OpenAI-Chat.git
   cd Gradio-OpenAI-Chat/
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

## Usage
Run the chatbot UI:
```bash
python main.py
```

The Gradio interface will launch in your browser automatically.

## Configuration
Users can modify the chatbot settings dynamically via the UI, including:
- Model selection (GPT-4, GPT-3.5-Turbo, etc.)
- Temperature (controls randomness in responses)
- Max tokens (limits response length)
- System and user prompts

## Deployment
To deploy on a server or cloud platform, use:
```bash
huggingface-cli login
gradio share
```

Alternatively, use **Docker**:
```bash
docker build -t gradio-chatbot .
docker run -p 7860:7860 gradio-chatbot
```

## Contributing
Pull requests are welcome! If you have suggestions or find bugs, feel free to open an issue.

## License
MIT License. See `LICENSE` for details.
---

🚀 Enjoy chatting with AI using this Gradio-based UI!
