import base64
import os
import streamlit as st

st.set_page_config(page_title="SOLSTONE", layout="wide")

# Initialize session state variables for navigation and data retention
if "page" not in st.session_state:
    st.session_state["page"] = "contact"
if "company_name" not in st.session_state:
    st.session_state["company_name"] = ""
if "contact_name" not in st.session_state:
    st.session_state["contact_name"] = ""
if "company_email" not in st.session_state:
    st.session_state["company_email"] = ""
if "mark_name" not in st.session_state:
    st.session_state["mark_name"] = ""
if "goods_name" not in st.session_state:
    st.session_state["goods_name"] = ""


# Case-insensitive helper to locate and convert texture assets to base64
def get_asset_base64(filename):
    base_dir = os.path.dirname(__file__)
    search_dirs = [os.path.join(base_dir, "assets"), base_dir]
    
    for d in search_dirs:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower() == filename.lower():
                    full_path = os.path.join(d, f)
                    if os.path.isfile(full_path):
                        with open(full_path, "rb") as file_obj:
                            return base64.b64encode(file_obj.read()).decode("utf-8")
    return ""


# Load texture files
bg_b64 = get_asset_base64("background.jpg")
panel_b64 = get_asset_base64("panel.jpg")
btn_b64 = get_asset_base64("buttons.jpg")

# CSS Background Rules
if bg_b64:
    bg_css = f"radial-gradient(circle at 50% 30%, rgba(14, 29, 40, 0.25) 0%, rgba(8, 16, 22, 0.65) 85%), url('data:image/jpeg;base64,{bg_b64}')"
else:
    bg_css = "radial-gradient(circle at 50% 30%, rgba(14, 29, 40, 0.85) 0%, rgba(8, 16, 22, 0.98) 85%)"

if panel_b64:
    panel_css = f"linear-gradient(180deg, rgba(20, 12, 6, 0.35) 0%, rgba(20, 12, 6, 0.65) 100%), url('data:image/jpeg;base64,{panel_b64}')"
else:
    panel_css = "linear-gradient(180deg, rgba(50, 28, 14, 0.96) 0%, rgba(24, 12, 6, 0.98) 100%)"

if btn_b64:
    btn_css = f"linear-gradient(135deg, rgba(255, 255, 255, 0.45) 0%, rgba(200, 220, 235, 0.2) 50%, rgba(255, 255, 255, 0.35) 100%), url('data:image/jpeg;base64,{btn_b64}')"
else:
    btn_css = "linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(200, 220, 235, 0.25) 50%, rgba(255, 255, 255, 0.4) 100%)"

