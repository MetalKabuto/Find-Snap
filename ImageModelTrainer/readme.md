# Python Image Trainer #

### Purpose ###

main.py trains and pickles an image predictor as model.p intended for use in the FindNSnap API.

### Use ###

1. Download 'main.py' and 'requirements.txt'
2. Install Python 3.11
3. Make sure you have the required dependencies, a virtual environment is recommended ('pip install -r requirements.txt' from the root folder)
4. Create a folder named 'data' in the same folder as your local 'main.py'
5. Add a subfolder to 'data' for each category you want to train the model on. The folder should contain image files and the folder name will be the name of the category.
6. Run 'python3 main.py' from the root folder
7. Wait....