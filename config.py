INDUSTRY_PRESETS = {
    "Finance": {
        "default_x": "Date",
        "default_y": "Amount",
        "primary_category": "Account",
        "categorical_filters": ["Account", "Category"],
        "numeric_filters": ["Amount"],
        "date_filters": ["Date"],
    },
    "Sales": {
        "default_x": "Date",
        "default_y": "Revenue",
        "primary_category": "Product",
        "categorical_filters": ["Product", "Region", "Salesperson"],
        "numeric_filters": ["Revenue", "Quantity"],
        "date_filters": ["Date"],
    },
    "Marketing": {
        "default_x": "Date",
        "default_y": "CTR",
        "primary_category": "Campaign",
        "categorical_filters": ["Campaign", "Channel"],
        "numeric_filters": ["Impressions", "Clicks", "Spend", "CTR"],
        "date_filters": ["Date"],
    },
    "E-commerce": {
        "default_x": "OrderDate",
        "default_y": "Sales",
        "primary_category": "Category",
        "categorical_filters": ["Category", "Product", "CustomerSegment"],
        "numeric_filters": ["Sales", "Profit", "Quantity"],
        "date_filters": ["OrderDate"],
    },
    "HR": {
        "default_x": "HireDate",
        "default_y": "Salary",
        "primary_category": "Department",
        "categorical_filters": ["Department", "JobRole", "Location"],
        "numeric_filters": ["Salary", "Tenure"],
        "date_filters": ["HireDate"],
    },
}

THEME = {
    "footer_note": "Built with Streamlit + Plotly. Customize presets to match your dataset columns.",
}