st.markdown(
    f"""
    <style>
    /* 1. GLOBAL HELVETICA TYPOGRAPHY & AGGRESSIVE TOP SPACING REDUCTION */
    .stApp, html, body, [class*="css"] {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }}
    
    /* Hide the blank Streamlit header bar to save space */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* Reduce Streamlit's default top padding dramatically (Pulls boxes to the top) */
    .block-container {{
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
    }}

    /* 2. BACKGROUND WATER TEXTURE */
    .stApp {{
        background-color: #0E1D28 !important;
        background-image: {bg_css} !important;
        background-position: center !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    /* 3. FORCE COLUMNS TO STAY SIDE-BY-SIDE ON NARROW SCREENS */
    div[data-testid="stHorizontalBlock"] {{
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }}

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
        min-width: 0 !important;
        flex: 1 1 auto !important;
    }}

    /* 4. OPAQUE WOOD PANEL CARDS WITH STRICT GLOBAL MAX-WIDTH (660px) */
    form[data-testid="stForm"],
    .stForm,
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #2D1A0E !important;
        background-image: {panel_css} !important;
        background-size: cover !important;
        background-position: center !important;
        padding: 24px 20px 18px 20px !important;
        border: 4px solid #000000 !important;
        border-radius: 6px !important;
        box-shadow: 
            inset 0 0 40px rgba(0, 0, 0, 0.95),
            0px 10px 30px rgba(0, 0, 0, 0.9) !important;
        max-width: 660px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        box-sizing: border-box !important;
    }}

    form[data-testid="stForm"] > div,
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: transparent !important;
    }}

    /* 5. UNIFORM BOLD HELVETICA SUN GOLD MAIN TITLE WITH SUPERSCRIPT TM */
    .sun-gold-title {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        text-align: center;
        font-size: 44px !important;
        font-weight: 900 !important;
        letter-spacing: 6px !important;
        color: #FFD700 !important;
        text-shadow: 
            3px 3px 0px #000000,
            4px 4px 10px rgba(0, 0, 0, 0.95),
            0px 0px 20px rgba(255, 215, 0, 0.5) !important;
        margin-top: 0px;
        margin-bottom: 18px;
        line-height: 1.1;
    }}

    /* 6. INPUT LABELS & FIELDS */
    div.stTextInput {{
        margin-bottom: 8px !important;
    }}

    div.stTextInput > label {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: 800 !important;
        font-size: 13.5px !important;
        letter-spacing: 1.1px !important;
        color: #F8FAFC !important;
        text-shadow: 2px 2px 4px #000000 !important;
    }}

    div.stTextInput > div > div > input {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        border: 1.5px solid rgba(255, 235, 200, 0.45) !important;
        border-radius: 2px !important;
        background-color: rgba(12, 8, 5, 0.88) !important;
        backdrop-filter: blur(4px) !important;
        box-shadow: inset 1px 1px 5px rgba(0, 0, 0, 0.95) !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    div.stTextInput > div > div > input::placeholder {{
        color: #A0AEC0 !important;
        opacity: 0.85 !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    /* PAGE 1 INFO NOTE TEXT */
    .info-note-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #CBD5E1 !important;
        font-size: 11.5px !important;
        font-style: italic !important;
        margin-top: 4px !important;
        margin-bottom: 14px !important;
        text-align: center !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    /* PAGE 2 CONTACT SUMMARY BANNER */
    .user-summary-banner {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #FFD700 !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        text-align: center !important;
        background-color: rgba(8, 8, 8, 0.35) !important;
        backdrop-filter: blur(2px) !important;
        border: 1px solid #5C3A21 !important;
        border-radius: 4px !important;
        padding: 6px 12px !important;
        margin-bottom: 16px !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    /* PAGE 3 QUERY SUMMARY BANNER */
    .query-summary-banner {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #FFD700 !important;
        font-size: 13.5px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-align: center !important;
        background-color: rgba(8, 8, 8, 0.35) !important;
        backdrop-filter: blur(2px) !important;
        border: 1.5px solid #5C3A21 !important;
        border-radius: 4px !important;
        padding: 6px 14px !important;
        margin-bottom: 14px !important;
        text-shadow: 1px 1px 3px #000000 !important;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8) !important;
        word-break: break-word !important;
    }}

    /* SOLID BLACK TEXT LABELS FOR PAGE 3 SUMMARY */
    .query-label {{
        color: #000000 !important;
        font-weight: 900 !important;
        text-shadow: none !important;
        text-decoration: underline !important;
        text-underline-offset: 2px !important;
        text-decoration-thickness: 2px !important;
    }}
    
    .query-divider {{
        color: #000000 !important;
        font-weight: 900 !important;
        text-shadow: none !important;
        margin: 0 6px !important;
    }}

    /* 7. SLEEK, REFINED BUTTON STYLING */
    div.stButton > button,
    div.stFormSubmitButton > button,
    button[data-testid^="baseButton"] {{
        background-image: {btn_css} !important;
        background-size: cover !important;
        background-position: center !important;
        background-blend-mode: overlay !important;
        background-color: rgba(220, 230, 240, 0.45) !important;
        
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;

        border-radius: 3px !important;
        margin-top: 10px !important;
        width: 100% !important;
        
        box-shadow: 
            1px 1px 0px rgba(255, 255, 255, 0.7),
            0px 4px 10px rgba(0, 0, 0, 0.7) !important;
            
        transition: all 0.12s ease-in-out !important;
    }}

    /* STRICT SLEEK HEIGHT (56px) & FLEX CENTERING */
    div[data-testid="stColumn"] div.stFormSubmitButton > button,
    div[data-testid="stColumn"] div.stButton > button {{
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        box-sizing: border-box !important;
    }}

    div.stButton > button p,
    div.stFormSubmitButton > button p,
    button[data-testid^="baseButton"] p {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #1A0F00 !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin: 0 !important;
        text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6) !important;
        white-space: pre-wrap !important;
        text-align: center !important;
    }}

    /* 8. EQUAL FIXED HEIGHT & SCROLLING FOR LEFT/RIGHT BLACK BOXES (INCREASED to 530px) */
    .results-heading {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 15px !important;
        font-weight: 900 !important;
        letter-spacing: 1.2px;
        color: #FFD700 !important;
        margin-top: 0px;
        margin-bottom: 8px;
        line-height: 1.2;
        text-shadow: 2px 2px 4px #000000 !important;
        border-bottom: 1.5px solid #5C3A21;
        padding-bottom: 5px;
    }}

    .results-black-box {{
        background-color: rgba(8, 8, 8, 0.35) !important;
        backdrop-filter: blur(2px) !important;
        border: 1.5px solid #5C3A21 !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        box-shadow: 
            inset 0 0 15px rgba(0, 0, 0, 0.95),
            0px 4px 12px rgba(0, 0, 0, 0.8) !important;
        height: 530px !important;
        min-height: 530px !important;
        max-height: 530px !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}

    /* Scrollbar Styling inside Black Boxes */
    .results-black-box::-webkit-scrollbar {{
        width: 4px;
    }}
    .results-black-box::-webkit-scrollbar-thumb {{
        background: #5C3A21;
        border-radius: 2px;
    }}

    .results-list,
    .results-list ol,
    .results-list li {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 10.5px !important;
        color: #E2E8F0 !important;
        line-height: 1.25 !important;
        word-break: break-word !important;
    }}

    .results-list ol {{
        padding-left: 14px;
        margin: 0;
    }}

    .results-list li {{
        margin-bottom: 2px;
        text-shadow: 1px 1px 3px #000000 !important;
    }}

    .results-list strong {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #FFD700 !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    /* 9. DESCRIPTION PANEL TEXT FORMATTING */
    .desc-section-title {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #FFD700 !important;
        font-size: 12px !important;
        font-weight: 900 !important;
        letter-spacing: 0.8px;
        margin-top: 4px;
        margin-bottom: 4px;
        text-shadow: 2px 2px 4px #000000 !important;
    }}

    .desc-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #F1F5F9 !important;
        font-size: 10px !important;
        line-height: 1.3 !important;
        margin-bottom: 6px;
        text-shadow: 1px 1px 3px #000000 !important;
        word-break: break-word !important;
    }}

    .desc-list,
    .desc-list li {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #E2E8F0 !important;
        font-size: 10px !important;
        line-height: 1.3 !important;
        word-break: break-word !important;
    }}

    .desc-list {{
        padding-left: 12px !important;
        margin-left: 0 !important;
        margin-bottom: 0px !important;
    }}

    .desc-list li {{
        margin-bottom: 4px;
        text-shadow: 1px 1px 3px #000000 !important;
    }}

    .desc-list li.desc-list-green-bold-italic,
    ul.desc-list li.desc-list-green-bold-italic {{
        color: #22C55E !important;
        font-weight: 800 !important;
        font-style: italic !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }}

    hr.desc-hr {{
        border: none !important;
        border-bottom: 1px solid #5C3A21 !important;
        margin: 6px 0 !important;
    }}

    /* 10. GREEN DISCOUNT BANNER & LEGAL DISCLAIMER BOX */
    .green-discount-box {{
        background-color: rgba(5, 5, 5, 0.95) !important;
        border: 2px solid #22C55E !important;
        border-radius: 4px !important;
        padding: 12px 18px !important;
        text-align: center;
        margin-top: 16px !important;
        box-shadow: 
            0px 6px 20px rgba(0,0,0,0.95),
            0px 0px 15px rgba(34, 197, 94, 0.35) !important;
        max-width: 660px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    .green-discount-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #22C55E !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        text-shadow: 1px 1px 3px #000000 !important;
    }}

    .green-discount-price-old {{
        color: #DC2626 !important;
        text-decoration: line-through !important;
        font-weight: 700 !important;
        margin-right: 6px;
    }}

    .green-discount-price-new {{
        color: #4ADE80 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        margin-right: 6px;
    }}

    .green-discount-tag {{
        color: #86EFAC !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
    }}

    .disclaimer-box {{
        background-color: rgba(5, 5, 5, 0.92) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 16px !important;
        margin-top: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.8) !important;
        max-width: 660px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    .disclaimer-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #94A3B8 !important;
        font-size: 10.5px !important;
        line-height: 1.4 !important;
        text-align: left !important;
        margin: 0 !important;
        text-shadow: 1px 1px 2px #000000 !important;
    }}

    .disclaimer-text strong {{
        color: #CBD5E1 !important;
    }}

    /* 11. MOBILE RESPONSIVE MEDIA QUERIES */
    @media (max-width: 768px) {{
        form[data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"],
        .disclaimer-box,
        .green-discount-box {{
            max-width: 100% !important;
            padding: 14px 8px 12px 8px !important;
            margin-bottom: 12px !important;
        }}
        .sun-gold-title {{
            font-size: 28px !important;
            letter-spacing: 3px !important;
            margin-bottom: 10px !important;
        }}
        .query-summary-banner {{
            font-size: 11px !important;
            padding: 4px 6px !important;
            margin-bottom: 10px !important;
        }}
        /* TALLER MOBILE BOXES (Increased to 460px) */
        .results-black-box {{
            height: 460px !important;
            min-height: 460px !important;
            max-height: 460px !important;
            padding: 10px 8px !important;
        }}
        .results-heading {{
            font-size: 12px !important;
            letter-spacing: 0.5px !important;
            margin-bottom: 8px !important;
            padding-bottom: 4px !important;
        }}
        .results-list, .results-list ol, .results-list li {{
            font-size: 9.5px !important;
            line-height: 1.25 !important;
        }}
        .results-list ol {{
            padding-left: 12px !important;
        }}
        .desc-section-title {{
            font-size: 10.5px !important;
            letter-spacing: 0.4px !important;
            margin-top: 4px !important;
            margin-bottom: 4px !important;
        }}
        .desc-text, .desc-list, .desc-list li {{
            font-size: 9.5px !important;
            line-height: 1.3 !important;
        }}
        .desc-list {{
            padding-left: 10px !important;
        }}
    }}
    </style>
""",
    unsafe_allow_html=True,
)


