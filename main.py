
import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer

st.set_page_config('ReServe', ':cook:')
st.title('ReServe :cook:')

if 'food items' not in st.session_state:
    st.session_state['food items'] = []

with open('about.txt') as f:
    about = f.read()

chatbot = ChatBot(dict(st.secrets['gcp_service_account']))
food_recognizer = FoodRecognizer(st.secrets['clarifai_api']['PAT'])

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
    response = chatbot.send_msg(prompt)
    return response

tab1, tab2 = st.tabs(['Recognize Food', 'About'])

with tab1:
    input = st.radio('Choose an input method:', ['Camera', 'Text'])
    num_of_rcps = st.number_input('Select number of suggested recipes:', 1, 3, 1, 1)

    if input == 'Camera':
        buffer = st.camera_input('Take a picture of food items!')
        if buffer:
            img = Image.open(buffer)
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
            st.write(suggest(num_of_rcps, st.session_state['food items']))
    
    else:
        food_items = st.text_input('Input Food Items: (Ex: apple, orange, mango)')
        if st.button('Suggest') and food_items:
            st.write(suggest(num_of_rcps, food_items))


with tab2:
    st.markdown(about)
    st.image('logo.png')



'''import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer

st.set_page_config('ZeroWaste', ':cook:') 
with open('Instructions.txt') as f:
    Instruction = f.read()
    
if 'food items' not in st.session_state:
    st.session_state['food items'] = []
    
food_recognizer = FoodRecognizer(st.secrets['PAT'])

def suggest(dish, num_of_recipes):  # Function to suggest dishes from the ingredients given to it 
    prompt = f'''
   ''' Suggest me {num_of_recipes} recipes from {dish}
    Should follow the following template:
    **Dish Name**
    1. 
    2.
    3.
    4.
    '''
    '''return "hello"


    
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
