
import streamlit as st
import pandas as pd
from returntrack_logic import load_data, save_data, add_or_merge_entry, calculate_impact, get_available_months, DEFAULT_REUSE

st.set_page_config(page_title="ReturnTrack Dashboard", layout="wide")

# ---- Title and Intro ----
st.title("📦 ReturnTrack - Reusable Packaging Impact Dashboard")
st.markdown("A sustainability initiative dashboard for tracking reusable material returns and their environmental & financial impact.")

# ---- Load Data ----
df = load_data()

# ---- Sidebar: Reuse Tuning ----
st.sidebar.header("⚙️ Reuse Frequency Settings")
reuse_freq = {}
for item in DEFAULT_REUSE:
    reuse_freq[item] = st.sidebar.slider(f"{item} reuse/month", 1, 50, DEFAULT_REUSE[item])

# ---- Add New Entry ----
st.subheader("➕ Add New Monthly Data")
with st.form("entry_form", clear_on_submit=True):
    item = st.selectbox("Item Type", list(DEFAULT_REUSE.keys()))
    qty = st.number_input("Quantity Returned", min_value=0, step=1)
    month = st.selectbox("Month", ["May", "June", "July", "August"])
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        df = add_or_merge_entry(df, {"Item Type": item, "Quantity Returned": qty, "Month": month})
        save_data(df)
        st.success("Entry added and merged successfully!")

# ---- Editable Table ----
st.subheader("📋 Editable Monthly Data")
df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
save_data(df)

# ---- Select Month for Analysis ----
months = get_available_months(df)
if months:
    selected_month = st.selectbox("📅 Select Month to View Impact", months)
    df_month = df[df["Month"] == selected_month]
    impact_df = calculate_impact(df_month, reuse_freq)

    # ---- KPI Dashboard ----
    st.subheader(f"📊 Impact Summary - {selected_month}")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("CO₂ Avoided (kg)", f"{impact_df['CO2 Avoided (kg)'].sum():,.2f}")
    kpi2.metric("Material Saved (kg)", f"{impact_df['Material Saved (kg)'].sum():,.2f}")
    kpi3.metric("Cost Avoided (₹)", f"{impact_df['Cost Avoided (₹)'].sum():,.0f}")

    # ---- Data Table ----
    st.dataframe(impact_df, use_container_width=True)

    # ---- Download Report ----
    csv = impact_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Impact Report (CSV)",
        data=csv,
        file_name=f'ReturnTrack_Impact_{selected_month}.csv',
        mime='text/csv',
    )
else:
    st.info("Please add data to begin analysis.")
