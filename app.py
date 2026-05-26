import base64
import io
from typing import Dict

import anthropic
import streamlit as st
from PIL import Image, UnidentifiedImageError
from streamlit.components.v1 import html

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
PLATFORM_PROMPTS = {
    "Instagram": "Create a polished Instagram caption that is engaging and optimized for Reels, Stories, and posts.",
    "Twitter/X": "Create a concise, punchy Twitter/X caption with strong hooks and high impact.",
    "LinkedIn": "Create a professional LinkedIn caption that is thoughtful, credible, and business-friendly.",
    "YouTube": "Create a YouTube caption that is warm, descriptive, and ready to pair with a video thumbnail.",
    "General": "Create a versatile, high-quality caption suitable for general social media use.",
}
TONE_PROMPTS = {
    "Funny": "Use a light, playful, and humorous tone.",
    "Emotional": "Use an emotionally resonant, heartfelt tone.",
    "Inspirational": "Use an uplifting, motivating, and encouraging tone.",
    "Viral": "Use a highly shareable, trend-aware, and attention-grabbing tone.",
    "Professional": "Use a polished, credible, and executive tone.",
    "Poetic": "Use a lyrical, expressive, and evocative tone.",
}


def validate_image(uploaded_file) -> str:
    """Validate uploaded image type and return a safe media type."""
    if uploaded_file is None:
        return ""

    media_type = uploaded_file.type
    if media_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported file type. Please upload JPG, PNG, or WEBP.")

    try:
        image = Image.open(uploaded_file)
        image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc

    return media_type


def encode_image(uploaded_file) -> str:
    """Return base64-encoded image payload for Claude Vision."""
    uploaded_file.seek(0)
    image_bytes = uploaded_file.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")


def build_prompt(platform: str, tone: str) -> str:
    """Build the caption generation prompt for Claude."""
    return (
        f"{PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS['General'])} "
        f"{TONE_PROMPTS.get(tone, TONE_PROMPTS['Professional'])} "
        "Keep it concise, engaging, and ready to post. "
        "Do not include markdown formatting or hashtags unless they naturally fit the caption."
    )


def generate_caption(image_bytes: bytes, media_type: str, filename: str, platform: str, tone: str, api_key: str) -> str:
    """Generate a caption using Anthropic Claude Vision API."""
    client = anthropic.Anthropic(api_key=api_key)
    encoded = base64.b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=240,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": encoded,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            f"Analyze this image and generate a caption for {platform}. "
                            f"Tone: {tone}. "
                            f"File name: {filename}. "
                            f"{build_prompt(platform, tone)}"
                        ),
                    },
                ],
            }
        ],
    )

    return response.content[0].text


def copy_button_html(caption: str) -> None:
    """Render a copy-to-clipboard button using HTML/JS."""
    html(
        f"""
        <div style="margin-top: 0.75rem;">
            <button id="copy-caption-btn" style="
                background: #0E1117;
                color: white;
                border: 1px solid #4B5563;
                border-radius: 8px;
                padding: 0.6rem 1rem;
                font-weight: 600;
                cursor: pointer;
            ">
                Copy caption
            </button>
            <span id="copy-caption-status" style="margin-left: 0.75rem; color: #22c55e; font-weight: 600;"></span>
        </div>
        <script>
            const caption = {caption!r};
            const button = document.getElementById('copy-caption-btn');
            const status = document.getElementById('copy-caption-status');
            button.addEventListener('click', async () => {{
                try {{
                    await navigator.clipboard.writeText(caption);
                    status.textContent = 'Copied!';
                }} catch (error) {{
                    status.textContent = 'Copy failed';
                }}
            }});
        </script>
        """,
        height=90,
    )


def main() -> None:
    st.set_page_config(page_title="AI Caption Generator", page_icon="✨", layout="centered")
    st.title("✨ AI Caption Generator")
    st.caption("Upload an image, choose your platform and tone, and generate a social-ready caption in seconds.")

    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Supported formats: JPG, JPEG, PNG, WEBP",
        )

        col1, col2 = st.columns(2)
        with col1:
            platform = st.selectbox("Platform", list(PLATFORM_PROMPTS.keys()))
            tone = st.selectbox("Tone", list(TONE_PROMPTS.keys()))
        with col2:
            api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

        generate = st.button("Generate caption", use_container_width=True)

    if uploaded_file is not None:
        try:
            media_type = validate_image(uploaded_file)
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded preview", use_container_width=True)
        except ValueError as exc:
            st.error(str(exc))
            st.stop()

    if not generate:
        st.info("Upload an image and click Generate caption to begin.")
        return

    if not api_key:
        st.warning("Please enter your Anthropic API key to continue.")
        return

    if uploaded_file is None:
        st.warning("Please upload an image first.")
        return

    status = st.empty()
    status.info("Generating caption...")

    try:
        image_bytes = uploaded_file.getvalue()
        caption = generate_caption(image_bytes, media_type, uploaded_file.name, platform, tone, api_key)
        status.success("Caption generated successfully.")

        st.subheader("Generated caption")
        st.text_area("Caption", caption, height=180, disabled=True)
        copy_button_html(caption)

    except anthropic.APIStatusError as exc:
        status.error(f"API request failed: {exc}")
    except Exception as exc:
        status.error(f"Something went wrong: {exc}")


if __name__ == "__main__":
    main()