# Helper function to render persistent legal disclaimer
def render_legal_disclaimer():
    st.html(
        """<div class="disclaimer-box">
<p class="disclaimer-text">
<strong>LEGAL DISCLAIMER:</strong> SOLSTONE is an automated search tool for informational purposes only and does not constitute legal advice or formal legal representation. Although our search engine checks extensive federal, commercial, and industry databases, no search tool can guarantee 100% complete coverage or eliminate the risk that an unidentified third party holds prior registered or common law trademark rights.
</p>
</div>"""
    )


# --- PAGE 1: CONTACT INFORMATION FORM ---
if st.session_state["page"] == "contact":
    
    st.markdown("""
    <style>
    div[data-testid="stForm"] div.stFormSubmitButton > button {
        border: 2px solid #000000 !important;
    }
    div[data-testid="stForm"] div.stFormSubmitButton > button:hover {
        border-color: #333333 !important;
        transform: translate(-1px, -1px);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form(key="solstone_contact_panel"):
        st.markdown(
            '<div class="sun-gold-title">SOLSTONE&trade;</div>',
            unsafe_allow_html=True,
        )

        company_input = st.text_input(
            "COMPANY NAME:",
            value=st.session_state["company_name"],
            placeholder="YOUR COMPANY NAME",
        )
        contact_input = st.text_input(
            "CONTACT NAME:",
            value=st.session_state["contact_name"],
            placeholder="YOUR FULL NAME",
        )
        email_input = st.text_input(
            "COMPANY EMAIL:",
            value=st.session_state["company_email"],
            placeholder="NAME@COMPANY.COM",
        )

        st.markdown(
            '<div class="info-note-text">Your information will be used to email you a copy of the results of your searches</div>',
            unsafe_allow_html=True,
        )

        btn_next = st.form_submit_button(
            "PROCEED TO SEARCH TOOL", use_container_width=True
        )

    render_legal_disclaimer()

    if btn_next:
        st.session_state["company_name"] = company_input
        st.session_state["contact_name"] = contact_input
        st.session_state["company_email"] = email_input
        st.session_state["page"] = "search_input"
        st.rerun()

# --- PAGE 2: SEARCH QUERY INPUTS ---
elif st.session_state["page"] == "search_input":
    
    st.markdown("""
    <style>
    /* Styling for Page 2 Buttons */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(1) div.stFormSubmitButton > button,
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(2) div.stFormSubmitButton > button {
        border: 2px solid #000000 !important;
    }
    
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(2) button p {
        font-size: 18px !important;
        line-height: 1 !important;
        margin-top: 1px !important;
        color: #1A0F00 !important;
        text-transform: none !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"] div.stFormSubmitButton > button:hover {
        border-color: #333333 !important;
        transform: translate(-1px, -1px);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form(key="solstone_search_panel"):
        st.markdown(
            '<div class="sun-gold-title">SOLSTONE&trade;</div>',
            unsafe_allow_html=True,
        )

        # Formatted contact summary banner
        c_name = st.session_state.get("contact_name", "").strip() or "Mark"
        c_email = (
            st.session_state.get("company_email", "").strip()
            or "mark@yahoo.com"
        )
        c_comp = (
            st.session_state.get("company_name", "").strip()
            or "ABC Brewing"
        )
        summary_banner = f"{c_name} ({c_email}) from {c_comp}"

        st.markdown(
            f'<div class="user-summary-banner">{summary_banner}</div>',
            unsafe_allow_html=True,
        )

        mark_input = st.text_input(
            "MARK:",
            value=st.session_state["mark_name"],
            placeholder="INSERT DESIRED NAME HERE",
        )
        goods_input = st.text_input(
            "Goods:",
            value=st.session_state["goods_name"],
            placeholder="BEER",
        )

        btn_col_search, btn_col_back = st.columns([5, 1], gap="small")
        
        with btn_col_search:
            btn_search = st.form_submit_button(
                "PERFORM FREE SEARCH", use_container_width=True
            )
        with btn_col_back:
            btn_back = st.form_submit_button("↻", use_container_width=True)

    render_legal_disclaimer()

    if btn_search:
        st.session_state["mark_name"] = mark_input
        st.session_state["goods_name"] = goods_input
        st.session_state["page"] = "results"
        st.rerun()
        
    if btn_back:
        st.session_state["mark_name"] = mark_input
        st.session_state["goods_name"] = goods_input
        st.session_state["page"] = "contact"
        st.rerun()

# --- PAGE 3: SEARCH RESULTS & COVERAGE ---
elif st.session_state["page"] == "results":
    
    st.markdown("""
    <style>
    /* PAGE 3: LEFT PREMIUM BUTTON */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(1) div.stFormSubmitButton > button {
        border: 2px solid #16A34A !important;
        padding: 4px 8px !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(1) button p {
        color: #15803D !important;
        font-size: 11px !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(1) div.stFormSubmitButton > button:hover {
        border-color: #22C55E !important;
        transform: translate(-1px, -1px); box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.9) !important;
    }

    /* PAGE 3: MIDDLE & RIGHT BUTTONS */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(2) div.stFormSubmitButton > button,
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(3) div.stFormSubmitButton > button {
        border: 2px solid #000000 !important;
        padding: 4px 4px !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(3) button p {
        font-size: 18px !important;
        line-height: 1 !important;
        margin-top: 1px !important;
        text-transform: none !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(2) div.stFormSubmitButton > button:hover,
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="stColumn"]:nth-child(3) div.stFormSubmitButton > button:hover {
        border-color: #333333 !important;
        transform: translate(-1px, -1px);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form(key="solstone_results_panel"):
        st.markdown(
            '<div class="sun-gold-title">SOLSTONE&trade;</div>', unsafe_allow_html=True
        )

        # QUERY SUMMARY BOX BETWEEN TITLE AND SEARCH BOXES
        s_mark = st.session_state.get("mark_name", "").strip() or "BEER BRAND"
        s_goods = st.session_state.get("goods_name", "").strip() or "BEER"
        
        query_banner = f'<span class="query-label">Mark:</span> {s_mark} <span class="query-divider">|</span> <span class="query-label">Goods:</span> {s_goods}'

        st.markdown(
            f'<div class="query-summary-banner">{query_banner}</div>',
            unsafe_allow_html=True,
        )

        res_col, cov_col = st.columns([1.1, 0.9], gap="small")

        # LEFT COLUMN: SEARCH RESULTS
        with res_col:
            st.html("""<div class="results-black-box">
<div class="results-heading">SEARCH RESULTS:</div>
<div class="results-list">
<ol>
<li><strong>BEER BRAND</strong> by Competing Brewery</li>
<li><strong>WINE BRAND</strong> by Competing Winery</li>
<li><strong>SPIRITS BRAND</strong> by Competing Distillery</li>
<li><strong>BAR BRAND</strong> by Fancy Restaurant</li>
<li><strong>ALE CRAFT</strong> by Mountain Ales LLC</li>
<li><strong>LAGER KING</strong> by Crown Brewing Co</li>
<li><strong>CIDER HAVEN</strong> by Valley Cider Works</li>
<li><strong>MEAD VAULT</strong> by Nordic Meadery</li>
<li><strong>BOURBON RIDGE</strong> by Heritage Distilling</li>
<li><strong>VODKA PURE</strong> by Crystal Spirits Inc</li>
<li><strong>TEQUILA SOL</strong> by Agave Sun Spirits</li>
<li><strong>RUM TROPIC</strong> by Caribbean Imports</li>
<li><strong>GIN BOTANICA</strong> by Herbal Craft Distillers</li>
<li><strong>PUB HOUSE</strong> by Corner Pub LLC</li>
<li><strong>TASTING ROOM</strong> by Coastal Vineyards</li>
<li><strong>BREW PUB</strong> by Downtown Brew Co</li>
<li><strong>SELTZER SPLASH</strong> by Refresh Beverages</li>
<li><strong>COCKTAIL CLUB</strong> by Craft Cocktails Corp</li>
<li><strong>HARD TEA</strong> by Sunny Orchard Teas</li>
<li><strong>LOUNGE NATION</strong> by Nightlife Hospitality</li>
</ol>
</div>
</div>""")

        # RIGHT COLUMN: SEARCH COVERAGE
        with cov_col:
            st.html("""<div class="results-black-box">
<div class="results-heading">SEARCH COVERAGE:</div>
<div class="desc-section-title">🔍 FREE SEARCH</div>
<div class="desc-text">
Enjoy this free sneak-peek at our clearance tool. If things look good here, we suggest you consider trying our premium tool to fully vet the availability of your mark before committing to it.<br><br>
</div>

<hr class="desc-hr">

<div class="desc-section-title">🔍 PREMIUM SEARCH</div>
<ul class="desc-list">
<li>Hand-curated database with millions of records relevant to the beverage alcohol business.</li>
<li>Proprietary search engine designed to identify the closest competitor brands.</li>
<li>Carefully crafted by trademark attorney with 15 years in the beverage alcohol business.</li>
<li>Your custom PDF report demonstrates you did your due diligence efforts in selecting your name.</li>
<li class="desc-list-green-bold-italic">Temporary 50% discount to conference attendees</li>
</ul>
</div>""")

        # BOTTOM BUTTON ROW (1/3 / 1/3 / 1/3 Spacing)
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1], gap="small")
        
        with btn_col1:
            btn_premium = st.form_submit_button(
                "$ PREMIUM UPGRADE $", use_container_width=True
            )
        with btn_col2:
            btn_new_search = st.form_submit_button(
                "NEW SEARCH", use_container_width=True
            )
        with btn_col3:
            btn_refresh = st.form_submit_button(
                "↻", use_container_width=True
            )

    if btn_premium:
        st.html(
            """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" type="audio/mpeg"></audio>"""
        )
        st.html("""<div class="green-discount-box">
<span class="green-discount-text">
Upgrading to Premium Search: <span class="green-discount-price-old">$100</span> <span class="green-discount-price-new">$50</span> <span class="green-discount-tag">(ATTENDEE DISCOUNT)</span>
</span>
<p style="color: #E2E8F0; font-size: 13px; margin-top: 6px; margin-bottom: 0;">Accessing 40+ years of TTB COLAs, food & beverage registries, and common law databases...</p>
</div>""")

    if btn_new_search:
        st.session_state["page"] = "search_input"
        st.rerun()
        
    if btn_refresh:
        st.session_state["page"] = "contact"
        st.rerun()

    # PERSISTENT LEGAL DISCLAIMER
    render_legal_disclaimer()
