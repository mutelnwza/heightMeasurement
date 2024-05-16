import cv2 
import math
import streamlit as st
from PIL import Image
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates


def draw_circle(x, y, img): 
    print("position added")
    cv2.circle(st.session_state['img'], (x, y), 3, (0,0,255), -1)   
    st.session_state['pos'].append([x,y])
    print(st.session_state['pos'])


def refobj(x,y,img):
    cv2.circle(st.session_state['img'],(x,y),3,(0,0,255),-1)
    st.session_state['refpos'].append([x,y])


def getdist(pos1,pos2):
    return math.dist(pos1,pos2)


def setstate(i):
    st.session_state.stage=i


if "stage" not in st.session_state:
    st.session_state.stage=0

if 'pos' not in st.session_state:
    st.session_state['pos'] = []

if 'refpos' not in st.session_state:
    st.session_state['refpos'] = []

if 'img' not in st.session_state:
    st.session_state['img'] = None

if 'heightinpixel' not in st.session_state:
    st.session_state['heightinpixel'] = []

if 'heightsum' not in st.session_state:
    st.session_state['heightsum'] = 0

st.title("Height Estimating")

if st.session_state.stage==0:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        imgraw = Image.open(uploaded_file)
        imgraw = imgraw.resize((500,500))

        st.session_state['img'] = np.array(imgraw)

        with imgraw:
            value=streamlit_image_coordinates(imgraw, key="pil")

            if value is not None:
                point = value["x"],value["y"]
                draw_circle(point[0],point[1],st.session_state['img'])
        
        st.button("continue",on_click=setstate,args=[2])

        st.image(st.session_state['img'])

if st.session_state.stage ==2:
    for i in range(len(st.session_state['pos'])-1):
        img=cv2.circle(st.session_state['img'],(st.session_state['pos'][i]),3, (0,0,255), -1)
        img=cv2.line(st.session_state['img'],st.session_state['pos'][i],st.session_state['pos'][i+1],(0,0,255),1)
        st.session_state['heightinpixel'].append(getdist(st.session_state['pos'][i],st.session_state['pos'][i+1]))

    for i in range(len(st.session_state['heightinpixel'])):
        st.session_state['heightsum'] += st.session_state['heightinpixel'][i]

    img2 = Image.fromarray(st.session_state['img'])

    with img2:
        value=streamlit_image_coordinates(img2,key="pil")

        if value is not None:
            point=value["x"],value["y"]
            refobj(point[0],point[1],img2)



    # if cv2.waitKey(0) == ord('a'):
    #     for i in range(len(pos)-1):
    #         heightinpixel.append(getdist(pos[i],pos[i+1]))
    #         # heightinpixel.append(abs(pos[i][1]-pos[i+1][1]))
    #         img=cv2.line(img, pos[i],pos[i+1],(0,0,255),1)
    #         print(i)
    #     for i in range(len(heightinpixel)):
    #         heightsum+=heightinpixel[i]


    # # cv2.destroyWindow("Original Picture")

    # cv2.imshow("heightline", img)
    # cv2.setMouseCallback("heightline",draw_circle)

    # if cv2.waitKey(0) == ord('a'):
    #     for i in range(len(pos)-1):
    #         refinpixel.append(abs(pos[i+1][1]-pos[i][1]))
    #         img=cv2.line(img,pos[i],pos[i+1],(0,0,255),1)

    # cv2.destroyWindow("heightline")

    # cv2.imshow("reference object",img)
    # height=float(input("input length of the reference object"))
    # if cv2.waitKey(0) == ord('q'):
    #     print("calculating")
    #     print(heightsum)
        
    #     pixel_per_cm = height/refinpixel[0]
    #     print("pixel per cm =",pixel_per_cm)
    #     cm = heightsum*pixel_per_cm
    #     cv2.putText(img, str(cm), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    #     cv2.destroyWindow("reference object")
    #     cv2.imshow("final height",img)
        
        

    # cv2.destroyAllWindows() 
