import streamlit as st
import requests
 
API_URL = "http://localhost:8000"
 
st.set_page_config(page_title="Real-Time Translator", layout="centered")
 
st.title("🌐 English to Spanish Translator")
st.markdown("This app translates English text to Spanish and computes BLEU & Perplexity scores.")
 
# Text Input
text_input = st.text_area("✏️ Enter English text below:", height=150)
 
if st.button("Translate"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        # Step 1: Validate input before translation
        validation_response = requests.post(f"{API_URL}/validate", json={"text": text_input})
        if validation_response.status_code == 200:
            validation_result = validation_response.json()
            if validation_result["valid"]:
                with st.spinner("Translating..."):
                    response = requests.post(f"{API_URL}/translate", json={"text": text_input})
                    if response.status_code == 200:
                        data = response.json()

                        st.subheader("✅ Translation Result")
                        st.write(f"**Original:** {data['original_text']}")
                        st.write(f"**Translated:** {data['translated_text']}")
                        st.write(f"**Reference (Hugging Face):** {data['reference_translation']}")
                        st.metric(label="BLEU Score", value=data['bleu_score'])
                        st.metric(label="Perplexity", value=data['perplexity'])
                    else:
                        st.error("Something went wrong with the translation request.")
            else:
                st.error("🚫 Input failed validation.")
                for i, err in enumerate(validation_result["errors"], 1):
                    reason = err["expectation_config"]["_expectation_type"].replace("_", " ").capitalize()
                    sample = err["result"].get("partial_unexpected_list", ["N/A"])[0]
                    st.markdown(f"- ❌ **{reason}** – Problematic value: `{sample}`")
        else:
            st.error("❌ Could not validate the input. Please check the backend.")
 
# Show system metrics
if st.button("📊 Show System Metrics"):
    metrics_response = requests.get(f"{API_URL}/metrics")
    if metrics_response.status_code == 200:
        metrics = metrics_response.json()
        st.subheader("📈 API Usage Metrics")
        st.metric(label="Total Requests", value=metrics['total_requests'])
        st.metric(label="Memory Usage (MB)", value=metrics['current_memory_usage_mb'])
    else:
        st.error("Couldn't fetch system metrics.")
