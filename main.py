import streamlit as st
import numpy as np
import cv2
from pyzbar.pyzbar import decode
from isbnlib import meta, is_isbn10, is_isbn13
from isbnlib.registry import bibformatters
# from camera_input_live import camera_input_live


SERVICE = "openl"
bibtex = bibformatters["bibtex"]

# cap = cv2.VideoCapture(0)

results = set()

stream, info = st.columns(2)
with stream:
    img_holder = st.empty()
with info:
    res_holder = st.empty()
    inf_holder = st.empty()
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
    count = 0
    stop = st.button("Stop")

# value = camera_input_live(debounce=100)

# while value is not None:
value = st.camera_input("take")
if value:
    bytes_data = value.getvalue()
    frame = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    # Capture frame-by-frame
    res = decode(frame)
    if res:
        isbn = res[0][0].decode("utf-8")
        if isbn not in results:
            results.add(isbn)
        else:
            pass
            
        res_holder.write(results)
        if is_isbn10(isbn) or is_isbn13(isbn):
            res = meta(isbn, SERVICE)
            if res is not None:
                try:
                    inf_holder.write(bibtex(res))
                except AttributeError:
                    inf_holder.write(res)
            else:
                inf_holder.write("Not found")
        else:
            inf_holder.write("Bad format")
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_holder.image(gray)
    count += 1

from camera_input_live import camera_input_live


