from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "leaf_model.keras"


CLASS_NAMES = [
    "Anthracnose",
    "Bacterial Canker",
    "Cutting Weevil",
    "Die Back",
    "Gall Midege",
    "Healthy",
    "Powdery Mildew",
    "Sooty Mould"
]


model = tf.keras.models.load_model(MODEL_PATH)


def predict_leaf(image_path):

    img = load_img(
        image_path,
        target_size=(260, 260)
    )

    img_array = img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": confidence,
        "confidence_percentage": round(
            confidence * 100,
            2
        )
    }