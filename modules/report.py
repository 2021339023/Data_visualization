import streamlit as st
import pandas as pd
import io

def make_download_buttons(df: pd.DataFrame, industry: str):
    # CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered CSV",
        data=csv,
        file_name=f"{industry.lower()}_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered")
    st.download_button(
        label="⬇️ Download filtered Excel",
        data=buffer.getvalue(),
        file_name=f"{industry.lower()}_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    # Stub for PDF
    st.caption("Tip: Add HTML-to-PDF later using pdfkit/reportlab for a branded report.")
