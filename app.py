import os
import streamlit as st
from shopping_agent import agent

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Reliable CSS using st.markdown with !important overrides ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ─── Root variables ─────────────────────────────── */
:root {
    --bg:        #f5f3ef;
    --surface:   #ffffff;
    --border:    #e2dfd8;
    --accent:    #c8622a;
    --accent2:   #2a6cc8;
    --text:      #1c1a18;
    --muted:     #6b6761;
    --user-bg:   #eef4fd;
    --user-bd:   #b8d0f0;
    --bot-bg:    #ffffff;
    --bot-bd:    #e2dfd8;
    --radius:    14px;
}

/* ─── Global background ──────────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
}
            
/* Hero Section */
.hero {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 52px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 20px;
    opacity: 0.95;
}

/* ─── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #fff !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
}

/* ─── Main content width ─────────────────────────── */
.main .block-container {
    max-width: 820px !important;
    padding: 2rem 2.5rem 5rem !important;
    margin: 0 auto !important;
}

/* ─── Chat messages ──────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bot-bg) !important;
    border: 1px solid var(--bot-bd) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.75rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.94rem !important;
    line-height: 1.7 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

/* User message distinction via avatar area hack */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--user-bg) !important;
    border-color: var(--user-bd) !important;
}

/* ─── Avatar icons ───────────────────────────────── */
[data-testid="chatAvatarIcon-user"] svg {
    fill: var(--accent2) !important;
}
[data-testid="chatAvatarIcon-assistant"] svg {
    fill: var(--accent) !important;
}
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {
    border-radius: 50% !important;
    padding: 4px !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #dbeafe !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: #fde8d8 !important;
}

/* ─── Chat input ─────────────────────────────────── */
[data-testid="stChatInputTextArea"],
textarea[data-testid="stChatInputTextArea"],
.stChatInput textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.94rem !important;
    border-radius: var(--radius) !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    padding: 0.85rem 1rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="stChatInputTextArea"]:focus,
.stChatInput textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,98,42,0.12) !important;
    outline: none !important;
}

/* ─── Chat input container ───────────────────────── */
[data-testid="stBottom"] {
    background: var(--bg) !important;
    border-top: 1px solid var(--border) !important;
    padding: 0.75rem 0 !important;
}

/* ─── Buttons ────────────────────────────────────── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border-radius: 10px !important;
    border: 1.5px solid var(--accent) !important;
    color: var(--accent) !important;
    background: #fff7f3 !important;
    padding: 0.55rem 1.1rem !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #fde8d8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 8px rgba(200,98,42,0.15) !important;
}

/* ─── File uploader ──────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: #faf9f7 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] * {
    font-family: 'DM Sans', sans-serif !important;
}

/* ─── Divider ────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ─── Spinner text ───────────────────────────────── */
[data-testid="stSpinner"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--muted) !important;
}

/* ─── Sidebar typography ─────────────────────────── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text) !important;
    font-size: 1.1rem !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .caption {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    line-height: 1.5 !important;
}

/* ─── Image in sidebar ───────────────────────────── */
[data-testid="stSidebar"] img {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* ─── Scrollbar ──────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #ccc9c2; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #b0aca5; }
</style>
""", unsafe_allow_html=True)


# ── Custom header using HTML (bypasses st.title styling issues) ───────────────
st.markdown("""
<div style="
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.25rem;
    padding-bottom: 0;
">
    <span style="font-size: 2rem;">🛒</span>
    <div>
        <div style="
            font-family: 'DM Serif Display', serif;
            font-size: 1.75rem;
            color: #1c1a18;
            line-height: 1.2;
        ">AI Shopping Assistant</div>
        <div style="
            font-family: 'DM Sans', sans-serif;
            font-size: 0.875rem;
            color: #6b6761;
            margin-top: 2px;
        ">Tell me what you want — I'll search, rate, and order the best match for you.</div>
    </div>
</div>
<hr style="border: none; border-top: 1px solid #e2dfd8; margin: 1rem 0 1.25rem;" />
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 0.25rem;">
        <span style="font-size: 1.4rem;">🖼️</span>
        <span style="
            font-family: 'DM Serif Display', serif;
            font-size: 1.1rem;
            color: #1c1a18;
            font-weight: 600;
            margin-left: 6px;
            vertical-align: middle;
        ">Shop by Image</span>
    </div>
    <p style="font-size:0.82rem; color:#6b6761; margin-bottom:0.75rem; font-family:'DM Sans',sans-serif;">
        Upload a photo and I'll find similar items in our store.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload product image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.image(uploaded_file, use_container_width=True, caption=uploaded_file.name)

    if uploaded_file and st.button("🔍  Find similar products", use_container_width=True):
        resources_dir = os.path.join(os.path.dirname(__file__), "resources")
        os.makedirs(resources_dir, exist_ok=True)
        image_path = os.path.join(resources_dir, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        prompt = (
            f"I uploaded a product image. "
            f"Please analyze it and find similar products in the store. "
            f"Image path: {image_path}"
        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_image = uploaded_file.name
        st.rerun()


# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 3rem 1rem;
        color: #9c9891;
        font-family: 'DM Sans', sans-serif;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🛍️</div>
        <div style="font-size: 1rem; font-weight: 500; color: #6b6761; margin-bottom: 0.4rem;">
            Start your shopping journey
        </div>
        <div style="font-size: 0.85rem; max-width: 320px; margin: 0 auto; line-height: 1.6;">
            Try <em>"organic honey under $15 with 4+ stars"</em> or upload an image on the left.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Render chat history ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user" and msg["content"].startswith("I uploaded a product image"):
            filename = os.path.basename(msg["content"].split("Image path:")[-1].strip())
            st.markdown(f"🖼️ &nbsp;**Searching by image:** `{filename}`")
        else:
            st.markdown(msg["content"].replace("$", r"\$"))


# ── Run agent on pending image upload ─────────────────────────────────────────
if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
    and "pending_image" in st.session_state
):
    with st.chat_message("assistant"):
        with st.spinner("Analyzing image and searching…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))

    st.session_state.messages.append({"role": "assistant", "content": response})
    del st.session_state.pending_image
    st.rerun()


# ── Text input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("e.g. I want organic honey under $15 with 4+ rating"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()