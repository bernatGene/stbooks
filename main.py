import streamlit as st
import cv2
from pyzbar.pyzbar import decode
from isbnlib import meta, is_isbn10, is_isbn13
from isbnlib.registry import bibformatters

SERVICE = "openl"
bibtex = bibformatters["bibtex"]

cap = cv2.VideoCapture(0)

results = set()

img_holder = st.empty()
res_holder = st.empty()
inf_holder = st.empty()
if not cap.isOpened():
    print("Cannot open camera")
    exit()
count = 0
scan = st.button("Scan")
stop = st.button("Stop")
while scan:
    if stop:
        break
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    res = decode(frame)
    if res:
        isbn = res[0][0].decode("utf-8")
        if isbn not in results:
            results.add(isbn)
        else:
            continue
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
    if count % 2  ==0 :
        img_holder.image(gray)
    count += 1
