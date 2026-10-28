import os
import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Solstone AI | IP & Compliance Engine",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- CUSTOM CSS: COMPACT, SQUARE, TEXT-WRAPPED & MOBILE FRIENDLY ---
st.markdown("""
<style>
    /* Clean Top Padding for Mobile */
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 100vw; overflow-x: hidden; }
    div[data-testid="stSidebarNav"] { display: none; }
    
    /* Enforce Strict Rectangular Square Edges (No Rounded Corners) */
    .stDataFrame, div[data-testid="stVerticalBlockBorderWrapper"], .stAlert, div[data-testid="stExpander"], .stButton>button, .stPopover>button {
        border-radius: 0px !important;
    }
    
    /* Sleek Sidebar Buttons */
    .stButton>button {
        text-align: left;
        border: 1px solid transparent;
        box-shadow: none;
        background-color: transparent;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    .stButton>button:hover { background-color: #f1f5f9; color: #0f172a; border-color: #cbd5e1; }
    
    /* Primary buttons */
    button[kind="primary"] {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: 600 !important;
        text-align: center !important;
        border: 1px solid #1d4ed8 !important;
    }
    button[kind="primary"]:hover { background-color: #1d4ed8 !important; }
    
    /* Compact, Wide, Square License Cards */
    .license-card {
        border: 1px solid #334155;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 8px 12px; /* Minimized vertical padding */
        margin-bottom: 4px; /* Minimized lines/gaps between boxes */
        display: flex;
        flex-direction: column; 
        gap: 4px;
        border-radius: 0px !important;
        width: 100%;
    }
    
    .license-title { font-size: 1.0rem; font-weight: 700; margin-bottom: 0px; }
    .license-meta { font-size: 0.85rem; color: #94a3b8; margin-bottom: 2px; }
    /* Force text to wrap to prevent scrolling */
    .license-endorsements { 
        font-size: 0.85rem; 
        line-height: 1.3; 
        white-space: normal !important; 
        word-wrap: break-word !important; 
        overflow-wrap: break-word !important;
    }
    
    h1, h2, h3 { color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* Ensure tables don't break layout on mobile */
    .stDataFrame { overflow-x: auto; }
</style>
""", unsafe_allow_html=True)

