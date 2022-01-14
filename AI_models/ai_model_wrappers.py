import os
from enum import Enum
from tensorflow.keras.models import model_from_json


class ModelType(Enum):
    EMOTION_AUDIO = 1
    EMOTION_VIDEO = 2


model_names = {
    ModelType.EMOTION_AUDIO: "Emotion.Audio",
    ModelType.EMOTION_VIDEO: "Emotion.Video",
}


class EmotionRecognizer:
    def __init__(self) -> None:
        self.absolute_path = os.path.dirname(__file__)

        # TODO: make a path provider
        model_path_getter = lambda model_relative_path: os.path.join(
            self.absolute_path, model_relative_path
        )
        self.audio_model = ModelWrapper(
            model_path_getter("audio"), ModelType.EMOTION_AUDIO
        )
        self.video_model = ModelWrapper(
            model_path_getter("video"), ModelType.EMOTION_VIDEO
        )

    def predict_emotion_video(self, input):
        return self.video_model.predict(input)

    def predict_emotion_audio(self, input):
        return self.audio_model.predict(input)


class ModelWrapper:
    def __init__(self, model_dir: str, model_type: ModelType) -> None:
        self.model_name = model_names.get(model_type, "INVALID")
        self.model_dir = model_dir
        self.model_json = os.path.join(model_dir, "best.json")
        self.model_weights = os.path.join(model_dir, "best.hdf5")

        if not os.path.exists(model_dir):
            raise Exception(
                f"model: {self.model_name}  -> directory path: '{model_dir}' does not exist"
            )
        elif not os.path.exists(self.model_json):
            raise Exception(
                f"model: {self.model_name}  -> json file: '{self.model_json}' does not exist"
            )
        elif not os.path.exists(self.model_weights):
            raise Exception(
                f"model: {self.model_name}  -> weights file: '{self.model_weights}' does not exist"
            )

        with open(self.model_json, "r") as model_as_json:
            model_read = model_as_json.read()
            self.model = model_from_json(model_read)
            self.model.load_weights(self.model_weights)

    def predict(self, input):
        return self.model.predict(input)


if __name__ == "__main__":
    EmotionRecognizer()
