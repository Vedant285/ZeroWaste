import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer

st.set_page_config('ZeroWaste', ':cook:') 
with open('Instructions.txt') as f:
    Instruction = f.read()
    

def suggest(dish, num_of_recipes):  # Function to suggest dishes from the ingredients given to it 
    prompt = f'''
    Suggest me {num_of_recipes} recipes from {dish}
    Should follow the following template:
    **Dish Name**
    1. 
    2.
    3.
    4.
    '''
    return bot(prompt)


st.title("ZeroWaste")   #title of project
tab1, tab2 = st.tabs(['Instructions', "Food Dish"])    #2 tabs 1st for Instructions  and 2nd is for Dishes 


with tab1:
    st.markdown(Instruction)
    st.image('logo.png', width=400)
    
with tab2:
    input_choice = st.radio("Choose how you want to tell us about the ingredients:", ['Camera', 'Text'])
    num_of_recipes = st.number_input("Select how many dishes you want", 1, 4, 1, 1) # 1,4 1 1 means start the count from 1, go up to 4, start the preview of count 1 from and after each increment, increment the number by 1.
    if input_choice == 'Camera':
        capture = st.camera_input("Take the image of food ingredients or vegetable")
        if capture:
            img = Image.open(capture)
        else:
            st.write("We are unable to detect. Can you please type the name if you know, otherwise try to capture again.")
            
    else:
        text = st.text_input("Enter the name of ingredients ex: mango, banana, orange etc")
        if text and num_of_recipes:
            st.write(suggest(text, num_of_recipes))
