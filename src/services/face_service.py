from __future__ import annotations
import pathlib
import math
import logging
from typing import Sequence, Optional, List

import cv2
import numpy as np
from fastapi import UploadFile, HTTPException, status

from src.core.config import settings
from src.models.domain.face import FaceIdentity
from src.models.schemas.identify import IdentifyResponse
from src.utils.image import read_image_from_upload
import itertools

logger = logging.getLogger(__name__)

THRESHOLD = 0.8


class FaceService:

    def __init__(self) -> None:
        self._faces: List[FaceIdentity] = []
        self._detector = cv2.dnn.readNetFromCaffe(
            settings.face_detector_prototxt,
            settings.face_detector_model,
        )
        self._embedder = cv2.dnn.readNetFromTorch(settings.face_embedder_model)

    def preload_faces(self) -> None:
        db_dir = pathlib.Path(settings.faces_db_path)
        if not db_dir.exists():
            raise FileNotFoundError(f"faces_db path '{db_dir}' not found")

        self._faces.clear()
        for img_path in itertools.chain(db_dir.glob("*.jpg"), db_dir.glob("*.png")):
            image = cv2.imread(str(img_path))
            if image is None:
                logger.warning("Не читается %s", img_path)
                continue
            try:
                vec = self._extract_embedding(image)
                self._faces.append(FaceIdentity(person_id=img_path.stem, embedding=vec))
            except Exception as exc:
                logger.error("Ошибка с обработкой изоброжения %s: %s", img_path, exc)

        logger.info("Загружено эмбеддинги лиц: %d", len(self._faces))

    def list_faces(self) -> List[FaceIdentity]:
        return self._faces

    def compute_embedding(self, img: np.ndarray) -> Sequence[float]:
        return self._extract_embedding(img)

    def find_best_match(self, query_vec: Sequence[float]) -> tuple[Optional[str], float]:
        best_dist = float("inf")
        best_id: Optional[str] = None
        for face in self._faces:
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(query_vec, face.embedding)))
            if dist < best_dist:
                best_dist = dist
                best_id = face.person_id
        return best_id, best_dist

    async def identify_face(self, file: UploadFile) -> IdentifyResponse:
        img = read_image_from_upload(file)
        try:
            q_vec = self.compute_embedding(img)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid face image")

        best_id, best_dist = self.find_best_match(q_vec)
        matched = (best_id is not None and best_dist <= THRESHOLD)
        return IdentifyResponse(matched=matched, person_id=best_id if matched else None)


    def _extract_embedding(self, img: np.ndarray) -> List[float]:
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104, 177, 123))
        self._detector.setInput(blob)
        detections = self._detector.forward()

        if detections.shape[2] == 0:
            raise ValueError("not founded")
        i = np.argmax(detections[0, 0, :, 2])
        conf = float(detections[0, 0, i, 2])
        if conf < 0.5:
            raise ValueError("low confidence")

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        x1, y1, x2, y2 = box.astype(int)
        face = img[y1:y2, x1:x2]
        if face.size == 0:
            raise ValueError("empty face crop")

        face_blob = cv2.dnn.blobFromImage(face, 1/255, (96, 96), (0, 0, 0), swapRB=True)
        self._embedder.setInput(face_blob)
        vec = self._embedder.forward().flatten()
        return vec.tolist()


face_service = FaceService()
