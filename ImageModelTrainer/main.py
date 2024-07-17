import os
import pickle
from pathlib import Path

from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import m2cgen as m2c            # for model-to-code
from PIL import Image           # for making dataset smaller
import sys
sys.setrecursionlimit(5000)     # helps issue with model-to-code hitting recursion limit

def prepare_data(model_name = Path('model_experiment')):
    input_dir = Path("data_images")
    output_model_path = model_name
    data = []
    labels = []
# Iterate through each subfolder in the input directory and dynamically add categories
    for category in os.listdir(input_dir):
        category_path = Path(input_dir, category)
        if category_path.is_dir():
        #if category == 'banana' or category == 'car':          # set certain categories to train a model on
            print("loading " + str(category_path) + " folder", end='')
            for file in os.listdir(category_path):
                print(".", end='')
                img_path = category_path / file
                img = imread(img_path)
                img = resize(img, (15, 15))
                data.append(img.flatten())
                labels.append(category)
            print("DONE")
    print("Converting images to arrays...", end='')
    data = np.asarray(data)
    labels = np.asarray(labels)
    print("DONE")
# train / test split
    print("Splitting data to training and testing sets...", end='')
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)
    print("DONE")
    return output_model_path,x_train,x_test,y_train,y_test

def training_model(x_train, y_train):
# train classifier
    print("Setting up classifier......", end='')
    classifier = SVC(probability=True)
    print("DONE")
    parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10]}] # Made the C parameter and search process shorter to reduce training time and model complexity

    print("Setting up GridSearch...", end='')
    grid_search = GridSearchCV(classifier, parameters)
    print("...", end='')
    grid_search.fit(x_train, y_train)
    print("DONE")

    print("Extracting best estimator...", end='')
    best_estimator = grid_search.best_estimator_
    print("DONE")
    return best_estimator

def write_model_as_code(best_estimator):
    print("Converting model to c# code....")
    model_code = m2c.export_to_c_sharp(best_estimator)
    print("Saving to file...")
    with open(Path(f'{output_model_path}.cs'), 'w') as code_file:
        code_file.write(model_code)
    print("DONE\nModel code saved to file.")

def test_performance(x_test, y_test, best_estimator):
    print("Predicting test dataset...", end='')
    y_prediction = best_estimator.predict(x_test)
    print("...", end='')
    score = accuracy_score(y_prediction, y_test)
    print("DONE")
    return score

def resize_dataset(dataset_dir = Path("data_images"), max_dimension = 100):
    for folder in os.listdir(dataset_dir):
        count = 0
        changed = 0
        category_path = Path(dataset_dir, folder)
        if category_path.is_dir():
            print("resizing " + str(category_path) + " folder")
            for file in os.listdir(category_path):
                count+=1
                img_path = category_path / file
                img = Image.open(img_path)
                if max(img.size) > max_dimension:
                    if img.size[0] > img.size[1]:
                        diff = img.size[0]/max_dimension
                    else:
                        diff = img.size[1]/max_dimension
                    (h, w) = (round(img.size[0]/diff), round(img.size[1]/diff))
                    small_img = img.resize((h, w))
                    small_img.save(img_path)
                    changed+=1
            print('DONE {} of {}'.format(changed, count))

# step 0 (when adding new datasets). to make the dataset smaller: resize dataset images for each category folder to max height and width while keeping proportions.
#resize_dataset()

# step 1. prepare data
#output_model_path, x_train, x_test, y_train, y_test = prepare_data('model_bananacar')

# step 2. train model
#best_estimator = training_model(x_train, y_train)

# step 3 (optional). test performance
# score = test_performance(x_test, y_test, best_estimator)
# print('{}% of samples were correctly classified'.format(str(score * 100)))

# step 4 (optional). convert to C# code file for use in frontend
#write_model_as_code(best_estimator)

# step 5 (optional). save as pickle-file for use in python server
#pickle.dump(best_estimator, open(Path(f'{output_model_path}.p'), 'wb'))
#print("Model pickled and dumped to " + str(output_model_path+'.p'))