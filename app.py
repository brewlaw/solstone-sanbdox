import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Solstone AI | Regulatory & IP Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "entity_uuid" not in st.session_state:
    st.session_state.entity_uuid = "ENT-8924-WYNGMAN"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Solstone Copilot active. Scope locked to Entity ENT-8924-WYNGMAN (CO | Manufacturer / Brewer | Beer). How can I assist your compliance or trademark workflow?"
        }
    ]

if "review_data" not in st.session_state:
    st.session_state.review_data = pd.DataFrame([
        {
            "Select": True,
            "Source": "USPTO",
            "Matched Mark": "WINGMAN BREWING",
            "Class": "Class 032",
            "Status": "LIVE",
            "Risk Score": 0.92,
            "Attorney Notes": "Direct 2(d) refusal risk against core beer goods."
        },
        {
            "Select": True,
            "Source": "USPTO (CCCI)",
            "Matched Mark": "WINGMAN SPIRITS",
            "Class": "Class 033",
            "Status": "LIVE",
            "Risk Score": 0.88,
            "Attorney Notes": "High cross-class co-citation refusal zone."
        },
        {
            "Select": False,
            "Source": "USPTO",
            "Matched Mark": "WINGMAN BEVERAGE BAR",
            "Class": "Class 035",
            "Status": "DEAD",
            "Risk Score": 0.21,
            "Attorney Notes": ""
        },
        {
            "Select": True,
            "Source": "TTB COLA",
            "Matched Mark": "WINGMAN CIDER",
            "Class": "Malt / Cider",
            "Status": "ACTIVE",
            "Risk Score": 0.75,
            "Attorney Notes": "Common law prior-use exposure in market."
        },
        {
            "Select": False,
            "Source": "Amazon SP-API",
            "Matched Mark": "Wingman Party Cups",
            "Class": "Home & Kitchen",
            "Status": "LIVE",
            "Risk Score": 0.15,
            "Attorney Notes": ""
        }
    ])

