import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from config.settings import CLEAN_RECEIPTS_PATH
from src.analyze.spending_analyzer import SpendingAnalyzer

st.set_page_config(page_title="Campus Receipt Analyzer", layout="wide")
st.title("Campus Mobile Order Receipt Analyzer")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_RECEIPTS_PATH)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


df = load_data()
analyzer = SpendingAnalyzer()

df_time = df.drop_duplicates("message_id").copy()
df_time = df_time.dropna(subset=["timestamp", "total"])

df_time["hour"] = df_time["timestamp"].dt.hour

def get_period(hour):
    if hour < 11:
        return "Breakfast"
    elif hour < 15:
        return "Lunch"
    elif hour < 19:
        return "Dinner"
    else:
        return "Late Night"

df_time["period"] = df_time["hour"].apply(get_period)

period_spend = df_time.groupby("period")["total"].sum()

period_order = ["Breakfast", "Lunch", "Dinner", "Late Night"]
period_spend = period_spend.reindex(period_order).fillna(0)

st.subheader("Raw Data Preview")
st.dataframe(df.head(20), use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Monthly Spending")
    monthly = analyzer.monthly_totals(df)

    monthly["month"] = pd.to_datetime(monthly["month"])
    monthly = monthly.sort_values("month")

    fig, ax = plt.subplots()

    ax.bar(monthly["month"].dt.strftime("%Y-%m"), monthly["total"])

    ax.set_title("Monthly Spending")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spend ($)")
    ax.grid(axis='y')

    # annotate bars
    for i, v in enumerate(monthly["total"]):
        ax.text(i, v, f"${v:.2f}", ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Category Breakdown")
    cats = analyzer.category_breakdown(df)
    fig, ax = plt.subplots()
    ax.pie(cats["item_price"], labels=cats["category"], autopct="%1.1f%%")
    st.pyplot(fig)

top_period = period_spend.idxmax()
st.metric("Peak Spending Time", top_period)
with col3:
    st.subheader("Spending by Time of Day")

    fig, ax = plt.subplots()

    ax.bar(period_spend.index, period_spend.values)

    ax.set_title("When Do I Spend Most?")
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Total Spend ($)")
    ax.grid(axis='y')

    # annotate bars
    for i, v in enumerate(period_spend.values):
        if v > 0:
            ax.text(i, v, f"${v:.2f}", ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Top Items")
st.dataframe(analyzer.top_items(df), use_container_width=True)
