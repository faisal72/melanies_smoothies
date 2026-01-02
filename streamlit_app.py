# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothies! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custome Smoothie!
  """
)

import streamlit as st

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)

#import streamlit as st

#option_contact = st.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"),
#)
#st.write("You selected:", option_contact)

#option_fruit = st.selectbox(
#    "what is your favorite fruit?",
#    ("Bananna", "Strawbarries", "Peaches"),
#)
#st.write("Your favorite fruit is:", option_fruit)

cnx = st.connection("snowflake")
#session = get_active_session()
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredents_list = st.multiselect('Choose up to 5 ingregdients:', my_dataframe, max_selections=5)

if ingredents_list:
    st.write(ingredents_list)
    st.text(ingredents_list)

    ingredients_string = ''

    for fruit_chosen in ingredents_list:
        ingredients_string += fruit_chosen + ' '

#   st.write(ingredents_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)
    #st.stop
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