# ==============================================================================
# SIDEBAR: PERSISTENT SOLSTONE ASSISTANT & SCOPE LOCK (GLOBAL CO-PILOT)
# ==============================================================================
with st.sidebar:
    st.markdown("### ⬡ SOLSTONE COPILOT")
    st.caption("Cross-Domain Regulatory & IP Intelligence Engine")
    
    st.markdown("---")
    st.markdown("**Scope Lock Injection (J ∩ L ∩ E ∩ C)**")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        jurisdiction = st.selectbox("Jurisdiction (J)", ["Federal (TTB/FDA)", "CO", "VA", "DC", "CA", "NY"], index=1)
        commodity = st.selectbox("Commodity (C)", ["Beer", "Wine", "Spirits", "Low-ABV RTD", "Non-Alc"], index=0)
    with col_s2:
        tier = st.selectbox("Entity Tier (E)", ["Manufacturer", "Wholesaler", "Importer", "Retailer"], index=0)
        license_type = st.selectbox("License Class (L)", ["Brewery (Small)", "Commercial Brewery", "Brewpub", "Wholesale Malt"], index=0)

    st.markdown("---")
    st.markdown("**Assistant Conversation**")

    # Message container with fixed height
    chat_container = st.container(height=320)
    for msg in st.session_state.chat_history:
        with chat_container.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if user_prompt := st.chat_input("Ask a compliance or IP question..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        # Simulated dual-payload RAG response
        simulated_response = (
            f"**[Active Scope: {jurisdiction} | {commodity} | {license_type}]**\n\n"
            f"Under governing regulations for this profile, direct commercial self-distribution "
            f"is permitted up to statutory volume limits, provided brand label approvals are filed. "
            f"\n\n*Statutory Citations: C.R.S. § 44-3-402; 1 CCR 203-2 Regulation 47-400; 27 CFR § 25.205.*"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": simulated_response})
        st.rerun()

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ==============================================================================
# MAIN VIEW: HUB-AND-SPOKE WORKSPACES
# ==============================================================================
workspace = st.radio(
    "Select Platform Workspace",
    [
        "🏢 Master Entity Hub & IP Gap Audit",
        "⚖️ Trademark Clearance Suite (tm.solstone.ai)",
        "📜 Regulatory Compliance RAG (bev.solstone.ai)",
        "🗺️ 3-Pillar GIS Site Feasibility"
    ],
    horizontal=True
)

st.markdown("---")

# ------------------------------------------------------------------------------
# 1. MASTER ENTITY HUB & GAP EVALUATOR
# ------------------------------------------------------------------------------
if workspace == "🏢 Master Entity Hub & IP Gap Audit":
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.subheader("Master Entity Profile: Wyngman Brewing Co.")
        st.caption(f"Immutable Identifier: `{st.session_state.entity_uuid}` | Tied to States.db & IP Registers")
    with col_head2:
        st.metric(label="Overall Compliance Status", value="Active", delta="1 IP Gap Flagged", delta_color="inverse")

    # Set-Difference Gap Engine Banner
    st.error(
        "⚠️ **IP-Regulatory Gap Detected (Set-Difference: B_active \\ TM_registered)**\n\n"
        "Your active brand registration **'Wyngman Imperial Porter'** (TTB COLA #24018001000842) is commercially distributed, "
        "but has no matching USPTO Trademark filing under Nice Class 032 or Class 033."
    )

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### Operational & Regulatory Holdings (States.db)")
        permits_df = pd.DataFrame([
            {"Jurisdiction": "Federal", "Permit #": "BR-CO-WYNG-01", "Type": "TTB Brewer's Notice", "Status": "VALID"},
            {"Jurisdiction": "CO", "Permit #": "03-88491-0001", "Type": "Manufacturer - Small Brewery", "Status": "ACTIVE"},
            {"Jurisdiction": "CO - Denver", "Permit #": "LIC-2024-00918", "Type": "Local Liquor Sales Room", "Status": "ACTIVE"}
        ])
        st.dataframe(permits_df, use_container_width=True, hide_index=True)

        st.markdown("#### Commercial Brand & COLA Filings")
        colas_df = pd.DataFrame([
            {"COLA ID": "23100001000122", "Brand Name": "Wyngman Hazy IPA", "Class": "Class 032 (Beer)", "TM Protected": "Yes"},
            {"COLA ID": "24018001000842", "Brand Name": "Wyngman Imperial Porter", "Class": "Class 032 (Beer)", "TM Protected": "No (GAP)"}
        ])
        st.dataframe(colas_df, use_container_width=True, hide_index=True)

    with col_e2:
        st.markdown("#### IP Holdings & Registrations (USPTO)")
        tm_df = pd.DataFrame([
            {"Serial / Reg #": "97412894", "Mark": "WYNGMAN", "Nice Classes": "032", "Status": "REGISTERED"},
            {"Serial / Reg #": "98129048", "Mark": "WYNGMAN HAZY", "Nice Classes": "032", "Status": "PENDING (Pub for Opp)"}
        ])
        st.dataframe(tm_df, use_container_width=True, hide_index=True)

        st.markdown("#### Proactive Legislative Delta Feed")
        st.info(
            "📢 **CO SB 24-089 (Passed Aug 2026):** Direct-to-Consumer delivery reporting threshold "
            "adjusted for Colorado Manufacturer taproom branches."
        )

# ------------------------------------------------------------------------------
# 2. TRADEMARK CLEARANCE & REVIEW PANEL (tm.solstone.ai)
# ------------------------------------------------------------------------------
elif workspace == "⚖️ Trademark Clearance Suite (tm.solstone.ai)":
    st.subheader("Automated Trademark Clearance & Cross-Class Conflict Search")
    st.caption("Powered by the Correlative Class Confusion Index (CCCI) & Multi-Marketplace Scrapers")

    col_t1, col_t2, col_t3 = st.columns([2, 2, 1])
    with col_t1:
        target_mark = st.text_input("Proposed Word Mark", value="WYNGMAN")
    with col_t2:
        goods_desc = st.text_input(
            "Goods & Services (USPTO ID Manual Autocomplete)", 
            value="Craft beers, ales, and non-alcoholic malt beverages"
        )
    with col_t3:
        st.write("")
        st.write("")
        run_search = st.button("Run Clearance Search", type="primary", use_container_width=True)

    # Risk Summary Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Likelihood of Section 2(d) Refusal", "84.2%", "HIGH RISK", delta_color="inverse")
    col_m2.metric("Section 2(e) Descriptiveness", "12.0%", "LOW RISK")
    col_m3.metric("Cross-Class Confusion Index (CCCI)", "0.89", "032 ↔ 033 Conflict")

    st.markdown("---")
    st.markdown("#### Interactive Review Panel (Curate Hits for Report)")
    st.caption("Toggle checkboxes to include records in the Curated Analysis Report. Add attorney notes directly in the table.")

    # Data Editor with Checkboxes and Notes
    edited_df = st.data_editor(
        st.session_state.review_data,
        column_config={
            "Select": st.column_config.CheckboxColumn("Include in PDF 2", help="Select to curate", default=True),
            "Source": st.column_config.TextColumn("Source Registry", disabled=True),
            "Matched Mark": st.column_config.TextColumn("Matched Mark", disabled=True),
            "Class": st.column_config.TextColumn("Nice / Market Class", disabled=True),
            "Status": st.column_config.TextColumn("Legal Status", disabled=True),
            "Risk Score": st.column_config.ProgressColumn("Risk Weight", min_value=0.0, max_value=1.0, format="%.2f"),
            "Attorney Notes": st.column_config.TextColumn("Custom Attorney Annotation")
        },
        use_container_width=True,
        hide_index=True
    )
    st.session_state.review_data = edited_df

    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        if st.button("📄 Preview PDF 1: Full Raw Search Log", use_container_width=True):
            st.success("PDF 1 compiled: Contains all 48 uncurated hits across USPTO, TTB COLAs, and Amazon.")
    with col_b2:
        if st.button("🚀 Finalize & Export Curated Report (PDF 2)", type="primary", use_container_width=True):
            selected_count = edited_df["Select"].sum()
            st.balloons()
            st.success(f"Report Generated! Emailed Dual-PDF package ({selected_count} curated conflicts included in PDF 2) to your account.")

# ------------------------------------------------------------------------------
# 3. REGULATORY COMPLIANCE RAG (bev.solstone.ai)
# ------------------------------------------------------------------------------
elif workspace == "📜 Regulatory Compliance RAG (bev.solstone.ai)":
    st.subheader("Statutory Compliance Inquiry & RAG Auditor")
    st.caption("Deterministic Legal Sourcing Grounded in Codified Statutes and Regulations")

    rag_q = st.text_input(
        "Enter plain-English regulatory query:",
        value="Can a licensed Colorado craft brewery operate a non-contiguous sales room and serve malt beverages manufactured off-site?"
    )

    if st.button("Evaluate Compliance"):
        st.markdown("### Compliance Evaluation Payload")
        
        # Header disclosing evaluated layers
        st.info(
            "**Active Scope Header:** Evaluated C.R.S. Title 44, 1 CCR 203-2, and Federal TTB 27 CFR Part 25. "
            "Excluded non-applicable tiers: Retail Liquor Store, Wholesaler B, Out-of-State Shipper."
        )

        st.markdown(
            """
            #### Grounded Determination: **PERMITTED WITH RESTRICTIONS**
            
            1. **Sales Room Authority:** Under **C.R.S. § 44-3-402(2)**, a licensed Colorado manufacturer (brewery) is entitled to operate one sales room on or contiguous to the licensed premises, and up to one additional sales room away from the primary manufacturing premises.
            2. **Product Restrictions:** Under **1 CCR 203-2 Regulation 47-400**, a manufacturer's sales room may only serve and sell alcohol beverages that were manufactured by the licensee. Malt beverages manufactured by an unaffiliated third party cannot be served unless the premises holds a separate retail tavern or hotel & restaurant license.
            3. **Local Municipal Approval:** Notice of the proposed sales room must be filed with the local licensing authority, subject to public hearing and local zoning compliance.
            """
        )

        with st.expander("View Sourced Statutory Text & Metadata"):
            st.code(
                "C.R.S. § 44-3-402(2)(a): 'A manufacturer licensee may operate an additional sales room... "
                "subject to approval of the state and local licensing authorities...'\n\n"
                "1 CCR 203-2 Reg 47-400: 'No licensee operating a sales room shall sell products other than "
                "those fermented or distilled by said licensee...'",
                language="markdown"
            )

# ------------------------------------------------------------------------------
# 4. GIS SITE FEASIBILITY & 3-PILLAR ZONING
# ------------------------------------------------------------------------------
elif workspace == "🗺️ 3-Pillar GIS Site Feasibility":
    st.subheader("3-Pillar Site Feasibility & Spatial Conflict Check")
    st.caption("Pillar 1: Zoning & Land Use | Pillar 2: Municipal Alcohol Licensing | Pillar 3: Environmental & Utility Traps")

    address_input = st.text_input("Enter Candidate Premises Address:", value="2901 Blake St, Denver, CO 80205")

    if st.button("Run Spatial Conflict Check", type="primary"):
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.metric("Pillar 1: Zoning Classification", "I-MX-3", "Permitted (Industrial Mixed-Use)")
        with col_g2:
            st.metric("Pillar 2: School / Church Buffer", "640 ft", "Clear (> 500 ft Minimum)")
        with col_g3:
            st.metric("Pillar 3: Wastewater BOD Pre-Treatment", "Traps Found", "High Surcharge Zone", delta_color="inverse")

        st.markdown("#### Spatial Overlay Analysis")
        gis_table = pd.DataFrame([
            {"Layer Category": "Municipal Zoning", "Target Property": "I-MX-3", "Status": "Manufacturing & Taproom Permitted by Right", "Flag": "CLEAR"},
            {"Layer Category": "School Buffer (500ft)", "Nearest School": "640 ft (Swansea Elementary)", "Status": "Complies with C.R.S. § 44-3-313(1)(d)", "Flag": "CLEAR"},
            {"Layer Category": "Moratorium Polygon", "District": "RiNo Arts / Ballpark", "Status": "No active municipal tavern caps in this sector", "Flag": "CLEAR"},
            {"Layer Category": "Industrial Surcharge", "Metro Wastewater": "BOD / TSS > 250 mg/L", "Status": "Requires municipal grease/solids interceptor", "Flag": "WARNING"}
        ])
        st.dataframe(gis_table, use_container_width=True, hide_index=True)

        st.info(
            "📐 **Metes & Bounds Premises Description Drafted:** Ready for TTB Brewer's Notice Premises Diagram Exhibit."
        )
