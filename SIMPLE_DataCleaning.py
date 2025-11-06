import streamlit as st
import pandas as pd
import numpy as np
import csv
import requests

# Page setup
st.set_page_config(page_title="SIMPLE Data Cleaning Station by Zamzuri", layout="wide", page_icon="📊")
st.title("📊 SIMPLE – Data Cleaning Station V1.1")

# --- Sidebar Input Section ---
st.sidebar.header("📥 Data Input Method")
input_method = st.sidebar.radio("Choose input method:", ["📂 Upload File", "📡 Import via URL"])

df = None  # initialize

if input_method == "📂 Upload File":
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if uploaded_file:
        file_name = uploaded_file.name
        st.sidebar.success(f"✅ Uploaded: `{file_name}`")
        if file_name.endswith('.csv'):
            sample = uploaded_file.read(2048).decode('utf-8', errors='ignore')
            uploaded_file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample)
                separator = dialect.delimiter
            except csv.Error:
                separator = ','
            st.sidebar.info(f"🔍 Detected Separator: `{separator}`")
            try:
                df = pd.read_csv(uploaded_file, sep=separator)
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=',')
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.info("You can proceed to the tabs for EDA, Cleaning, Transformation, and Export.")

elif input_method == "📡 Import via URL":
    url_input = st.sidebar.text_input("Paste CSV/Excel/gsheet/RAW URL")
    if url_input:
        try:
            if url_input.endswith('.csv'):
                df = pd.read_csv(url_input)
            elif url_input.endswith('.xlsx'):
                df = pd.read_excel(url_input)
            elif "docs.google.com/spreadsheets" in url_input:
                sheet_id = url_input.split("/d/")[1].split("/")[0]
                gid = url_input.split("gid=")[-1]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
                df = pd.read_csv(csv_url)
            else:
                st.sidebar.error("❌ Unsupported format. Only CSV, Excel, or Google Sheets allowed.")
            if df is not None:
                st.sidebar.success("✅ Data loaded from URL.")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to load data: {e}")

# --- Branding Footer ---
st.sidebar.markdown("""
<hr style="margin-top:20px;margin-bottom:10px;">
<div style='text-align: center; font-size: 13px; color: grey;'>
    Developed by <strong>Zamzuri</strong> © 2025
</div>
""", unsafe_allow_html=True)

# --- Stop if no data ---
if df is None:
    st.warning("Hi! Please upload a file or provide a valid URL to begin.")
    st.stop()
else:
    st.session_state.df = df.copy()

df = st.session_state.df

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 EDA", "🧹 Auto Cleaning", "🧱 Transformation", "📥 Export"])

