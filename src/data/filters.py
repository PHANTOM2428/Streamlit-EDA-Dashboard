import pandas as pd
import streamlit as st


def get_filter_options(df, column):
    return sorted(df[column].unique())


def apply_hierarchical_filters(df):
    st.sidebar.header("Choose your filter: ")
    
    filtered_df = df.copy()
    
    region = st.sidebar.multiselect("Pick your Region", get_filter_options(filtered_df, "Region"))
    if region:
        filtered_df = filtered_df[filtered_df["Region"].isin(region)]
    
    state = st.sidebar.multiselect("Pick the State", get_filter_options(filtered_df, "State"))
    if state:
        filtered_df = filtered_df[filtered_df["State"].isin(state)]
    
    city = st.sidebar.multiselect("Pick the City", get_filter_options(filtered_df, "City"))
    if city:
        filtered_df = filtered_df[filtered_df["City"].isin(city)]
    
    return filtered_df


def aggregate_by_category(df):
    return df.groupby(by=["Category"], as_index=False)["Sales"].sum()


def aggregate_by_region(df):
    return df.groupby(by="Region", as_index=False)["Sales"].sum()


def create_timeseries_data(df):
    df["month_year"] = df["Order Date"].dt.to_period("M")
    timeseries_df = pd.DataFrame(
        df.groupby(df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()
    ).reset_index()
    return timeseries_df


def create_monthly_subcategory_pivot(df):
    df["month"] = df["Order Date"].dt.month_name()
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    pivot = pd.pivot_table(data=df, values="Sales", index=["Sub-Category"], columns="month")
    return pivot.reindex(columns=[m for m in month_order if m in pivot.columns])