# --- FULL MOCK DATA: 3 EXAMPLE ENTITIES + 1 FREE FORM ---
ENTITIES_DATA = {
    "Wyngman Brewing Co.": {
        "company": "Wyngman Brewing Company LLC",
        "hq": "Denver, CO",
        "type": "Craft Brewery (Manufacturer)",
        "uuid": "ENT-8924-WYNGMAN",
        "default_context": ["JURIS - COLORADO (CO)", "COMMODITY - BEER", "LICENSE - BREWERY", "TIER - MANUFACTURER"],
        "deadlines": [
            {"type": "LICENSE", "severity": "HIGH", "text": "COLORADO BREWERY LICENSE EXPIRES 12/01/2026", "action": "Submit Renewal Form DR 8404"},
            {"type": "TRADEMARK", "severity": "CRITICAL", "text": "USPTO OA DEADLINE - WYNGMAN HAZY - 11/05/2026", "action": "File Response to Office Action"},
            {"type": "TAX", "severity": "NORMAL", "text": "TTB Q3 EXCISE TAX RETURN DUE 10/29/2026", "action": "Reconcile Operational Barrelage"}
        ],
        "licenses": [
            {
                "jurisdiction": "Federal (US)",
                "license_name": "TTB Commercial Brewer's Notice",
                "id_num": "BR-CO-WYNG-01",
                "issued": "2021-04-12",
                "expires": "Continuous Bonded",
                "status": "VALID",
                "endorsements": "Alternating Proprietor Host, Pilot Brewery Notice (27 CFR § 25.261), Bulk Malt Beverage Transfer in Bond Authorized",
                "context_tag": "LICENSE - COMMERCIAL BREWER'S NOTICE"
            },
            {
                "jurisdiction": "Colorado (CO)",
                "license_name": "Manufacturer - Malt Liquor",
                "id_num": "03-88491-0001",
                "issued": "2021-06-01",
                "expires": "2026-12-01",
                "status": "RENEWAL DUE",
                "endorsements": "Wholesale Self-Distribution Privilege, Sidewalk Café / Streatery Local Outdoor Seating Endorsement, Non-Contiguous Storage Premises",
                "context_tag": "LICENSE - BREWERY (MANUFACTURER)"
            },
            {
                "jurisdiction": "Denver (CO)",
                "license_name": "Local Liquor Sales Room Permit",
                "id_num": "LIC-2024-00918",
                "issued": "2022-02-15",
                "expires": "2027-02-15",
                "status": "ACTIVE",
                "endorsements": "Patio / Summer Garden Outdoor Perimeter Approval, Live Entertainment & Acoustic Music Authorization, ABC Manager Endorsement (3 Managers)",
                "context_tag": "LICENSE - LOCAL SALES ROOM"
            }
        ],
        "brands": [
            {"Brand Name": "Wyngman Hazy IPA", "Class": "Class 032 (Beer)", "TTB COLA": "23100001000122", "TM Status": "Registered (Reg #97412894)", "States Registered": "CO, VA, TX, WY"},
            {"Brand Name": "Wyngman Imperial Porter", "Class": "Class 032 (Beer)", "TTB COLA": "24018001000842", "TM Status": "UNPROTECTED (Unregistered)", "States Registered": "CO"},
            {"Brand Name": "Mile High Crisp Lager", "Class": "Class 032 (Beer)", "TTB COLA": "22099001000455", "TM Status": "Pending (Pub for Opp)", "States Registered": "CO, WY"}
        ],
        "distributors": [
            {"Distributor / Wholesaler": "Front Range Beverage Wholesalers", "State": "CO", "Territory": "Denver Metro, Boulder, Larimer", "Exclusivity": "Exclusive Franchise Territory", "Agreement": "2021-09-01"},
            {"Distributor / Wholesaler": "Old Dominion Craft Distributing", "State": "VA", "Territory": "Northern Virginia & Richmond Metro", "Exclusivity": "Exclusive Franchise Territory", "Agreement": "2023-03-15"}
        ],
        "price_postings": [
            {"Jurisdiction": "CA ABC", "Product / SKU": "Wyngman Hazy IPA (24/12oz Cans)", "Filing Status": "Active Posting", "Case FOB": "$28.50", "Effective Date": "2026-08-01"},
            {"Jurisdiction": "CA ABC", "Product / SKU": "Wyngman Imperial Porter (1/2 BBL Keg)", "Filing Status": "Active Posting", "Case FOB": "$145.00", "Effective Date": "2026-08-01"},
            {"Jurisdiction": "ID ISP", "Product / SKU": "Wyngman Hazy IPA (24/12oz Cans)", "Filing Status": "Price Schedule Filed", "Case FOB": "$27.90", "Effective Date": "2026-09-15"}
        ],
        "owners": [
            {"Name": "Daniel Christopherson", "Title": "Managing Partner & CEO", "Equity": "60.0%", "Background": "Approved (CO LED & TTB)"},
            {"Name": "Summit Beverage Ventures LLC", "Title": "Holding Company / Member", "Equity": "30.0%", "Background": "Disclosed Entity"},
            {"Name": "Robert Vance", "Title": "Master Brewer & VP", "Equity": "10.0%", "Background": "Approved (TTB Notice)"}
        ]
    },
    "Blue Ridge Cellars LLC": {
        "company": "Blue Ridge Cellars LLC",
        "hq": "Charlottesville, VA",
        "type": "Farm Winery & Estate (Manufacturer)",
        "uuid": "ENT-4102-BLUERIDGE",
        "default_context": ["JURIS - VIRGINIA (VA)", "COMMODITY - WINE", "LICENSE - FARM WINERY", "CONCEPT - DIRECT-TO-CONSUMER"],
        "deadlines": [
            {"type": "LICENSE", "severity": "NORMAL", "text": "VA FARM WINERY ANNUAL TAX RETURN DUE 12/15/2026", "action": "Calculate In-State Farm Fruit %"},
            {"type": "TRADEMARK", "severity": "HIGH", "text": "SECTION 8 AFFIDAVIT WINDOW OPENS - 11/20/2026", "action": "Collect Current In-Commerce Specimens"}
        ],
        "licenses": [
            {
                "jurisdiction": "Federal (US)",
                "license_name": "TTB Bonded Winery / Wine Cellar",
                "id_num": "BW-VA-4102",
                "issued": "2018-03-10",
                "expires": "Continuous Bonded",
                "status": "VALID",
                "endorsements": "Taxpaid Wine Bottling House, Bonded Wine Premises Cellarage Privileges",
                "context_tag": "LICENSE - BONDED WINERY"
            },
            {
                "jurisdiction": "Virginia (VA)",
                "license_name": "Farm Winery Class A",
                "id_num": "04-99120-001",
                "issued": "2018-05-20",
                "expires": "2027-05-20",
                "status": "ACTIVE",
                "endorsements": "Remote Tasting Room Authorization (up to 5), Vineyard Pavilion Streatery & Terrace Sales, Direct-to-Retailer Self-Distribution",
                "context_tag": "LICENSE - FARM WINERY"
            },
            {
                "jurisdiction": "Colorado (CO)",
                "license_name": "Winery Direct Shipper's Permit",
                "id_num": "WDS-2020-0192",
                "issued": "2020-11-04",
                "expires": "2026-11-04",
                "status": "RE চুক্তি DUE",
                "endorsements": "Direct-To-Consumer Common Carrier Interstate Fulfillment Authorization",
                "context_tag": "LICENSE - WINERY DIRECT SHIPPER"
            }
        ],
        "brands": [
            {"Brand Name": "Shenandoah Valley Viognier", "Class": "Class 033 (Wine)", "TTB COLA": "21045001000119", "TM Status": "Registered (Reg #94582910)", "States Registered": "VA, NY, CO, MD"},
            {"Brand Name": "Monticello Reserve Cabernet", "Class": "Class 033 (Wine)", "TTB COLA": "22180001000341", "TM Status": "Registered (Reg #96281744)", "States Registered": "VA, MD"}
        ],
        "distributors": [
            {"Distributor / Wholesaler": "Dominion Wine & Spirits Merchants", "State": "VA", "Territory": "Statewide Commonwealth of Virginia", "Exclusivity": "Exclusive Primary Source", "Agreement": "2018-10-01"},
            {"Distributor / Wholesaler": "Empire Merchant Wholesale NY", "State": "NY", "Territory": "New York City & Long Island", "Exclusivity": "Non-Exclusive Territory", "Agreement": "2022-01-10"}
        ],
        "price_postings": [
            {"Jurisdiction": "NY SLA", "Product / SKU": "Shenandoah Valley Viognier (12/750ml)", "Filing Status": "Schedule Filed", "Case FOB": "$160.00", "Effective Date": "2026-09-01"},
            {"Jurisdiction": "NY SLA", "Product / SKU": "Monticello Reserve Cabernet (12/750ml)", "Filing Status": "Schedule Filed", "Case FOB": "$240.00", "Effective Date": "2026-09-01"}
        ],
        "owners": [
            {"Name": "Eleanor Sterling", "Title": "Managing Member & Vintner", "Equity": "85.0%", "Background": "Approved (VA ABC)"},
            {"Name": "Carter Sterling", "Title": "Estate Vineyard Manager", "Equity": "15.0%", "Background": "Approved (VA ABC)"}
        ]
    },
    "High Peak Spirits Co.": {
        "company": "High Peak Distilling Co. LLC",
        "hq": "Bozeman, MT",
        "type": "Distilled Spirits Plant (DSP)",
        "uuid": "ENT-6729-HIGHPEAK",
        "default_context": ["JURIS - MONTANA (MT)", "COMMODITY - SPIRITS", "LICENSE - DISTILLERY", "TIER - MANUFACTURER"],
        "deadlines": [
            {"type": "LICENSE", "severity": "CRITICAL", "text": "MONTANA DOR DSP LICENSE EXPIRES 11/01/2026", "action": "Submit Annual State Renewal"},
            {"type": "COMPLIANCE", "severity": "NORMAL", "text": "MONTHLY DSP STORAGE REPORT (TTB 5110.28) DUE 11/10/2026", "action": "Transmit via Pay.gov"}
        ],
        "licenses": [
            {
                "jurisdiction": "Federal (US)",
                "license_name": "Distilled Spirits Plant (DSP)",
                "id_num": "DSP-MT-20019",
                "issued": "2019-09-15",
                "expires": "Continuous Bonded",
                "status": "VALID",
                "endorsements": "DSP Beverage Distiller, DSP Processor & Rectifier, Bonded Spirits Warehouseman Storage",
                "context_tag": "LICENSE - DISTILLED SPIRITS PLANT"
            },
            {
                "jurisdiction": "Montana (MT)",
                "license_name": "Micro-Distillery Manufacturing License",
                "id_num": "MT-DSP-882",
                "issued": "2019-11-01",
                "expires": "2026-11-01",
                "status": "RENEWAL DUE",
                "endorsements": "On-Premises Sample Room (2 oz individual limit per day), Direct Bottle Sales to Consumers (up to 4.5L per day)",
                "context_tag": "LICENSE - MICRO-DISTILLERY"
            }
        ],
        "brands": [
            {"Brand Name": "High Peak Glacier Bourbon", "Class": "Class 033 (Spirits)", "TTB COLA": "20112001000981", "TM Status": "Registered (Reg #91028394)", "States Registered": "MT, CA, ID, WY"},
            {"Brand Name": "Alpine Botanical Gin", "Class": "Class 033 (Spirits)", "TTB COLA": "21305001000412", "TM Status": "Registered (Reg #93847120)", "States Registered": "MT, ID"}
        ],
        "distributors": [
            {"Distributor / Wholesaler": "Montana Liquor Distribution Center", "State": "MT", "Territory": "Statewide Monopoly Bailment Warehouse", "Exclusivity": "Control State Agency Distribution", "Agreement": "2020-02-01"}
        ],
        "price_postings": [
            {"Jurisdiction": "MT DOR Liquor", "Product / SKU": "High Peak Glacier Bourbon (6/750ml)", "Filing Status": "Monopoly Bailment Quote", "Case FOB": "$132.00", "Effective Date": "2026-07-01"}
        ],
        "owners": [
            {"Name": "Marcus Thorne", "Title": "Founder & Master Distiller", "Equity": "70.0%", "Background": "Approved (TTB & MT DOR)"},
            {"Name": "Gallatin Capital Partners", "Title": "Angel Investment Fund", "Equity": "30.0%", "Background": "Institutional Filing"}
        ]
    },
    "Free Form": {
        "company": "Free Form Exploration (Ad-Hoc Session)",
        "hq": "Custom / Unbound",
        "type": "Free Form Regulatory & IP Sandbox",
        "uuid": "ENT-FREEFORM-UNBOUND",
        "default_context": ["JURIS - FEDERAL (US)", "COMMODITY - BEER", "LICENSE - BREWERY"],
        "deadlines": [],
        "licenses": [],
        "brands": [],
        "distributors": [],
        "price_postings": [],
        "owners": []
    }
}

