import os
from pathlib import Path
from PIL import Image   
                      
def convert_from_png(img, new_extension, new_path, old_path):
    new_img(img, new_path, new_extension)
    delete_img(old_path)                         
        
def new_img(img, new_path, ext_format):
    rgb_img = img.convert('RGB')
    rgb_img.save(new_path, format=ext_format)
    if Path.exists(new_path):
        print(f"img saved as {ext_format}")
    
def delete_img(file_path):
    file_path.unlink()
    if not Path.exists(file_path):
        print("removed file")
    else:
        print(f"file not removed {file_path}")

                
def png_to_jpeg(dataset_dir = Path("data_images")):
    dataset_dir = Path("data_images")
    for folder in os.listdir(dataset_dir):
        count = 0
        changed = 0
        category_path = Path(dataset_dir, folder)
        if category_path.is_dir():
            print("searching " + str(category_path) + " for png")
            for file in os.listdir(category_path):
                count+=1
                img_path = category_path / file
                name = file.split('.')[0]
                file_path_JPEG = Path(category_path, f"{name}.jpeg")
                file_path_png = Path(category_path, f"{name}.png")
                if Path.exists(file_path_png):
                    img = Image.open(img_path)
                    print(f"open img {file}")
                    new_img(img, file_path_JPEG, 'jpeg')
                    delete_img(file_path_png)
                    changed+=1
            print('DONE {} of {}'.format(changed, count))
