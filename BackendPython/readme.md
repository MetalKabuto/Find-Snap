# FindNSnap Backend API #

### Purpose ###

This script serves as an API endpoint for interacting with a pre-trained and pickled image model stored in the 'MODEL_PATH' path.

The API is intended to receive images from clients and return matching results per category.

### Version ###

The application should be run using a **Python 3.11** virtual environment.

Dependencies versions according to "./requirements.txt"

### Use ###

The directory is structured to be deployed in its entirety to [Google Cloud Services](https://cloud.google.com)

### API Endpoints ###

- **`/`**: Root endpoint to test the API. Returns a welcome message.
- **`/categories`**: Returns the list of categories the model can predict.
- **`/images/<path:category_name>`**: Serves images based on the category name.
- **`/predict`**: Accepts a POST request with an image file and returns the prediction results.

### Environment Variables ###

During development, you have a `.env` file in the root directory with the following variables:

- `FLASK_DEBUG`: Debug mode for Flask.

This is to ensure verbose logging for the deployed server during development.
Before publication and release of the app the server should be updated not to run in debug mode to increase security.

### Running the Application ###

To run the application locally, use the following command:

```sh
python app.py
# FindNSnap Backend API #

### Purpose ###

This script serves as an API endpoint for interacting with a pre-trained and pickled image model stored as "./model.p" in the root directory.

The API is intended to receive images from clients and return matching results per category.

### Version ###

The application should be run using the **Python 3.11** virtual environment stored in "./env"

Dependencies versions according to "./requirements.txt"

### Use ###

The directory is structured to be deployed in its entirety to [Google Cloud Services](https://cloud.google.com)

### Launching the server ###

Only available to administrators. Follow login to gcloud when prompted.

In CMD go to project working folder:
        > gcloud run deploy --source .
            Service name (backendpython):   findnsnapapi
            Please specify a region:        14 [for europe-north]

### Available models ###

+ model_bananacar: two categories for testing
+ model_fruitanimals_jpeg_jpg: ten categories of fruits, veggies and common animals