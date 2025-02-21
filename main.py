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
    api_key,
    model,
    prompt,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    user_message,
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
            model=(
                model if model else DEFAULT_MODEL
            ),  # Use user-specified model or default
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


# Gradio UI
ui = gr.Interface(
    fn=chat_with_openai,
    inputs=[
        gr.Textbox(
            label="OpenAI API Key (Leave blank to use default)", placeholder="sk-..."
        ),
        gr.Textbox(
            label="Model", value=DEFAULT_MODEL, placeholder="gpt-4, gpt-3.5-turbo, etc."
        ),
        gr.Textbox(
            label="System Prompt",
            value=DEFAULT_PROMPT,
            placeholder="Define AI behavior...",
        ),
        gr.Slider(
            label="Temperature",
            minimum=0.0,
            maximum=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
        ),
        gr.Slider(
            label="Max Tokens",
            minimum=50,
            maximum=4096,
            value=DEFAULT_MAX_TOKENS,
            step=50,
        ),
        gr.Slider(
            label="Top P", minimum=0.0, maximum=1.0, value=DEFAULT_TOP_P, step=0.1
        ),
        gr.Slider(
            label="Frequency Penalty",
            minimum=-2.0,
            maximum=2.0,
            value=DEFAULT_FREQUENCY_PENALTY,
            step=0.1,
        ),
        gr.Slider(
            label="Presence Penalty",
            minimum=-2.0,
            maximum=2.0,
            value=DEFAULT_PRESENCE_PENALTY,
            step=0.1,
        ),
        gr.Textbox(label="User Message", placeholder="Type your message here..."),
    ],
    outputs="text",
    title="Dynamic ChatGPT UI",
    description="Fully customizable ChatGPT interface where you can set all OpenAI parameters dynamically!",
)

ui.launch()
