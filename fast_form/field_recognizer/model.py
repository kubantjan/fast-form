import json
import logging
import os

from keras.models import model_from_json

logger = logging.getLogger(__name__)


def load_model(model_structure_path, model_weights_path):

    # load model structure
    with open(model_structure_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)

    # load model weights
    loaded_model.load_weights(model_weights_path)
    logger.debug(f"Loaded model {os.path.basename(model_structure_path)} from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
                         optimizer='adam',  # using the Adam optimiser
                         metrics=['accuracy'])  # reporting the accuracy

    return loaded_model


def load_result_mapper(path):
    with open(path, 'r') as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}
