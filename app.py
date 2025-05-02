import streamlit as st
import cv2
import tempfile
from lane_detection import detect_lanes
import os

st.title("Road Lane Line Detection System")
uploaded_video = st.file_uploader("Upload a road video...", type=["mp4", "mov", "avi"])

if uploaded_video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    cap = cv2.VideoCapture(tfile.name)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_path = os.path.join("output_videos", "output.avi")
    out = cv2.VideoWriter(out_path, fourcc, 20.0, (640, 480))

    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))
        lanes = detect_lanes(frame)
        out.write(lanes)
        stframe.image(lanes, channels="BGR")

    cap.release()
    out.release()
    st.success("Lane detection complete! Check output_videos/output.avi")
