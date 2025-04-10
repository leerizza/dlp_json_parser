import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="DLP Rule Parser", layout="wide")
st.title("DLP Rule Parser")

uploaded_file = st.file_uploader("Upload DLP Rule JSON (.txt) File", type=["txt", "json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)

        # Parse data into table format
        table_data = []
        for rule in data:
            table_data.append({
                "Display Name": rule.get("displayName", ""),
                "Description": rule.get("description", ""),
                "Status": rule.get("status", ""),
                "Rule Type": rule.get("ruleType", ""),
                "Severity": next((p["stringValue"] for p in rule.get("metadata", {}).get("parameter", []) if p["name"] == "severity"), ""),
                "Trigger": ", ".join(rule.get("trigger", [])),
                "Actions": ", ".join([a["actionName"] for a in rule.get("action", [])]),
                "Applications": ", ".join([app["googleApplication"] for app in rule.get("applicationIds", [])]),
                "Created By": rule.get("createdBy", {}).get("userName", "")
            })

        df = pd.DataFrame(table_data)

        st.success("File parsed successfully!")
        st.dataframe(df, use_container_width=True)

        # Export to Excel
        with pd.ExcelWriter("dlp_rules_output.xlsx", engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='DLP Rules')

        with open("dlp_rules_output.xlsx", "rb") as f:
            st.download_button("Download Excel File", f, file_name="DLP_Rules_Parsed.xlsx")

    except Exception as e:
        st.error(f"Failed to parse file: {e}")