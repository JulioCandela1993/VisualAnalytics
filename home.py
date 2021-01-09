import streamlit as st
from PIL import Image


def app():
    st.title("Tobacco: a silent killer")
    
    st.markdown('''
    Smoking is considered one of the biggest public health threats by the World Health Organization (WHO)
    ''')
    
    image = Image.open('img/smoking.jpg')

    st.image(image, caption='',
          use_column_width=True)
#app()
