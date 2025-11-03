import streamlit as st
from wordfreq import top_n_list
import random
import base64

# --- Setup ---
st.set_page_config(page_title="🎯 Word Guessing Game", page_icon="🧩", layout="centered")

# --- Encode logo to Base64 (works on cloud too) ---
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("logo.png")  # Keep logo.png in same folder

# --- Global Styles for Header, Background, Footer ---
st.markdown("""
    <style>
        /* 🌈 Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #c0e3ff, #e4b8ff, #ffd6a5);
            background-attachment: fixed;
            font-family: 'Helvetica Neue', sans-serif;
            color: #222;
        }

        /* Remove Streamlit default padding */
        .block-container {
            padding-top: 0 !important;
        }

        /* 📌 Fixed Glass Header */
        .school-header {
            position: fixed;
            top: 60px;
            left: 0;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 10px 0 6px 0;
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.4);
            border-top: 2px solid rgba(255,255,255,0.3);
            z-index: 9999;
        }

        .school-header img {
            width: 85px;
            height: 85px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 4px;
        }

        .school-header-text h2 {
            margin: 0;
            color: #1f1f1f;
            font-size: 34px;
            font-weight: 700;
            line-height: 1.05;
        }

        .school-header-text h3 {
            margin-top: -4px;
            font-size: 18px;
            color: #333;
            font-weight: 500;
        }

        /* 👣 Footer (glass effect same as header) */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 10px 25px;
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-top: 1px solid rgba(255, 255, 255, 0.4);
            font-size: 16px;
            color: #1a1a1a;
            z-index: 9999;
        }

        /* 🧩 Main Content */
        .main {
            margin-top: 280px;
            margin-bottom: 100px;
            text-align: center;
        }

        /* 🎯 Center and style main headings */
        h1, div[data-testid="stMarkdownContainer"] {
            text-align: center !important;
        }

        h1 {
            color: #202020;
            font-size: 40px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
        }

        p {
            font-size: 30px;
            color: #222;
            text-align: left !important;
        }

        /* Center st.text() content */
        div[data-testid="stText"] > div {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 26px;
            letter-spacing: 6px;
            color: #1f1f1f;
        }

        /* Center buttons horizontally */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Style buttons */
        .stButton>button {
            background: linear-gradient(135deg, #e4b8ff, #ffd6a5);
            border: none;
            color: #1f1f1f;
            font-weight: 600;
            padding: 0.6em 1.2em;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            transition: 0.3s ease;
            display: block;
            margin: 10px auto;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #ffd6a5, #e4b8ff);
        }

        /* 📱 Responsive fix */
        @media (max-width: 768px) {
            .school-header img {
                width: 70px;
                height: 70px;
            }
            .school-header-text h2 {
                font-size: 26px;
            }
            .school-header-text h3 {
                font-size: 18px;
            }
            .main {
                margin-top: 240px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Header (Logo on Top, Text Below) ---
st.markdown(f"""
<div class="school-header">
    <img src="data:image/png;base64,{logo_base64}" alt="School Logo">
    <div class="school-header-text">
        <h2>The Spice Valley Public School</h2>
        <h3>CBSE Senior Secondary – Bodinayakanur</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    Created by <b>Tharika Meenakshi N</b>, <b>Gowri Shree P</b>, and <b>Thanya Shree S</b> – XI Std
</div>
""", unsafe_allow_html=True)

# --- Add space for content below header ---
st.markdown('<div class="main">', unsafe_allow_html=True)


# --- Title and Intro ---
st.title("🎯 Word Guessing Game")
st.subheader("Guess the hidden word! You have **7 chances** to find it.")

# --- Game Initialization (Session State) ---
if "secret_word" not in st.session_state:
    common_words = top_n_list("en", 5000)
    valid_words = [w for w in common_words if 4 <= len(w) <= 13]
    st.session_state.secret_word = random.choice(valid_words)
    st.session_state.hidden = ["_"] * len(st.session_state.secret_word)
    st.session_state.chances = 7
    st.session_state.message = "Let's begin!"
    st.session_state.game_over = False

# --- Display Word ---
st.subheader("Word Progress:")
st.text(" ".join(st.session_state.hidden))
st.write(f"Chances left: **{st.session_state.chances}**")


# --- Input from user ---
guess = st.text_input("Enter a letter or the full word:", key="guess_input")

# --- When user presses the 'Guess' button ---
if st.button("Submit Guess") and not st.session_state.game_over:

    secret_word = st.session_state.secret_word
    hidden = st.session_state.hidden
    chances = st.session_state.chances
    message = ""

    if not guess:
        st.warning("Please enter a guess before submitting.")
    else:
        # Full word guess
        if secret_word.lower() == guess.lower():
            st.session_state.message = "🎉 Wow... You found the word! Thank you for your time!"
            st.session_state.hidden = list(secret_word)
            st.session_state.game_over = True

        # Multi-letter guess (not full word)
        elif len(guess) >= 2:
            st.session_state.message = "Kindly enter letter by letter..."

        # Single-letter guess
        else:
            if guess.lower() in secret_word.lower():
                correct = False
                for i in range(len(secret_word)):
                    if secret_word[i].lower() == guess.lower() and hidden[i] == "_":
                        hidden[i] = guess.lower()
                        correct = True
                st.session_state.hidden = hidden
                if correct:
                    st.session_state.message = "Good! Letter is in the word."
                else:
                    st.session_state.message = "⚠️ You already guessed that letter!"
            else:
                st.session_state.chances -= 1
                st.session_state.message = f"❌ OOPS... Wrong Letter. {st.session_state.chances} chances left."

        # Game over conditions
        if "_" not in st.session_state.hidden:
            st.session_state.message = "🎉 Wow... You found the word! Thank you for your time!"
            st.session_state.game_over = True
            st.balloons()
        elif st.session_state.chances == 0:
            st.session_state.message = f"💀 Game Over! The word was **{secret_word}**."
            st.session_state.hidden = list(secret_word)
            st.session_state.game_over = True

# --- Display Current Message ---
st.info(st.session_state.message)
st.write(" ".join(st.session_state.hidden))

# --- Restart Game Button ---
if st.button("Restart Game"):
    common_words = top_n_list("en", 5000)
    valid_words = [w for w in common_words if 4 <= len(w) <= 13]
    st.session_state.secret_word = random.choice(valid_words)
    st.session_state.hidden = ["_"] * len(st.session_state.secret_word)
    st.session_state.chances = 7
    st.session_state.message = "New game started! Guess the word!"
    st.session_state.game_over = False
    st.rerun()