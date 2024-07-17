# minst python 3.10: 
# pip install m2cgen        # for converting .pickle to C#
# pip install numpy
# pip install -U scikit-learn
# pip install -U scikit-image

import numpy as np
from skimage import io, transform
import pickle
import json
from pathlib import Path

def load_model(path):
    """Load the pre-trained model from a pickle file."""
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model

def prepare_image(img_path, target_size=(15, 15)):
    """Load, resize and preprocess the image."""
    img = io.imread(img_path)
    img = transform.resize(img, target_size, anti_aliasing=True)
    img = img.flatten().reshape(1, -1)  # Reshape to 2D array with one sample
    return img

def predict(model, img_array):
    """Make predictions with the model and return formatted results."""
    prediction = model.predict_proba(img_array)[0]
    categories = model.classes_
    results = {str(category): f"{prob * 100:.2f}%" for category, prob in zip(categories, prediction)}
    return results

def save_results(results, file_path):
    """Save the results to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)

def main():
    model_path = Path('new_model.p')
    image_path = Path('test_image.jpg')
    result_path = Path('result.json')

    # Load the model
    model = load_model(model_path)
    print("Model loaded successfully.")  # Debugging line

    # Prepare the image
    img_array = prepare_image(image_path)
    print(f"Prepared Image Array: {img_array.shape}")  # Debugging line

    # Predict using the model
    results = predict(model, img_array)
    print(f"Formatted Results: {results}")  # Debugging line

    # Save results to a JSON file
    save_results(results, result_path)
    print(f"Results saved to {result_path}")  # Debugging line

    # Print results to terminal
    print("Prediction Results:")
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
