# ZeroWaste

Link : https://zerowaste-vedant.streamlit.app/

## Inspiration
The motivation behind our project stems from the unfortunate reality of surplus food often ending up wasted. Our vision revolves around creating a web application that harnesses the power of Artificial Intelligence (AI) to capture images of leftover food and propose inventive ways to transform them into delectable dishes.

## Functionality
ZeroWaste, our web application, offers users the choice to either capture an image of their leftover food or manually input the food items. Employing computer vision technology, the application identifies various food tags within the images. Subsequently, these recognized food items are passed to a natural language chatbot, which ingeniously suggests diverse methods to repurpose the surplus food.

## Development Process
To realize our project, we integrated a computer vision model sourced from the Clarifai food recognition API into our web application. Additionally, we leveraged the natural language processing capabilities of the PaLM 2 for Chat API to build the chatbot component. These models were harmoniously integrated and packaged within a Streamlit-based web application.

## Challenges Faced
Our journey encountered challenges, notably in safeguarding the security of the API keys used in the web application. However, we triumphed over this hurdle by encrypting the API keys using Streamlit secrets in TOML format, ensuring robust protection.

## Noteworthy Achievements
We take pride in the successful deployment of an AI-powered solution that amalgamates computer vision and natural language processing. ZeroWaste represents a user-friendly platform that assists in repurposing leftover food, contributing significantly to sustainability endeavors.
