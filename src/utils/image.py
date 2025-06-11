import numpy as np
import cv2
from fastapi import UploadFile


def read_image_from_upload(file: UploadFile) -> np.ndarray:
    content = file.file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Cannot decode image from upload")
    return img


def preprocess_face_image(img: np.ndarray, target_size: tuple[int, int] = (96, 96)) -> np.ndarray:
    face = cv2.resize(img, target_size)
    face = face.astype("float32") / 255.0
    return face
