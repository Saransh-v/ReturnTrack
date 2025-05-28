
import streamlit as st
import pandas as pd
from returntrack_logic import load_data, save_data, add_or_merge_entry, calculate_impact, get_available_months, DEFAULT_REUSE

st.set_page_config(page_title="ReturnTrack Dashboard", layout="wide")

# ---- Styling for light theme ----
light_style = '''
<style>
    body {
        background-color: #f9f9f9;
        color: #31333F;
    }
    .stApp {
        background-color: #ffffff;
    }
</style>
'''
st.markdown(light_style, unsafe_allow_html=True)

# ---- Title and Intro ----
st.title("🚚 ReturnTrack – Sustainability Dashboard")
st.markdown("Track reusable packaging returns and calculate your monthly sustainability impact for Volvo Eicher Commercial Vehicles Ltd.")

# ---- Load Data ----
df = load_data()

# ---- Sidebar: Reuse Tuning ----
st.sidebar.header("🔁 Reuse Frequency Settings")
reuse_freq = {}
for item in DEFAULT_REUSE:
    reuse_freq[item] = st.sidebar.slider(f"{item} reuse/month", 1, 50, DEFAULT_REUSE[item])

# ---- Add New Entry ----
st.subheader("📥 Add New Monthly Data")
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

    # ---- KPI Summary Cards ----
    st.subheader(f"📊 Monthly Impact Summary – {selected_month}")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🌍 CO₂ Avoided (kg)", f"{impact_df['CO2 Avoided (kg)'].sum():,.2f}")
    kpi2.metric("📦 Material Saved (kg)", f"{impact_df['Material Saved (kg)'].sum():,.2f}")
    kpi3.metric("💰 Cost Avoided (₹)", f"{impact_df['Cost Avoided (₹)'].sum():,.0f}")
    kpi4.metric("🚛 Truckloads Avoided", f"{impact_df['Truckloads Avoided'].sum():,.2f}")

    # ---- Impact Breakdown ----
    st.markdown("### 📑 Impact Breakdown by Item")
    for item in impact_df["Item Type"].unique():
        item_data = impact_df[impact_df["Item Type"] == item].iloc[0]
        with st.container():
            st.markdown(f"**🧱 {item}**")
            cols = st.columns(4)
            cols[0].metric("CO₂ Avoided", f"{item_data['CO2 Avoided (kg)']:.2f} kg")
            cols[1].metric("Material Saved", f"{item_data['Material Saved (kg)']:.2f} kg")
            cols[2].metric("Cost Saved", f"₹{item_data['Cost Avoided (₹)']:.0f}")
            cols[3].metric("Truckloads", f"{item_data['Truckloads Avoided']:.2f}")

    # ---- Download Report ----
    st.download_button(
        label="⬇️ Download Monthly Impact Report (CSV)",
        data=impact_df.to_csv(index=False).encode("utf-8"),
        file_name=f"ReturnTrack_Impact_{selected_month}.csv",
        mime="text/csv"
    )
else:
    st.info("Please add data to begin analysis.")
