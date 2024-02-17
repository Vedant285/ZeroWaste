import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer
import openai

st.set_page_config('ZeroWaste', ':cook:') 
openai.api_key = st.secrets["OpenAiAPI]

# Load Prompt Templates and Instructions
with open('Instructions.txt') as f:
    Instruction = f.read()

if 'food items' not in st.session_state:
    st.session_state['food items'] = []

food_recognizer = FoodRecognizer(st.secrets['PAT'])

st.title("ZeroWaste")   #title of project
tab1, tab2 = st.tabs(['Instructions', "Food Dish"])    #2 tabs 1st for Instructions  and 2nd is for Dishes 

def suggest(num_of_rcps, food_tags):
    prompt = f'''
    Provide {num_of_rcps} recipe suggestions for these food items: {food_tags}
    Write in this structure:
    **dish name**
    1. 
    2. 
    3. 
    Don't write ingredients.
    '''
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
          ]
    )
    st.write( completion.choices[0].message.content)


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
                st.error('AI cannot recognize item!')
        st.write('Food Items Recognized:')
        for item in st.session_state['food items']:
            st.markdown(f'- {item}')

        if st.button('Clear'):
            st.session_state['food items'] = []

        if st.button('Suggest') and st.session_state['food items']:
            (suggest(num_of_recipes,st.session_state['food items']))
        
            
    else:
        text = st.text_input("Enter the name of ingredients ex: mango, banana, orange etc")
        if st.button('Suggest') and num_of_recipes:
            
            (suggest(num_of_recipes, text))
