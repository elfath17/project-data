import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from data_cleaning import load_data, clean_data
from eda import get_transaction_counts, get_delivery_time, get_repeat_customers, get_new_customers_by_month, get_seller_performance, get_top_bottom_categories, get_correlations
from visualizations import plot_transactions_by_state, plot_top_25_cities, plot_new_customers_by_month, plot_review_scores, plot_top_bottom_categories

def display_dashboard():
    # Sidebar
    st.sidebar.image("https://d3hw41hpah8tvx.cloudfront.net/images/logo_olist_d7309b5f20.png", use_column_width=True)
    st.sidebar.markdown("## Rentang Waktu")
    date_range = st.sidebar.date_input("Rentang Tanggal", [])

    # Main content
    st.title("E-Commerce Data Analysis")

    # Load and clean data
    customers_df, geolocation_df, orderitems_df, payments_df, reviews_df, orders_df, category_df, products_df, seller_df = load_data()
    customers_df, geolocation_df, orderitems_df, reviews_df, orders_df, products_df = clean_data(customers_df, geolocation_df, orderitems_df, reviews_df, orders_df, products_df)

    # Perform EDA
    city_counts, state_counts = get_transaction_counts(customers_df)
    filtered_orders_df = get_delivery_time(orders_df)
    repeat_customers_count = get_repeat_customers(orders_df)
    new_customers_by_month = get_new_customers_by_month(orders_df)
    
    # Merge seller data with reviews
    seller_orderitems_df = pd.merge(left=seller_df, right=orderitems_df, how="left", left_on="seller_id", right_on="seller_id")
    seller_orderitems_score_df = pd.merge(left=seller_orderitems_df, right=reviews_df, how="left", left_on="order_id", right_on="order_id")
    review_score_counts = get_seller_performance(seller_orderitems_score_df)
    
    # Merge product category data with order items
    products_category_df = pd.merge(left=products_df, right=category_df, how="left", left_on="product_category_name", right_on="product_category_name")
    products_category_orderitems_df = pd.merge(left=products_category_df, right=orderitems_df, how="left", left_on="product_id", right_on="product_id")
    top_10_categories, bottom_10_categories = get_top_bottom_categories(products_category_orderitems_df)
    
    # Calculate correlations
    products_category_orderitems_df["size_barang"] = products_category_orderitems_df["product_length_cm"] * products_category_orderitems_df["product_height_cm"] * products_category_orderitems_df["product_width_cm"]
    orders_reviews_df = pd.merge(left=filtered_orders_df, right=reviews_df, how="left", left_on="order_id", right_on="order_id")
    size_corr, delivery_review_corr = get_correlations(products_category_orderitems_df, orders_reviews_df)

    # Display visualizations
    st.image(plot_transactions_by_state(state_counts))
    st.image(plot_top_25_cities(city_counts))
    st.image(plot_new_customers_by_month(new_customers_by_month))
    st.image(plot_review_scores(review_score_counts))
    top_10_img, bottom_10_img = plot_top_bottom_categories(top_10_categories, bottom_10_categories)
    st.image(top_10_img)
    st.image(bottom_10_img)

if __name__ == "__main__":
    display_dashboard()
