import streamlit as st
from PIL import Image
from ClarifaiAPI import FoodRecognizer


from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_pb2, rpc_status_pb2

st.set_page_config('ZeroWaste', ':cook:') 
with open('Instructions.txt') as f:
    Instruction = f.read()
    
if 'food items' not in st.session_state:
    st.session_state['food items'] = []

food_recognizer = FoodRecognizer(st.secrets['PAT'])

def suggest(food_tags,num_of_rcps):
    system=f'''
    Provide {num_of_rcps} recipe suggestions for these food items: {food_tags}
    Write in this structure:
    **dish name**
    1. 
    2. 
    3. 
    Don't write ingredients.
    '''
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2.V2Stub(channel)

    # Define the request parameters
    request = service_pb2.PostModelOutputsRequest(
        # This is the model ID of the Clarifai LLM
        model_id=st.secrets['PAT'],
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    text=resources_pb2.Text(
                        content=prompt
                    )
                )
            )
        ]
    )

    # Call the Clarifai API
    response = stub.PostModelOutputs(request, metadata=('',))
    if response.status.code != status_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    # Get the answer from the response
    answer = response.outputs[0].data.text

    return answer




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
                st.error('AI cannot recognize item!')
        st.write('Food Items Recognized:')
        for item in st.session_state['food items']:
            st.markdown(f'- {item}')

        if st.button('Clear'):
            st.session_state['food items'] = []

        if st.button('Suggest') and st.session_state['food items']:
            st.write(suggest(num_of_rcps, st.session_state['food items']))
        
            
    else:
        text = st.text_input("Enter the name of ingredients ex: mango, banana, orange etc")
        if st.button('Suggest') and num_of_recipes:
            st.write(suggest(text, num_of_recipes))
