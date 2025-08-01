# app.py - JEE Question Simplifier
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Master prompt for the AI
MASTER_PROMPT = """# The 'Question De-Coder' Prompt

**Your Role:** You are 'Dost AI', a friendly and super-intelligent study partner for Indian students preparing for the JEE exam. You are an expert at breaking down complex problems into simple, understandable parts. Your language is simple, encouraging Hinglish.

**Your Primary Goal:**
Your ONLY goal is to take a complex Physics, Chemistry, or Maths question (from text or an image) and REPHRASE it. You need to simplify the question's language, break it down, and explain what is being asked, without giving away the solution.

**THE CRITICAL RULE (Lakshman Rekha):**
- **DO NOT** provide the final answer.
- **DO NOT** give the exact formula needed to solve the problem.
- **DO NOT** provide the step-by-step solution.
- Your job is to make the student *think*, not to give them the answer. If the user asks for the answer, you must politely refuse and stick to your role of simplifying the question.

**Your Process:**
1.  **Identify Core Concept:** Pehle, pehchano ki sawaal kis topic se hai (e.g., Rotational Motion, Chemical Equilibrium).
2.  **De-Jargon:** Mushkil words (e.g., 'coefficient of restitution', 'molar conductivity') ko simple bhasha mein samjhao.
3.  **Break it Down:** Poore sawaal ko 2-3 chote-chote hisso mein todo.
4.  **Given & Find:** Saaf-saaf batao ki sawaal mein kya-kya information *di gayi hai* (Given) aur aakhir mein *dhundhna kya hai* (To Find).
5.  **Guiding Question:** End mein ek hint ya ek "sochne wala" sawaal pucho jo student ko sahi direction mein sochne par majboor kare."""

# Configure Google Generative AI
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("⚠️ Google API key nahi mila! Secrets.toml file mein GOOGLE_API_KEY add karo.")
    st.stop()

# Page configuration
st.set_page_config(page_title="JEE Dost AI", page_icon="🧠", layout="wide")

# Main title
st.title("🧠 JEE Dost AI - Sawaal ko Simplify Karo!")

# Model selection
model_choice = st.radio(
    "Choose your AI model:",
    ("Gemini 2.5 Flash (⚡ Fast)", "Gemini 2.5 Pro (🎯 High Accuracy, but slow)"),
    horizontal=True
)

# Set model name based on selection
if "Flash" in model_choice:
    selected_model_name = 'gemini-2.0-flash-exp'
else:
    selected_model_name = 'gemini-1.5-pro'

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📄 Type Question", "🖼️ Upload Image"])

# Initialize variables
user_input = ""
uploaded_image = None
additional_context = ""

with tab1:
    user_input = st.text_area("Apna sawaal yahan type karo:", height=150)

with tab2:
    uploaded_file = st.file_uploader("Sawaal ki photo upload karo:", type=['jpg', 'jpeg', 'png'])
    additional_context = st.text_input("Photo ke saath kuch likhna hai? (Optional)")
    
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

# AI response function
def get_gemini_response(input_text, image, selected_model, prompt):
    """Generate response using Google Gemini AI"""
    try:
        model = genai.GenerativeModel(selected_model)
        
        if image is not None:
            response = model.generate_content([prompt, image, input_text])
        else:
            response = model.generate_content([prompt, input_text])
            
        return response.text
    
    except Exception as e:
        return f"❌ Kuch gadbad hui hai bhai! Error: {str(e)}"

# Main action button
if st.button("Sawaal Simplify Karo ✨", type="primary"):
    # Check if user has provided any input
    if not user_input and uploaded_image is None:
        st.warning("⚠️ Pehle koi sawaal to daal bhai - text ya image!")
    else:
        with st.spinner("Dost AI soch raha hai..."):
            # Prepare input text
            if uploaded_image is not None:
                final_input = additional_context if additional_context else "Please simplify this question from the image."
            else:
                final_input = user_input
            
            # Get AI response
            response = get_gemini_response(
                input_text=final_input,
                image=uploaded_image,
                selected_model=selected_model_name,
                prompt=MASTER_PROMPT
            )
            
            # Display response
            st.markdown("### 🤖 Dost AI ka Response:")
            st.markdown(response)

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ for JEE Warriors! All the best bhai! 🚀*")
