from keras.models import model_from_json


def load_model(model_structure_path, model_weights_path):
    # load json and create model
    # json_file = open('model_data/model.json', 'r')

    # load model structure
    with  open(model_structure_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    # loaded_model.load_weights("model_data/model.h5")

    # load model weights
    loaded_model.load_weights(model_weights_path)
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy',  # using the cross-entropy loss function
                         optimizer='adam',  # using the Adam optimiser
                         metrics=['accuracy'])  # reporting the accuracy

    return loaded_model


# scores = model.evaluate(x_test, y_test, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1] * 100))

def load_result_mapper(path):
    with open(path) as f:
        s = f.read()[:-1]  # remove last char \n
    a = [l.split(" ") for l in s.split("\n")]
    res_mapper = {int(l[0]): chr(int(l[1])) for l in a}
    return res_mapper