# --- SESSION STATE INITIALIZATION ---
if "current_company" not in st.session_state:
    st.session_state.current_company = "Wyngman Brewing Co."
if "nav_section" not in st.session_state:
    st.session_state.nav_section = "SUMMARY"
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Licenses"
if "copilot_open" not in st.session_state:
    st.session_state.copilot_open = False
if "active_context" not in st.session_state:
    st.session_state.active_context = ["JURIS - COLORADO (CO)", "COMMODITY - BEER", "LICENSE - BREWERY"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Solstone RagnarBox active. Your query scope is locked to the active context tags."}
    ]

if "review_data" not in st.session_state:
    st.session_state.review_data = pd.DataFrame([
        {"Select": True, "Source": "USPTO", "Matched Mark": "WINGMAN BREWING", "Class": "Class 032", "Status": "LIVE", "Risk Score": 0.92, "Attorney Notes": "Direct 2(d) refusal risk against core beer goods."},
        {"Select": True, "Source": "USPTO (CCCI)", "Matched Mark": "WINGMAN SPIRITS", "Class": "Class 033", "Status": "LIVE", "Risk Score": 0.88, "Attorney Notes": "High cross-class co-citation refusal zone."},
        {"Select": False, "Source": "USPTO", "Matched Mark": "WINGMAN BEVERAGE BAR", "Class": "Class 035", "Status": "DEAD", "Risk Score": 0.21, "Attorney Notes": ""},
        {"Select": True, "Source": "TTB COLA", "Matched Mark": "WINGMAN CIDER", "Class": "Malt / Cider", "Status": "ACTIVE", "Risk Score": 0.75, "Attorney Notes": "Common law prior-use exposure in market."},
        {"Select": False, "Source": "Amazon SP-API", "Matched Mark": "Wingman Party Cups", "Class": "Home & Kitchen", "Status": "LIVE", "Risk Score": 0.15, "Attorney Notes": ""}
    ])

