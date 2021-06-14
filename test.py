from helperModule import *
from tensorflow.keras.models import model_from_json
import time
import os

if __name__ == "__main__":
    AI_MODELS_DIR = os.path.join(os.getcwd(), 'AI_models/audio')
    t1 = time.time()
    with open(os.path.join(AI_MODELS_DIR, 'best.json'), 'r') as json_file:
        txt_model = json_file.read()
        model = model_from_json(txt_model)
        model.load_weights(os.path.join(AI_MODELS_DIR, 'best.hdf5'))
    print(time.time() - t1)
