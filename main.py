import gradio as gr
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default OpenAI API Key (Can be overridden in UI)
DEFAULT_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default OpenAI settings
DEFAULT_MODEL = "gpt-4"
DEFAULT_PROMPT = os.getenv("OPENAI_SYSTEM_PROMPT", "You are a helpful assistant.")
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500
DEFAULT_TOP_P = 1.0
DEFAULT_FREQUENCY_PENALTY = 0.0
DEFAULT_PRESENCE_PENALTY = 0.0


def chat_with_openai(
    user_message,
    api_key,
    model,
    prompt,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
):
    """
    Function to interact with OpenAI's API dynamically using user-defined parameters.
    """

    # Use provided API key, or fallback to the default one
    api_key = api_key if api_key else DEFAULT_API_KEY

    if not api_key:
        return "⚠️ Error: No API key provided! Please enter a valid OpenAI API key."

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model if model else DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": prompt if prompt else DEFAULT_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
            max_tokens=max_tokens if max_tokens else DEFAULT_MAX_TOKENS,
            top_p=top_p if top_p is not None else DEFAULT_TOP_P,
            frequency_penalty=(
                frequency_penalty
                if frequency_penalty is not None
                else DEFAULT_FREQUENCY_PENALTY
            ),
            presence_penalty=(
                presence_penalty
                if presence_penalty is not None
                else DEFAULT_PRESENCE_PENALTY
            ),
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ OpenAI API Error: {str(e)}"


# Gradio UI with enhanced styling and layout
with gr.Blocks(
    css="""
    body { background-color: #121212; color: white; font-family: 'Arial', sans-serif; }
    .gradio-container { max-width: 100vw; margin: auto; padding: 20px; }
    .output-box { border: 2px solid #444; border-radius: 10px; padding: 15px; background-color: #222; }
    .btn-custom { background-color: #ff9900; color: black; font-weight: bold; }
    .hidden { display: none; }
    .settings-container { width: 20vw; transition: width 0.3s ease; overflow: hidden; }
    .settings-container.open { width: 60vw; }
    .input-container { width: 20vw; }
    .output-container { width: 40vw; }
    .row-flex { display: flex; flex-direction: row; gap: 10px; }
"""
) as ui:
    gr.Markdown(
        """
    # 🚀 **AI Chat Assistant**
    Engage in an interactive AI chat experience with customizable settings.
    """
    )

    with gr.Row():
        with gr.Column(
            scale=1, elem_id="settings-panel", elem_classes="settings-container"
        ):
            with gr.Accordion("⚙️ Advanced Settings", open=False):
                api_key = gr.Textbox(
                    label="🔑 OpenAI API Key", placeholder="sk-...", type="password"
                )
                model = gr.Dropdown(
                    ["gpt-4", "gpt-3.5-turbo"], value=DEFAULT_MODEL, label="🤖 Model"
                )
                prompt = gr.Textbox(
                    label="📜 System Prompt",
                    value=DEFAULT_PROMPT,
                    placeholder="Define AI behavior...",
                )
                temperature = gr.Slider(
                    label="🔥 Temperature",
                    minimum=0.0,
                    maximum=1.0,
                    value=DEFAULT_TEMPERATURE,
                    step=0.1,
                )
                max_tokens = gr.Slider(
                    label="🔠 Max Tokens",
                    minimum=50,
                    maximum=4096,
                    value=DEFAULT_MAX_TOKENS,
                    step=50,
                )
                top_p = gr.Slider(
                    label="🎯 Top P",
                    minimum=0.0,
                    maximum=1.0,
                    value=DEFAULT_TOP_P,
                    step=0.1,
                )
                frequency_penalty = gr.Slider(
                    label="📉 Frequency Penalty",
                    minimum=-2.0,
                    maximum=2.0,
                    value=DEFAULT_FREQUENCY_PENALTY,
                    step=0.1,
                )
                presence_penalty = gr.Slider(
                    label="📈 Presence Penalty",
                    minimum=-2.0,
                    maximum=2.0,
                    value=DEFAULT_PRESENCE_PENALTY,
                    step=0.1,
                )

        with gr.Column(scale=2, elem_classes="row-flex"):
            with gr.Column(scale=1, elem_classes="input-container"):
                user_message = gr.Textbox(
                    label="📝 User Message", placeholder="Type your message here..."
                )
                submit_button = gr.Button(
                    "🚀 Generate Response", elem_classes="btn-custom"
                )

            with gr.Column(scale=1, elem_classes="output-container"):
                output_text = gr.Textbox(
                    label="💬 AI Response", interactive=False, elem_classes="output-box"
                )

    submit_button.click(
        chat_with_openai,
        inputs=[
            user_message,
            api_key,
            model,
            prompt,
            temperature,
            max_tokens,
            top_p,
            frequency_penalty,
            presence_penalty,
        ],
        outputs=output_text,
    )

ui.launch()
