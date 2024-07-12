# import modules, Streamlit for rendering, datetime for date operations on this page
import streamlit as st
import datetime

# Import the helper_functions script to 'outsource' the backend
import helpers.helper_functions as helper_functions

# Check if User is on the right page using session_states variables
try:
    # exists only if user has chosen a saved model from the Load Model / Data page -- causes exception caught below
    # the values are actually needed on this page, not only a check for existance
    model = st.session_state['chosen_model']
    available_products = st.session_state['chosen_models_avail_products']

    # load the default markdown from file
    with open('markdowns/prediction.md') as file:
        markdown = file.read().split('[[[[')
    file.close()
    st.markdown(markdown[0])

    # show a selection field for the available products that the model can predict
    products = st.multiselect('Select a product to predict (if None, then all (Many Products=> Very Slow))',
                              options=available_products)

    # get current date, date in a week from now and date 90 days for now
    current_date = datetime.datetime.now()
    next_week = current_date + datetime.timedelta(days=7)
    max_date = current_date + datetime.timedelta(days=90)

    d = st.date_input(
        "Select the the date range to know how much to buy in this time",
        (current_date, next_week),
        min_value=current_date,  # it makes not sense to 'predict' the past, that's what data is for
        max_value=max_date,  # it would make sense to predict further into the future, but basically no data source can support this
        format="DD.MM.YYYY",
    )

    predict_them = st.button('Predict The Needed Inventory')
    if predict_them:
        if not products:  # as stated above in the multiselect, if no product is chosen, all are used
            products = available_products

        # get predictions for needed inventory in the set time range
        pred_data = helper_functions.make_prediction(model, products, d)
        # show the predictions to user -- also allows download of the predictions to users system
        st.dataframe(pred_data)

except:  # bare exception because this also makes errors clear to the user
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
