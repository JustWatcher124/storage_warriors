import streamlit as st
import datetime
import helpers.helper_functions as helper_functions

try:
    model = st.session_state['chosen_model']
    available_products = st.session_state['chosen_models_avail_products']
    with open('markdowns/prediction.md') as file:
        markdown = file.read().split('[[[[')
    file.close()
    st.markdown(markdown[0])

    products = st.multiselect('Select a product to predict (if None, then all (Many Products=> Very Slow))',
                              options=available_products)
    current_date = datetime.datetime.now()
    next_week = current_date + datetime.timedelta(days=7)
    max_date = current_date + datetime.timedelta(days=90)

    d = st.date_input(
        "Select the the date range to know how much to buy in this time",
        (current_date, next_week),
        min_value=current_date,
        max_value=max_date,
        format="DD.MM.YYYY",
    )

    predict_them = st.button('Predict The Needed Inventory')
    if predict_them:
        if not products:
            products = available_products
        pred_data = helper_functions.make_prediction(model, products, d)
        st.dataframe(pred_data.head(20))
except:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
