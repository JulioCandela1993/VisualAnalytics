import streamlit as st
from PIL import Image


def app():
    st.title("Tobacco: a silent killer")
    image = Image.open('img/smoking.jpg')

    st.image(image, caption='',
          use_column_width=True)
#app()