# ==============================================================================
# CONTEXT POP-UP MODAL (RAGNARBOX)
# ==============================================================================
@st.dialog("➕ Add Contextual Indicator")
def add_context_dialog():
    st.markdown("Pinpoint your inquiry by selecting a specific topic, jurisdiction, or license.")
    col_c1, col_c2 = st.columns([1, 1.5])
    with col_c1:
        category = st.radio("Category", ["Jurisdiction", "Commodity", "License Type", "Concept"])
    with col_c2:
        if category == "Jurisdiction":
            options = ["US (Federal/TTB)", "New York (NY)", "Virginia (VA)", "Colorado (CO)", "Montana (MT)", "California (CA)"]
        elif category == "Commodity":
            options = ["Beer / Malt", "Wine / Vinous", "Spirits", "Low-ABV RTD", "Non-Alc"]
        elif category == "License Type":
            options = ["Brewery", "Winery", "Distillery", "Wholesaler", "Retailer - On-Premises"]
        else:
            options = ["Direct-to-Consumer Shipping", "Tied-House & Inducements", "Alternating Proprietorship", "Change of Ownership"]
        selection = st.selectbox("Options", options)

    if st.button("Add to Active Scope", type="primary", use_container_width=True):
        prefix = "JURIS" if category == "Jurisdiction" else category.upper().replace(" TYPE", "")
        tag = f"{prefix} - {selection.upper()}"
        if tag not in st.session_state.active_context:
            st.session_state.active_context.append(tag)
        st.rerun()

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    if os.path.exists("solstone-logo.jpg"):
        st.image("solstone-logo.jpg", use_container_width=True)
    else:
        st.markdown("## ⬡ SOLSTONE")
    st.caption("LegalTech & Regulatory Operating System")
    st.markdown("")

    portfolio_options = [
        "Wyngman Brewing Co.",
        "Blue Ridge Cellars LLC",
        "High Peak Spirits Co.",
        "Free Form"
    ]
    current_idx = portfolio_options.index(st.session_state.current_company) if st.session_state.current_company in portfolio_options else 0
    selected_company = st.selectbox(
        "Active Entity Portfolio",
        portfolio_options,
        index=current_idx
    )
    if selected_company != st.session_state.current_company:
        st.session_state.current_company = selected_company
        st.session_state.active_context = ENTITIES_DATA[selected_company]["default_context"].copy()
        st.rerun()

    # Copilot Toggle
    btn_label = "✖ Close Solstone RagnarBox" if st.session_state.copilot_open else "✨ Launch Solstone RagnarBox"
    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.copilot_open = not st.session_state.copilot_open
        st.rerun()

    st.markdown("---")

    # --- EXPANDABLE: SUMMARY ---
    with st.expander("📊 CORPORATE RECORD (SUMMARY)", expanded=(st.session_state.nav_section == "SUMMARY")):
        if st.button("🏛️ Licenses & Permits", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "SUMMARY", "Licenses"; st.rerun()
        if st.button("🏷️ Brands & COLAs", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "SUMMARY", "Brands"; st.rerun()
        if st.button("🚚 Franchise Distributors", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "SUMMARY", "Distributors"; st.rerun()
        if st.button("💲 Price Postings", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "SUMMARY", "Price Postings"; st.rerun()
        if st.button("👥 Cap Table & Owners", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "SUMMARY", "Owners"; st.rerun()

    # --- EXPANDABLE: IP TOOLS ---
    with st.expander("⚖️ IP & TRADEMARK SUITE", expanded=(st.session_state.nav_section == "TOOLS_IP")):
        if st.button("🔍 TM Gap Audit", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "TM Audit"; st.rerun()
        if st.button("🛡️ Clearance Engine", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "TM Clearance"; st.rerun()
        if st.button("📡 Brand Monitoring", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "TM Monitoring"; st.rerun()
        if st.button("👤 Owner Portfolio Status", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "Owner Status"; st.rerun()
        if st.button("📝 Letter of Protest Builder", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "LOP Builder"; st.rerun()
        if st.button("⚠️ TTAB Threat Assessment", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_IP", "TTAB Threat"; st.rerun()

    # --- EXPANDABLE: COMPLIANCE & SITE TOOLS ---
    with st.expander("🏢 REGULATORY & SITE SUITE", expanded=(st.session_state.nav_section == "TOOLS_COMPLIANCE")):
        if st.button("📋 360° Company Audit", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_COMPLIANCE", "Company Audit"; st.rerun()
        if st.button("🗺️ GIS Site Feasibility", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_COMPLIANCE", "GIS Site Check"; st.rerun()
        if st.button("📐 Metes & Bounds Drafter", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "TOOLS_COMPLIANCE", "Metes Bounds"; st.rerun()

    # --- EXPANDABLE: FORMS ---
    with st.expander("📑 AGENCY FORMS", expanded=(st.session_state.nav_section == "FORMS")):
        if st.button("📄 Regulatory Library", use_container_width=True):
            st.session_state.nav_section, st.session_state.nav_page = "FORMS", "Forms Library"; st.rerun()

# ==============================================================================
# HEADER: ACTIVE ENTITY & DEADLINES DRAWER
# ==============================================================================
ent = ENTITIES_DATA[st.session_state.current_company]

col_h1, col_h2 = st.columns([3.5, 1.2])
with col_h1:
    st.markdown(f"## {ent['company']}")
    st.caption(f"HQ: {ent['hq']} | Category: {ent['type']} | Immutable UUID: `{ent['uuid']}`")

with col_h2:
    deadline_count = len(ent["deadlines"])
    badge_label = f"⚠️ Action Required ({deadline_count} Deadlines)" if deadline_count > 0 else "✅ No Action Required (0)"
    with st.popover(badge_label, use_container_width=True):
        if deadline_count > 0:
            st.markdown("#### Critical Regulatory & IP Deadlines")
            st.caption(f"Active Surveillance for {ent['company']}")
            st.markdown("---")
            for d in ent["deadlines"]:
                color = "red" if d["severity"] == "CRITICAL" else ("orange" if d["severity"] == "HIGH" else "blue")
                st.markdown(f":{color}[**{d['text']}**]")
                st.markdown(f"↳ *Required Action: {d['action']}*")
                st.divider()
        else:
            st.info("No impending statutory deadlines or trademark office action cutoffs found.")

st.markdown("---")

# ==============================================================================
# MAIN CANVAS VS COPILOT SPLIT (Mobile responsive columns)
# ==============================================================================
if st.session_state.copilot_open:
    col_workspace, col_chat = st.columns([1.3, 2.7], gap="large")
else:
    col_workspace = st.container()
    col_chat = None

# ==============================================================================
# WORKSPACE CONTENT ROUTER
# ==============================================================================
with col_workspace:
    nav = st.session_state.nav_page
    is_freeform = (st.session_state.current_company == "Free Form")

    # --------------------------------------------------------------------------
    # SUMMARY: LICENSES (COMPACT SQUARE CARDS WITH TEXT WRAP & INLINE ADD)
    # --------------------------------------------------------------------------
    if nav == "Licenses":
        st.subheader("🏛️ Operational Licenses & Permits Held")
        st.caption("Synchronized with Federal TTB and State Alcohol Beverage Control Registers")
        
        if is_freeform:
            st.info("Free Form Mode: Link state ABC permits or TTB notices via search below.")
            st.text_input("Enter Permit ID or Corporate Seed:", placeholder="e.g. 03-88491-0001 or BR-CO-WYNG-01")
        else:
            for idx, lic in enumerate(ent["licenses"]):
                with st.container():
                    col_info, col_scope_action = st.columns([4, 1.2], gap="small")
                    
                    with col_info:
                        # Minimal padding, wide rectangular box, enforced text wrapping
                        st.markdown(
                            f"""
                            <div class="license-card">
                                <div class="license-title">🏛️ {lic['jurisdiction']} — {lic['license_name']}</div>
                                <div class="license-meta">
                                    <b>ID:</b> <code>{lic['id_num']}</code> | 
                                    <b>Expires:</b> {lic['expires']} | 
                                    <b>Status:</b> <span style="color: {'#22c55e' if lic['status'] == 'VALID' or lic['status'] == 'ACTIVE' else '#eab308'}; font-weight:700;">{lic['status']}</span>
                                </div>
                                <div class="license-endorsements">
                                    <b>Endorsements:</b> {lic['endorsements']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col_scope_action:
                        st.write("") # Vertical alignment spacing
                        btn_key = f"add_lic_scope_{idx}_{lic['id_num']}"
                        if st.button("➕ Add to Scope", key=btn_key, use_container_width=True):
                            juris_val = lic['jurisdiction'].split(' (')[0].upper()
                            juris_tag = f"JURIS - {juris_val}"
                            lic_tag = lic["context_tag"]
                            
                            added_tags = []
                            if juris_tag not in st.session_state.active_context:
                                st.session_state.active_context.append(juris_tag)
                                added_tags.append(juris_tag)
                            if lic_tag not in st.session_state.active_context:
                                st.session_state.active_context.append(lic_tag)
                                added_tags.append(lic_tag)
                                
                            if added_tags:
                                st.toast(f"Injected into RagnarBox: {', '.join(added_tags)}")
                            else:
                                st.toast("Parameters already active in RagnarBox scope.")
                            st.rerun()

    # --------------------------------------------------------------------------
    # SUMMARY: BRANDS
    # --------------------------------------------------------------------------
    elif nav == "Brands":
        st.subheader("🏷️ Commercial Brands & Label Approvals (TTB COLAs)")
        if is_freeform:
            st.info("Free Form Mode: Query federal COLAs and state brand registrations dynamically.")
            st.text_input("Enter Brand Name or TTB COLA #:", placeholder="e.g. 23100001000122")
        else:
            st.dataframe(pd.DataFrame(ent["brands"]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # SUMMARY: DISTRIBUTORS
    # --------------------------------------------------------------------------
    elif nav == "Distributors":
        st.subheader("🚚 Authorized Wholesalers & Franchise Designations")
        if is_freeform:
            st.info("Free Form Mode: No franchise distribution contracts linked.")
        else:
            st.dataframe(pd.DataFrame(ent["distributors"]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # SUMMARY: PRICE POSTINGS
    # --------------------------------------------------------------------------
    elif nav == "Price Postings":
        st.subheader("💲 Wholesale Price Postings & Schedules")
        if is_freeform:
            st.info("Free Form Mode: Select a state liquor authority to view posted schedules.")
        else:
            st.dataframe(pd.DataFrame(ent["price_postings"]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # SUMMARY: OWNERS
    # --------------------------------------------------------------------------
    elif nav == "Owners":
        st.subheader("👥 True Owners & Corporate Officers (LIC-OWN-TRUE)")
        if is_freeform:
            st.info("Free Form Mode: Disclose ownership structure and fingerprinting status.")
        else:
            st.dataframe(pd.DataFrame(ent["owners"]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TOOLS: IP > TM GAP AUDIT
    # --------------------------------------------------------------------------
    elif nav == "TM Audit":
        st.subheader("🔍 Trademark Audit & IP-Regulatory Gap Evaluator")
        st.caption("Set-Difference Mathematical Engine: B_active \\ TM_registered across all commercial registers")
        
        if is_freeform:
            st.write("Cross-reference any portfolio of commercial brand labels against the USPTO register.")
            test_brand = st.text_input("Brand to Audit against USPTO Register:", value="Front Range Hazy IPA")
            if st.button("Run Diagnostic Check", type="primary"):
                st.warning(f"⚠️ Unprotected Brand: No active USPTO Class 032 filing found for '{test_brand}'.")
        else:
            if st.button("🚀 Run Instant IP Gap Audit", type="primary"):
                if "Wyngman" in st.session_state.current_company:
                    st.error(
                        "⚠️ **1 Critical IP Gap Detected!**\n\n"
                        "Brand Name: **'Wyngman Imperial Porter'**\n"
                        "- Federal TTB COLA #24018001000842 (Active In-Commerce Distribution in CO)\n"
                        "- USPTO Register Status: **NO FEDERAL TRADEMARK APPLICATION FOUND** in Class 032 or Class 033.\n"
                        "- Recommendation: Prepare Trademark Application in Nice Class 032 immediately."
                    )
                else:
                    st.success("✅ **Zero IP Gaps Detected.** All commercialized brands hold active federal USPTO registrations.")

    # --------------------------------------------------------------------------
    # TOOLS: IP > TM CLEARANCE
    # --------------------------------------------------------------------------
    elif nav == "TM Clearance":
        st.subheader("⚖️ Automated Trademark Clearance Engine")
        st.caption("Section 2(d) & 2(e) Likelihood of Confusion Analysis with Cross-Class Matrix")

        col_t1, col_t2 = st.columns([1.5, 2])
        with col_t1:
            st.text_input("Proposed Mark", value="WYNGMAN")
        with col_t2:
            st.text_input("Goods / Services", value="Craft beers, ales, and non-alcoholic malt beverages")

        c1, c2, c3 = st.columns(3)
        c1.metric("Section 2(d) Conflict Likelihood", "84.2%", "HIGH RISK", delta_color="inverse")
        c2.metric("Section 2(e) Descriptiveness", "12.0%", "LOW RISK")
        c3.metric("Cross-Class Confusion (CCCI)", "0.89", "032 ↔ 033")

        st.markdown("#### Interactive Review Panel (Curate Marks for Dual-PDF Export)")
        edited_df = st.data_editor(
            st.session_state.review_data,
            column_config={
                "Select": st.column_config.CheckboxColumn("Include in PDF 2", default=True),
                "Source": st.column_config.TextColumn(disabled=True),
                "Matched Mark": st.column_config.TextColumn(disabled=True),
                "Risk Score": st.column_config.ProgressColumn("Risk Weight", min_value=0.0, max_value=1.0, format="%.2f"),
                "Attorney Notes": st.column_config.TextColumn("Attorney Annotation")
            },
            use_container_width=True, hide_index=True
        )
        st.session_state.review_data = edited_df

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("📄 Preview PDF 1: Full Raw Search Log", use_container_width=True):
                st.info("PDF 1 compiled: Contains all 48 uncurated hits across USPTO, TTB COLAs, and Amazon.")
        with col_b2:
            if st.button("🚀 Finalize & Export Curated Report (PDF 2)", type="primary", use_container_width=True):
                st.balloons()
                st.success("Dual-PDF Package (Raw Log + Curated Analysis) compiled and emailed!")

    # --------------------------------------------------------------------------
    # TOOLS: IP > TM MONITORING
    # --------------------------------------------------------------------------
    elif nav == "TM Monitoring":
        st.subheader("📡 Trademark Brand Surveillance & Monitoring")
        st.dataframe(pd.DataFrame([
            {"Monitored Mark": "WYNGMAN", "Primary Class": "Class 032", "Frequency": "Daily Sweep", "Last Sweep": "2026-10-26", "New Alerts": "1 Potential Match"},
            {"Monitored Mark": "WYNGMAN HAZY", "Primary Class": "Class 032", "Frequency": "Weekly Sweep", "Last Sweep": "2026-10-20", "New Alerts": "0 Matches"}
        ]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TOOLS: IP > OWNER STATUS
    # --------------------------------------------------------------------------
    elif nav == "Owner Status":
        st.subheader("👤 Instant Owner Status Tool")
        target_entity = st.text_input("Entity Legal Name", value="Solace Brewing Company")
        if st.button("Run Portfolio Lookup", type="primary"):
            st.success(f"Records located for '{target_entity}':")
            st.dataframe(pd.DataFrame([
                {"Serial": "87123456", "Mark": "SOLACE", "Status": "REGISTERED", "Class": "032"},
                {"Serial": "88987654", "Mark": "PARTLY CLOUDY", "Status": "REGISTERED", "Class": "032"}
            ]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TOOLS: IP > LETTER OF PROTEST BUILDER
    # --------------------------------------------------------------------------
    elif nav == "LOP Builder":
        st.subheader("📝 Letter of Protest Generator")
        c1, c2 = st.columns(2)
        c1.text_input("Your Prior Registration #", value="97412894 (WYNGMAN)")
        c2.text_input("Target Co-Pending Serial #", value="99123456 (WINGMAN SELTZER)")
        if st.button("Generate Protest Draft", type="primary"):
            st.info("Draft generated. Phonetic equivalence (Double Metaphone) & CCCI cross-class conflict (032 ↔ 033) established.")
            with st.expander("Preview Draft LOP", expanded=True):
                st.code(
                    "Dear Deputy Director for Trademark Examination Policy:\n\n"
                    "Evidence is enclosed establishing that the mark in co-pending Application Serial No. 99123456 "
                    "(WINGMAN SELTZER, Class 033) creates a likelihood of confusion under Section 2(d) with prior "
                    "Registration No. 97412894 (WYNGMAN, Class 032)...",
                    language="text"
                )

    # --------------------------------------------------------------------------
    # TOOLS: IP > TTAB THREAT ASSESSMENT
    # --------------------------------------------------------------------------
    elif nav == "TTAB Threat":
        st.subheader("⚠️ TTAB / PACER Threat Assessment")
        opposer = st.text_input("Target Opposer Entity:", value="Monster Energy Company")
        if st.button("Evaluate Litigation Threat", type="primary"):
            st.error(f"High Litigation Propensity: '{opposer}' has initiated over 140 TTAB Oppositions in Class 032.")

    # --------------------------------------------------------------------------
    # TOOLS: COMPLIANCE > COMPANY AUDIT
    # --------------------------------------------------------------------------
    elif nav == "Company Audit":
        st.subheader("🏢 Comprehensive 360° Operational Audit")
        if st.button("Generate Full Audit Report", type="primary"):
            st.success("Parallel graph traversal completed across all federal and state registries.")
            st.dataframe(pd.DataFrame([
                {"Audit Dimension": "Federal TTB Notice", "Status": "COMPLIANT", "Notes": "Bonded premise status active"},
                {"Audit Dimension": "State ABC Licensing", "Status": "ATTENTION", "Notes": "State license renewal window open"},
                {"Audit Dimension": "Brand Labels (COLAs)", "Status": "WARNING", "Notes": "1 commercial brand lacks USPTO TM"},
                {"Audit Dimension": "Tied-House Exposure", "Status": "CLEAR", "Notes": "Zero prohibited cross-tier ownership"}
            ]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TOOLS: COMPLIANCE > GIS SITE FEASIBILITY
    # --------------------------------------------------------------------------
    elif nav == "GIS Site Check":
        st.subheader("🗺️ 3-Pillar GIS Site Feasibility")
        st.text_input("Candidate Premises Address:", value="2901 Blake St, Denver, CO 80205")
        if st.button("Run Spatial Conflict Check", type="primary"):
            st.dataframe(pd.DataFrame([
                {"Layer": "Pillar 1: Zoning", "Value": "I-MX-3", "Status": "Manufacturing & Taproom Permitted by Right", "Flag": "CLEAR"},
                {"Layer": "Pillar 2: School Buffer (500ft)", "Value": "640 ft to Swansea Elem", "Status": "Exceeds statutory buffer radius", "Flag": "CLEAR"},
                {"Layer": "Pillar 3: Industrial Pre-Treatment", "Value": "BOD > 250 mg/L", "Status": "Grease / solids interceptor required", "Flag": "WARNING"}
            ]), use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TOOLS: COMPLIANCE > METES & BOUNDS DRAFTER
    # --------------------------------------------------------------------------
    elif nav == "Metes Bounds":
        st.subheader("📐 Metes & Bounds Legal Description Drafter")
        addr = st.text_input("Premises Address for Parcel Extraction:", value="2901 Blake St, Denver, CO 80205")
        if st.button("Extract Parcel Geometry", type="primary"):
            st.success("Extracted parcel boundary geometry for Parcel ID: 02277-12-019.")
            st.code(
                "BEGINNING at a point on the northwesterly line of Blake Street, said point being South "
                "45 degrees 00 minutes 00 seconds West, a distance of 125.00 feet from the intersection of "
                "the northwesterly line of Blake Street and the southwesterly line of 30th Street; THENCE "
                "North 45 degrees 00 minutes 00 seconds West, a distance of 125.00 feet...",
                language="text"
            )

    # --------------------------------------------------------------------------
    # FORMS: REGULATORY LIBRARY
    # --------------------------------------------------------------------------
    elif nav == "Forms Library":
        st.subheader("📑 Regulatory & Intellectual Property Forms Library")
        st.dataframe(pd.DataFrame([
            {"Authority": "Federal (TTB)", "Form Code": "TTB F 5130.12", "Description": "Brewer's Notice & Operating Premises Schedule", "Format": "PDF Fillable"},
            {"Authority": "Federal (TTB)", "Form Code": "TTB F 5100.31", "Description": "Application for Label Approval (COLA)", "Format": "COLAs Online"},
            {"Authority": "Colorado LED", "Form Code": "DR 8404", "Description": "Colorado Liquor License Renewal Application", "Format": "State Portal"},
            {"Authority": "Virginia ABC", "Form Code": "ABC-206", "Description": "Farm Winery Remote Tasting Room Authorization", "Format": "PDF Fillable"}
        ]), use_container_width=True, hide_index=True)

# ==============================================================================
# PERSISTENT SOLSTONE RAGNARBOX (RIGHT 2/3 DRAWER)
# ==============================================================================
if col_chat:
    with col_chat:
        st.markdown("### ✨ SOLSTONE RAGNARBOX")
        st.markdown("**Active Inquiry Context Scope:**")
        
        # Explicit user guidance request
        st.caption(
            "The system is only considering these parameters. "
            "If you would like to also consider, e.g., laws relating to wine, TTB, another state, etc., "
            "click \"Add\" to include those as well."
        )
        
        pill_cols = st.columns(min(len(st.session_state.active_context) + 1, 5))
        with pill_cols[0]:
            if st.button("➕ Add", type="secondary"):
                add_context_dialog()

        for idx, ctx in enumerate(st.session_state.active_context):
            c_idx = (idx + 1) % 5
            if c_idx == 0 and idx > 0:
                pill_cols = st.columns(5)
            with pill_cols[c_idx]:
                if st.button(f"{ctx} ✖", key=f"copilot_pill_{idx}"):
                    st.session_state.active_context.pop(idx)
                    st.rerun()

        st.markdown("---")
        chat_box = st.container(height=520)
        for msg in st.session_state.chat_history:
            with chat_box.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_prompt := st.chat_input("Ask a legal, compliance, or IP question..."):
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            scope_str = " | ".join(st.session_state.active_context) if st.session_state.active_context else "GLOBAL"
            simulated_response = (
                f"**[Active Scope: {scope_str} | Active Entity: {st.session_state.current_company}]**\n\n"
                f"Under governing statutes, this operation is authorized to self-distribute "
                f"up to statutory barrelage limits directly to licensed retailers. "
                f"\n\n*Statutory Authority: C.R.S. § 44-3-402; 1 CCR 203-2 Regulation 47-400; 27 CFR Part 25.*"
            )
            st.session_state.chat_history.append({"role": "assistant", "content": simulated_response})
            st.rerun()
