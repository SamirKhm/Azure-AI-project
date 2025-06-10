import streamlit as st
import requests
import openai

# ==== Azure Keys and Endpoints ====
VISION_API_KEY = "A3jzKkTW2Utx17AOYZwUQ447aHUEouMUVuYKdRDl6P1ddmwylmv9JQQJ99BFACYeBjFXJ3w3AAAFACOG5DfE"
VISION_ENDPOINT = "https://image-caption-app.cognitiveservices.azure.com/"  # e.g., https://<resource-name>.cognitiveservices.azure.com
VISION_URL = VISION_ENDPOINT + "/vision/v3.2/describe?maxCandidates=3"

# Azure OpenAI Setup
openai.api_key = "ECguAQRE6a3vvI6CDuNxT0LuxxUsrwMF8z48S43VLFiyFbVj0rduJQQJ99BFACHYHv6XJ3w3AAABACOGFqFV"
openai.api_base = "https://caption-discription.openai.azure.com/"  # e.g., https://<resource-name>.openai.azure.com/
openai.api_type = "azure"
openai.api_version = "2023-12-01-preview"
GPT_DEPLOYMENT_NAME = "YOUR_GPT_DEPLOYMENT_NAME"  # e.g., gpt-35-turbo

# ==== Streamlit UI ====
st.title("🧠 AI-Powered Image Caption Generator")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

    headers = {
        'Ocp-Apim-Subscription-Key': VISION_API_KEY,
        'Content-Type': 'application/octet-stream'
    }

    # Step 1: Call Azure Computer Vision
    response = requests.post(VISION_URL, headers=headers, data=image_bytes)
    result = response.json()

    if "description" in result and result["description"]["captions"]:
        # Get best caption and tags
        caption = result["description"]["captions"][0]["text"]
        tags = result["description"].get("tags", [])
        tags_text = ", ".join(tags)

        # Show Azure output
        st.info("🖼 Azure Vision Caption:")
        st.write(caption)
        st.info("🏷 Tags:")
        st.write(tags_text)

        # Step 2: Expand caption with GPT
        prompt = f"Expand the following image caption and tags into a longer, vivid description:\n\nCaption: {caption}\nTags: {tags_text}"

        try:
            gpt_response = openai.ChatCompletion.create(
                engine=GPT_DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )

            long_caption = gpt_response['choices'][0]['message']['content']

            # Show final enhanced caption
            st.success("✨ AI-Enhanced Detailed Caption:")
            st.write(long_caption)

        except Exception as e:
            st.warning("⚠ GPT Enhancement Failed.")
            st.write(str(e))

        # Optional: Show all Azure captions with c