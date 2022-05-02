"""
Inference utilities.
"""
import os
from typing import Callable, Optional, Sequence

import numpy as np
from tensorflow.keras.models import Model

from dgd._download import get_default_weights_path, download_weights_to
from dgd.config import Config
from dgd.data import NDFloat32Array, preprocess
from dgd.model import make_model
from dgd.video import video_to_landmarks


def load_pretrained_model(weights_path: str = get_default_weights_path()) -> Model:
    model = make_model()
    if not os.path.isfile(weights_path):
        download_weights_to(weights_path)
    model.load_weights(weights_path)
    return model


def predict_video(
        video_path: Optional[str] = None,  # None will start a webcam.
        model: Optional[Model] = None,
        max_num_frames: int = Config.seq_length,  # For the pre-trained model.
        padding: bool = True,
        preprocess_fn: Callable[[NDFloat32Array], NDFloat32Array] = preprocess
) -> Sequence[float]:
    if model is None:
        model = load_pretrained_model()
    landmarks = video_to_landmarks(video_path, max_num_frames, padding)
    prediction: Sequence[float] = model.predict(
        np.expand_dims(preprocess_fn(np.array(landmarks)), axis=0)
    )[0].tolist()
    return prediction


if __name__ == "__main__":
    print(predict_video(model=load_pretrained_model(f"../training/{Config.weights_filename}")))
