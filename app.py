import streamlit as st
import requests

# ==== Azure Computer Vision Keys and Endpoints ====
VISION_API_KEY = "A3jzKkTW2Utx17AOYZwUQ447aHUEouMUVuYKdRDl6P1ddmwylmv9JQQJ99BFACYeBjFXJ3w3AAAFACOG5DfE"  # Replace with your actual API key
VISION_ENDPOINT = "https://image-caption-app.cognitiveservices.azure.com/"
VISION_URL = VISION_ENDPOINT + "/vision/v3.2/describe?maxCandidates=3"

# ==== Streamlit UI ====
st.title("🧠 AI-Powered Image Caption Generator (Azure Only)")

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
        caption = result["description"]["captions"][0]["text"]
        tags = result["description"].get("tags", [])
        tags_text = ", ".join(tags)

        st.info("🖼 Azure Vision Caption:")
        st.write(caption)
        st.info("🏷 Tags:")
        st.write(tags_text)
    else:
        st.warning("⚠ No caption generated. Please try a different image.")
