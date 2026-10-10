
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SupplierIQ Mini",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SupplierIQ Mini")
st.caption("Supplier intelligence and sourcing dashboard")

suppliers = [
    {
        "Supplier": "TechSource Inc.",
        "Price ($)": 4500,
        "Delivery (days)": 4,
        "Quality (/10)": 9
    },
    {
        "Supplier": "Global Supplies",
        "Price ($)": 4000,
        "Delivery (days)": 2,
        "Quality (/10)": 7
    },
    {
        "Supplier": "SmartBuy Solutions",
        "Price ($)": 4750,
        "Delivery (days)": 3,
        "Quality (/10)": 10
    }
]

df = pd.DataFrame(suppliers)

# Let the user choose what matters most
st.sidebar.header("Scoring Preferences")

price_weight = st.sidebar.slider(
    "Price importance (%)", 0, 100, 40
)

delivery_weight = st.sidebar.slider(
    "Delivery importance (%)", 0, 100, 30
)

quality_weight = 100 - price_weight - delivery_weight

st.sidebar.write(
    f"Quality importance: {quality_weight}%"
)

if quality_weight < 0:
    st.error(
        "Price and delivery weights cannot total over 100%."
    )
    st.stop()

# Calculate supplier scores
lowest_price = df["Price ($)"].min()
fastest_delivery = df["Delivery (days)"].min()

df["Price Score"] = (
    lowest_price / df["Price ($)"] * 100
)

df["Delivery Score"] = (
    fastest_delivery / df["Delivery (days)"] * 100
)

df["Quality Score"] = df["Quality (/10)"] * 10

df["Final Score"] = (
    df["Price Score"] * price_weight / 100
    + df["Delivery Score"] * delivery_weight / 100
    + df["Quality Score"] * quality_weight / 100
).round(2)

# Rank suppliers
df = df.sort_values(
    "Final Score",
    ascending=False
).reset_index(drop=True)

df.index = df.index + 1
df.index.name = "Rank"

# Dashboard summary
best = df.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Top Supplier",
    best["Supplier"]
)

col2.metric(
    "Best Match Score",
    f'{best["Final Score"]:.2f}/100'
)

col3.metric(
    "Suppliers Compared",
    len(df)
)

st.divider()

st.subheader("🏆 Supplier Rankings")

st.dataframe(
    df[
        [
            "Supplier",
            "Price ($)",
            "Delivery (days)",
            "Quality (/10)",
            "Final Score"
        ]
    ],
    use_container_width=True
)

st.subheader("📈 Supplier Score Comparison")

chart_data = df.set_index("Supplier")[["Final Score"]]
st.bar_chart(chart_data)


# Supplier search
st.divider()
st.subheader("🔎 Explore Suppliers")

search = st.text_input(
    "Search by supplier name",
    placeholder="e.g. SmartBuy"
)

filtered_df = df[
    df["Supplier"].str.contains(
        search, case=False, na=False
    )
]

st.dataframe(
    filtered_df[
        [
            "Supplier",
            "Price ($)",
            "Delivery (days)",
            "Quality (/10)",
            "Final Score"
        ]
    ],
    use_container_width=True
)

# Explain the top-ranked supplier
st.divider()
st.subheader("💡 Why This Supplier Ranks First")

best = df.iloc[0]

st.success(
    f"{best['Supplier']} is the current top-ranked supplier "
    f"with a score of {best['Final Score']:.2f}/100."
)

# Explain the supplier's strengths
if best["Price ($)"] == df["Price ($)"].min():
    st.write("✅ Offers the lowest price.")

if best["Delivery (days)"] == df["Delivery (days)"].min():
    st.write("✅ Has the fastest delivery.")

if best["Quality (/10)"] == df["Quality (/10)"].max():
    st.write("✅ Has the highest quality rating.")

# Explain the trade-off
if best["Price ($)"] > df["Price ($)"].min():
    st.write(
        f"ℹ️ Trade-off: Its price is "
        f"${best['Price ($)'] - df['Price ($)'].min():.2f} "
        "higher than the lowest-priced option."
    )

st.caption(
    "This recommendation uses sample data and your selected "
    "weights. It is a decision-support prototype, not an "
    "AI model or a verification of real suppliers."
)
