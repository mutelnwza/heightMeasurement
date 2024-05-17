import cv2 
import math
import streamlit as st
from PIL import Image
from PIL import ImageDraw
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_js_eval import streamlit_js_eval

def resize(img_original, img_input):
    if img_original == "1:1":
        return img_input.resize((800,800))
    if img_original == "3:4":
        return img_input.resize((600,800))
    if img_original == "9:16":
        return img_input.resize((360,640))


def reset():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")


def getdist(pos1,pos2):
    return math.dist(pos1,pos2)


def stage2():
    st.session_state.stage =2
    st.session_state['img'] = imgraw
    for i in range(len(st.session_state['pos'])-1):
        st.session_state['heightinpixel'].append(getdist(st.session_state['pos'][i],st.session_state['pos'][i+1]))


    for i in range(len(st.session_state['heightinpixel'])):
        st.session_state['heightsum'] += st.session_state['heightinpixel'][i]

def stage3():
    if st.session_state['refincm'] != 0:
        st.session_state.stage =3
        st.session_state['img'] = img
    else:
        

if "stage" not in st.session_state:
    st.session_state.stage=0

if 'pos' not in st.session_state:
    st.session_state['pos'] = []

if 'refpos' not in st.session_state:
    st.session_state['refpos'] = []

if 'refinpixel' not in st.session_state:
    st.session_state['refinpixel'] = []

if 'refsum' not in st.session_state:
    st.session_state['refsum'] = 0

if 'img' not in st.session_state:
    st.session_state['img'] = None

if 'heightinpixel' not in st.session_state:
    st.session_state['heightinpixel'] = []

if 'heightsum' not in st.session_state:
    st.session_state['heightsum'] = 0


st.title("Height Estimating")

if st.session_state.stage==0:
    imgsize = st.radio("Choose the image retio",["1:1","3:4","9:16"])
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        imgraw = Image.open(uploaded_file)
        imgraw = resize(imgsize, imgraw)

        st.session_state['img'] = np.array(imgraw)

        with imgraw:
            st.text("click to mark positions of your bodyparts, position recommended:\n-top of your head\n-neck\n-hip(only one side)\n-knee (only one side)\n-ankle(only one side)\n-heel(only one side)")
            draw = ImageDraw.Draw(imgraw)

            positionmarked= len(st.session_state["pos"])

            # count position marked then draw circle
            for i in range(positionmarked):
                circle=[st.session_state["pos"][i][0]-3,st.session_state["pos"][i][1]-3,st.session_state["pos"][i][0]+3,st.session_state["pos"][i][1]+3]
                draw.ellipse(circle,fill="red")
            
            # draw line
            if positionmarked > 1:
                for i in range(positionmarked-1):
                    draw.line([st.session_state['pos'][i][0],st.session_state['pos'][i][1],st.session_state['pos'][i+1][0],st.session_state['pos'][i+1][1]],fill="red",width=0)

            value=streamlit_image_coordinates(imgraw, key="pil")

            if value is not None and st.session_state.stage==0:
                point = value["x"],value["y"]
                if list(point) not in st.session_state["pos"] and list(point) not in st.session_state["refpos"]:
                    st.session_state['pos'].append([point[0],point[1]])
                    st.experimental_rerun()

            # if position clicked is not on the list, append it then reload the website to show the lastest update
        
        st.button("continue",on_click=stage2)
        st.button("reset", on_click=reset) # F5


if st.session_state.stage ==2:

    st.text(st.session_state['heightsum'])
    
    img = st.session_state['img']
    st.text(st.session_state['heightinpixel'])
    with img:
        draw = ImageDraw.Draw(img)
        positionmarked= len(st.session_state["refpos"])

        # count position marked then draw circle
        for i in range(positionmarked):
            circle=[st.session_state["refpos"][i][0]-3,st.session_state["refpos"][i][1]-3,st.session_state["refpos"][i][0]+3,st.session_state["refpos"][i][1]+3]
            draw.ellipse(circle,fill=(0,0,255))

        # draw line
        if positionmarked > 1:
            for i in range(positionmarked-1):
                draw.line([st.session_state['refpos'][i][0],st.session_state['refpos'][i][1],st.session_state['refpos'][i+1][0],st.session_state['refpos'][i+1][1]],fill=(0,0,255),width=0)

        click=streamlit_image_coordinates(img, key="x")

        if click is not None:
            point = click["x"],click["y"]
            if list(point) not in st.session_state["refpos"] and list(point) not in st.session_state["pos"]:
                st.session_state['refpos'].append([point[0],point[1]])
                st.experimental_rerun()
    
    st.session_state['refincm'] = st.number_input("input height of the reference object (cm)")
    st.button("start calculation", on_click=stage3)


if st.session_state.stage ==3:
    for i in range(len(st.session_state['refpos'])-1):
        st.session_state['refinpixel'].append(getdist(st.session_state['refpos'][i],st.session_state['refpos'][i+1]))

    for i in range(len(st.session_state['refinpixel'])):
        st.session_state['refsum'] += st.session_state['refinpixel'][i]

    # calculation
    refcm = float(st.session_state['refincm'])
    pixel_per_cm = refcm/st.session_state['refsum']
    heightestimated = st.session_state['heightsum']*pixel_per_cm

    img = st.session_state['img']

    st.image(img)
    st.text(heightestimated)
    st.button("back to upload", on_click=reset)

