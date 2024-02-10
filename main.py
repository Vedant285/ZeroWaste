import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer

st.set_page_config('ZeroWaste', ':cook:') 
with open('Instructions.txt') as f:
    Instruction = f.read()
    
food_recognizer = FoodRecognizer(st.secrets['PAT'])

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
            top_pred = list(food_recognizer.recognize(img).items())[0]
            if top_pred[1] > 0.4:
                if top_pred[0] not in st.session_state['food items']:
                    st.session_state['food items'].append(top_pred[0])
                    st.success(f'{top_pred[0]} detected with conf. of {top_pred[1]}')
                else:
                    st.info(f'{top_pred[0]} already in list.')
            else:
                st.error("Ai cannot determine item")
        st.write('Food Items Recognized:')
        for item in st.session_state['food items']:
            st.markdown(f'- {item}')
            if st.button('Clear'):
            st.session_state['food items'] = []

        if st.button('Suggest') and st.session_state['food items']:
            st.write(suggest(num_of_rcps, st.session_state['food items']))
            
    else:
        text = st.text_input("Enter the name of ingredients ex: mango, banana, orange etc")
        if st.button('suggest') and num_of_recipes:
            st.write(suggest(text, num_of_recipes))
