import io
import cv2
import numpy as np
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Smart Photo Editor")

st.title("Smart Photo Editor")
st.write("Upload your photo and add filters..")
st.sidebar.header("Filter settings")

uploaded_file = st.file_uploader("Pick photo..", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    if image.mode != "RGB":
        image = image.convert("RGB")
        
    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original photo")
        st.image(img_array, use_container_width=True)

    filter_option = st.sidebar.selectbox(
        "Pick effect: ",
        [
            "Original",
            "Black-white",
            "Blur",
            "Add brightness",
            "Invert",
            "Color Splash",
        ],
    )

    splash_color = None
    if filter_option == "Color Splash":

        splash_color = st.sidebar.radio(
            "Select color to keep:", ["Red", "Green", "Blue", "Yellow"]
        )

    processed_img = img_array.copy()

    if filter_option == "Black-white":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        processed_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    elif filter_option == "Blur":
        processed_img = cv2.GaussianBlur(img_array, (21, 21), 0)

    elif filter_option == "Add brightness":
        processed_img = cv2.convertScaleAbs(img_array, alpha=1.0, beta=75)

    elif filter_option == "Invert":
        processed_img = 255 - img_array

    elif filter_option == "Color Splash":
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        if splash_color == "Red":
            low_red1 = np.array([0, 40, 40])
            high_red1 = np.array([10, 255, 255])
            low_red2 = np.array([170, 40, 40])
            high_red2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(img_hsv, low_red1, high_red1)
            mask2 = cv2.inRange(img_hsv, low_red2, high_red2)
            mask = cv2.bitwise_or(mask1, mask2)

        elif splash_color == "Green":
            low_green = np.array([35, 40, 40])
            high_green = np.array([85, 255, 255])
            mask = cv2.inRange(img_hsv, low_green, high_green)

        elif splash_color == "Blue":
            low_blue = np.array([90, 40, 40])
            high_blue = np.array([130, 255, 255])
            mask = cv2.inRange(img_hsv, low_blue, high_blue)

        elif splash_color == "Yellow":
            low_yellow = np.array([20, 40, 40])
            high_yellow = np.array([35, 255, 255])
            mask = cv2.inRange(img_hsv, low_yellow, high_yellow)

        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        mask_3channel = np.expand_dims(mask, axis=2)
        processed_img = np.where(mask_3channel > 0, img_array, gray_3channel)

    with col2:
        st.subheader("Photo with filters")
        st.image(processed_img, use_container_width=True)

        result_image = Image.fromarray(processed_img)

        buf = io.BytesIO()
        result_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download",
            data=byte_im,
            file_name="smart_edit.jpeg",
            mime="image/jpeg",
        )