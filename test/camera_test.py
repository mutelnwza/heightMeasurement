import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import math
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_js_eval import streamlit_js_eval

def reset():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def getdist(pos1, pos2):
    return math.dist(pos1, pos2)

def stage2():
    if len(st.session_state['pos']) > 1:
        st.session_state.stage = 2
        st.session_state['img'] = imgraw
        for i in range(len(st.session_state['pos']) - 1):
            st.session_state['heightinpixel'].append(getdist(st.session_state['pos'][i], st.session_state['pos'][i + 1]))
    else:
        st.text("please mark the locations")

    for i in range(len(st.session_state['heightinpixel'])):
        st.session_state['heightsum'] += st.session_state['heightinpixel'][i]

def stage3():
    if st.session_state['refincm'] != 0 and st.session_state['refpos'] != []:
        st.session_state['refincm'] = float(st.session_state['refincm'])
        st.session_state.stage = 3
        st.session_state['img'] = img
    elif st.session_state['refincm'] == 0:
        st.text("please input height of the reference object")
    elif st.session_state['refpos'] == []:
        st.text("please mark the positions of the reference object")

def undo():
    if st.session_state.stage == 0 and len(st.session_state["pos"]) > 0:
        st.session_state["pos"].pop()
    elif st.session_state.stage == 2 and len(st.session_state["refpos"]) > 0:
        st.session_state["refpos"].pop()
    st.rerun()

if "stage" not in st.session_state:
    st.session_state.stage = 0

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

# Add JavaScript to listen for Ctrl + Z and call the undo function
undo_js = """
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'z') {
        window.streamlitApi.runMethod('undo')
    }
});
"""
streamlit_js_eval(js_expressions=undo_js)

st.title("Height Estimating")

if st.session_state.stage == 0:
    option = st.selectbox("Choose image source", ("Upload an image", "Capture from webcam"))
    
    if option == "Upload an image":
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            imgraw = Image.open(uploaded_file)
            imgraw = imgraw.resize((800, 800))
            st.session_state['img'] = np.array(imgraw)
    elif option == "Capture from webcam":
        try:
            camera_image = st.camera_input("Take a picture")
            if camera_image is not None:
                imgraw = Image.open(camera_image)
                imgraw = imgraw.resize((800, 800))
                st.session_state['img'] = np.array(imgraw)
            else:
                st.warning("Please capture an image using the webcam.")
        except Exception as e:
            st.error(f"Error accessing the camera: {e}")

    if st.session_state['img'] is not None:
        imgraw = Image.fromarray(st.session_state['img'])
        with imgraw:
            st.text("Click to mark positions of your body parts, position recommended:\n-top of your head\n-neck\n-hip (only one side)\n-knee (only one side)\n-ankle (only one side)\n-heel (only one side)")
            draw = ImageDraw.Draw(imgraw)

            if st.button("Undo", key="undo_button"):
                undo()

            positionmarked = len(st.session_state["pos"])

            # count position marked then draw circle
            for i in range(positionmarked):
                circle = [st.session_state["pos"][i][0] - 3, st.session_state["pos"][i][1] - 3, st.session_state["pos"][i][0] + 3, st.session_state["pos"][i][1] + 3]
                draw.ellipse(circle, fill="red")

            # draw line
            if positionmarked > 1:
                for i in range(positionmarked - 1):
                    draw.line([st.session_state['pos'][i][0], st.session_state['pos'][i][1], st.session_state['pos'][i + 1][0], st.session_state['pos'][i + 1][1]], fill="red", width=0)

            value = streamlit_image_coordinates(imgraw, key="pil")

            if value is not None and st.session_state.stage == 0:
                point = value["x"], value["y"]
                if list(point) not in st.session_state["pos"] and list(point) not in st.session_state["refpos"]:
                    st.session_state['pos'].append([point[0], point[1]])
                    st.experimental_rerun()

        st.button("Continue", on_click=stage2, key="continue_button")
        st.button("Reset", on_click=reset, key="reset_button")

if st.session_state.stage == 2:
    img = st.session_state['img']
    with img:
        st.text("Please mark the location of the reference object")
        draw = ImageDraw.Draw(img)
        positionmarked = len(st.session_state["refpos"])

        # count position marked then draw circle
        for i in range(positionmarked):
            circle = [st.session_state["refpos"][i][0] - 3, st.session_state["refpos"][i][1] - 3, st.session_state["refpos"][i][0] + 3, st.session_state["refpos"][i][1] + 3]
            draw.ellipse(circle, fill=(0, 0, 255))

        # draw line
        if positionmarked > 1:
            for i in range(positionmarked - 1):
                draw.line([st.session_state['refpos'][i][0], st.session_state['refpos'][i][1], st.session_state['refpos'][i + 1][0], st.session_state['refpos'][i + 1][1]], fill=(0, 0, 255), width=0)

        click = streamlit_image_coordinates(img, key="ref_pos")

        if click is not None:
            point = click["x"], click["y"]
            if list(point) not in st.session_state["refpos"] and list(point) not in st.session_state["pos"]:
                st.session_state['refpos'].append([point[0], point[1]])
                st.rerun()

    st.session_state['refincm'] = st.number_input("Input height of the reference object (cm)", key="ref_height_input")
    st.button("Start Calculation", on_click=stage3, key="start_calc_button")

if st.session_state.stage == 3:
    for i in range(len(st.session_state['refpos']) - 1):
        st.session_state['refinpixel'].append(getdist(st.session_state['refpos'][i], st.session_state['refpos'][i + 1]))

    for i in range(len(st.session_state['refinpixel'])):
        st.session_state['refsum'] += st.session_state['refinpixel'][i]

    # calculation
    pixel_per_cm = st.session_state['refincm'] / st.session_state['refsum']
    heightestimated = st.session_state['heightsum'] * pixel_per_cm

    img = st.session_state['img']

    st.image(img)
    st.text('The estimated height is ' + str(int(heightestimated)) + ' cm')
    st.button("Back to Upload", on_click=reset, key="back_to_upload_button")

