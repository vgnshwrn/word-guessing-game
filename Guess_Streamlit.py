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
        }

        /* 🧱 Remove Streamlit default padding */
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
            padding: 10px 0 15px 0;
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.4);
            border-top: 2px solid rgba(255,255,255,0.3); /* creates top blending effect */
            z-index: 9999;
        }

        .school-header img {
            width: 85px;
            height: 85px;
            border-radius: 50px;
            object-fit: cover;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 6px;
        }

        .school-header-text h2 {
            margin: 0;
            color: #1f1f1f;
            font-size: 26px;
            font-weight: 700;
        }

        .school-header-text p {
            margin: 0;
            font-size: 17px;
            color: #333;
        }

        /* 👣 Footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 10px 25px;
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            font-size: 16px;
            color: #2b2b2b;
            border-top: 1px solid rgba(255, 255, 255, 0.4);
        }

        /* 🧩 Space for header/footer */
        .main {
            margin-top: 180px;  /* ✅ adjust for top + logo height */
            margin-bottom: 70px;
        }

        /* 📱 Responsive fix */
        @media (max-width: 768px) {
            .school-header img {
                width: 70px;
                height: 70px;
            }
            .school-header-text h2 {
                font-size: 22px;
            }
            .main {
                margin-top: 200px;
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
        <p>CBSE Senior Secondary – Bodinayakanur</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    Created by <b>Tharika</b>, <b>Gowri</b>, and <b>Thanya Shree</b> – XI Std
</div>
""", unsafe_allow_html=True)

# --- Add space for content below header ---
st.markdown('<div class="main">', unsafe_allow_html=True)


# --- Title and Intro ---
st.title("🎯 Word Guessing Game")
st.write("Guess the hidden word! You have **7 chances** to find it.")

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
if st.button("🔄 Restart Game"):
    common_words = top_n_list("en", 5000)
    valid_words = [w for w in common_words if 4 <= len(w) <= 13]
    st.session_state.secret_word = random.choice(valid_words)
    st.session_state.hidden = ["_"] * len(st.session_state.secret_word)
    st.session_state.chances = 7
    st.session_state.message = "New game started! Guess the word!"
    st.session_state.game_over = False
    st.rerun()