# --- 📋 Tab 1: EDA ---
with tab1:
    st.subheader("🔍 Preview")
    st.dataframe(df.head())

    st.subheader("📐 Dimensions")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    st.subheader("❓ Missing & Duplicate Info")
    st.write(f"**Missing Values (Total):** {df.isnull().sum().sum()}")
    st.write(f"**Duplicate Rows:** {df.duplicated().sum()}")

    missing_total = df.isnull().sum().sum()
    st.markdown(f"""
        <div style="background-color:#f9f9f9;padding:10px;border-radius:5px;border-left:5px solid #4CAF50">
            <h4 style="margin:0;color:#333;">🧮 Missing Value Status</h4>
            <p style="margin:0;">Total missing values in current dataset: <strong>{missing_total}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🧬 Data Types")
    st.dataframe(df.dtypes.reset_index().rename(columns={'index': 'Column', 0: 'Type'}))

    st.subheader("📊 Statistical Summary")
    st.dataframe(df.describe())

    st.subheader("🔤 Non-Numeric Summary")
    st.dataframe(df.describe(include='object'))

    st.subheader("📈 Visualization")
    x_axis = st.selectbox("Select X-axis", df.columns)
    y_axis = st.selectbox("Select Y-axis", df.columns)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📉 Line Chart"):
            st.line_chart(df[[x_axis, y_axis]].dropna())
    with col2:
        if st.button("📊 Bar Chart"):
            st.bar_chart(df[[x_axis, y_axis]].dropna())

# --- 🧹 Tab 2: Cleaning ---
with tab2:
    st.subheader("🧽 Remove Missing Values")
    st.write(f"**Missing Values (Total):** {df.isnull().sum().sum()}")
    if st.button("Run Dropna"):
        cleaned_df = df.dropna()
        st.success("Missing values removed.")
        st.dataframe(cleaned_df.head())
        st.download_button("📥 Download Cleaned CSV", cleaned_df.to_csv(index=False), file_name="cleaned_missing_removed.csv")

    st.subheader("🔧 Handle Missing (fillna/interpolate)") 
    st.write(f"**Missing fillna (Total):** {missing_total}")
    if st.button("Run Fillna + Interpolate"):
        filled_df = df.copy()
        for col in filled_df.select_dtypes(include='object'):
            filled_df[col] = filled_df[col].fillna("Na")
        for col in filled_df.select_dtypes(include=np.number):
            filled_df[col] = filled_df[col].interpolate()
        st.success("Missing values handled.")
        st.dataframe(filled_df.head())
        st.download_button("📥 Download Filled CSV", filled_df.to_csv(index=False), file_name="cleaned_missing_handled.csv")

    st.subheader("🧹 Remove Duplicates")
    st.write(f"**Duplicate Rows:** {df.duplicated().sum()}")
    if st.button("Run Deduplicate"):
        dedup_df = df.drop_duplicates()
        st.success("Duplicate rows removed.")
        st.dataframe(dedup_df.head())
        st.download_button("📥 Download Deduplicated CSV", dedup_df.to_csv(index=False), file_name="cleaned_duplicates_removed.csv")

# --- 🧱 Tab 3: Transformation ---
with tab3:
    st.subheader("🗑️ Drop Columns")
    drop_cols = st.multiselect("Select columns to drop", df.columns.tolist())
    if st.button("🚮 Drop Selected Columns"):
        if drop_cols:
            df_dropped = df.drop(columns=drop_cols)
            st.success(f"{len(drop_cols)} columns dropped.")
            st.dataframe(df_dropped.head())
            st.download_button("📥 Download Dropped Dataset", df_dropped.to_csv(index=False), file_name="dataset_dropped_columns.csv")
        else:
            st.info("No columns selected.")

    st.subheader("🔢 Map Categorical Values to Integer (< 5 Unique Data Only)")
    eligible_cols = [col for col in df.select_dtypes(include='object') if len(df[col].dropna().unique()) < 5]
    selected_col = st.selectbox("System AUTO select list column with < 5 unique data, Please select column to map", eligible_cols)

    if selected_col:
        unique_vals = df[selected_col].dropna().unique()
        st.write(f"📌 Unique values in `{selected_col}`:")
        st.write(unique_vals)

        mapping_dict = {}
        for val in unique_vals:
            mapping_dict[val] = st.number_input(f"Value for '{val}'", min_value=0, step=1, key=f"{selected_col}_{val}")
        st.json(mapping_dict)

        if st.button("✅ Apply Mapping"):
            df_mapped = df.copy()
            df_mapped[selected_col] = df_mapped[selected_col].map(mapping_dict)
            st.success(f"Column `{selected_col}` mapped.")
            st.dataframe(df_mapped[[selected_col]].head())
            st.download_button("📥 Download Mapped Dataset", df_mapped.to_csv(index=False), file_name=f"{selected_col}_mapped.csv")

# --- 📥 Tab 4: Export & Preview ---
with tab4:
    st.subheader("🔍 Column Preview with Pagination")

    preview_cols = st.multiselect("Choose columns to preview", df.columns.tolist())
    preview_mode = st.radio("Preview mode", ["Head only", "Tail only", "Head & Tail", "Paginated View"])

    if 'page' not in st.session_state:
        st.session_state.page = 0

    if preview_mode == "Paginated View":
        row_limit = st.selectbox("Rows per page", [20, 50, 100], index=0)
        total_rows = df.shape[0]
        max_page = total_rows // row_limit

        start_idx = st.session_state.page * row_limit
        end_idx = start_idx + row_limit

        st.write(f"📄 Showing rows {start_idx + 1} to {min(end_idx, total_rows)} of {total_rows}")

        if preview_cols:
            st.dataframe(df[preview_cols].iloc[start_idx:end_idx])
        else:
            st.dataframe(df.iloc[start_idx:end_idx])

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.page > 0:
                st.session_state.page -= 1
        with col2:
            if st.button("➡️ Next") and end_idx < total_rows:
                st.session_state.page += 1
        with col3:
            st.caption(f"Page {st.session_state.page + 1} of {max_page + 1}")

    else:
        # Reset page if not in paginated mode
        st.session_state.page = 0
        if preview_cols:
            if preview_mode == "Head only":
                st.dataframe(df[preview_cols].head())
            elif preview_mode == "Tail only":
                st.dataframe(df[preview_cols].tail())
            else:
                st.dataframe(pd.concat([df[preview_cols].head(), df[preview_cols].tail()]))
        else:
            st.info("No columns selected. Showing full dataset.")
            if preview_mode == "Head only":
                st.dataframe(df.head())
            elif preview_mode == "Tail only":
                st.dataframe(df.tail())
            else:
                st.dataframe(pd.concat([df.head(), df.tail()]))
