import os, joblib

BASE_DIR = os.path.abspath("models")

def load_models(model_paths):
    models = {}

    for path in model_paths:
        abs_path = os.path.abspath(path)

        if not abs_path.startswith(BASE_DIR):
            raise Exception(f"Invalid model path: {path}")

        # extract clean name
        name = os.path.basename(path).lower()   # datatype_model_v2.pkl

        models[name] = joblib.load(abs_path)

    return models