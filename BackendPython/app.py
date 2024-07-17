import os
import numpy as np
from skimage import io, transform
import pickle
from dotenv import load_dotenv
from flask_cors import CORS
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

#Contants:
IMAGE_DIR = 'category_images'
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
DEFAULT_IMAGE = 'noimage.png'


def load_model(path):
    """Load the pre-trained model from a pickle file."""
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model

def prepare_image(image_stream, target_size=(15, 15)):
    """Load, resize and preprocess the image from the stream."""
    img = io.imread(image_stream)
    img = transform.resize(img, target_size, anti_aliasing=True)
    img = img.flatten().reshape(1, -1)  # Reshape to 2D array with one sample
    return img

def predict(model, img_array):
    """Make predictions with the model and return formatted results."""
    prediction = model.predict_proba(img_array)[0]
    categories = model.classes_
    results = {str(category): f"{prob * 100:.2f}%" for category, prob in zip(categories, prediction)}
    return results

@app.route('/')
def hello():
    return "Version 0.02. Welcome to the Find n Snap API!\n/predict - predicts an image"

@app.route('/categories', methods=['GET'])
def get_categories():
    """Return the list of categories the model can predict."""
    try:
        categories = model.classes_
        response = {}
        for category in categories:
            response.update({category:"/images/" + category})

        return jsonify(categories.tolist())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve images
@app.route("/images/<path:category_name>")
def download_file(category_name):
    # Check for the file with different extensions
    for ext in IMAGE_EXTENSIONS:
        file_path = Path(IMAGE_DIR, f"{category_name}.{ext}")
        if Path.exists(file_path):
            return send_from_directory(IMAGE_DIR, f"{category_name}.{ext}", as_attachment=True)
    
    return send_from_directory(IMAGE_DIR, DEFAULT_IMAGE, as_attachment=True)

# Route to predict image category matching
@app.route('/predict', methods=['POST'])
def predict_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        image_file = request.files['image']
        image_stream = BytesIO(image_file.read())

        # Prepare the image
        img_array = prepare_image(image_stream)

        # Predict using the model
        results = predict(model, img_array)

        # Return the results as JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

model_path = Path('./models/model_fruitanimals_jpeg_jpg.p')
model = load_model(model_path)

if __name__ == "__main__":
    # Load the model once when the server starts


    # Run the Flask server locally on the specified port (for development on your local machine)
    app.run(debug=True, host="127.0.0.1", port=5000)

    #app.run(debug=True, host="0.0.0.0")
