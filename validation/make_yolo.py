import json
import os
from pathlib import Path
import yaml
from PIL import Image

def convert(file, zip=True):
    # Convert Labelbox JSON labels to YOLO labels
    file = Path(file)
    
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f) # load JSON
        
    file_info = data['FileInfo']
    image_name = file_info['FileName']
    image_path = r"C:\Dev_2a\final_project\dataset\randomsplit\validation\images" + '\\' + image_name
    save_dir = Path(r"C:\Dev_2a\final_project\dataset\randomsplit\validation\labels")
    
    width = file_info['Width']
    height = file_info['Height']

    im = Image.open(image_path)
    im.save(save_dir / image_name, quality=95, subsampling=0)
    
    objects = data['ObjectInfo']['BoundingBox']
    names = [] # class names
    
    label_path = save_dir / image_name.replace('.jpg', '.txt')
    with open(label_path, 'w', encoding='utf-8') as label_file:
        for obj_name, obj_data in objects.items():
            names.append(obj_name)
            top, left, h, w = obj_data['Position']
            x_center = (left + w / 2) / width
            y_center = (top + h / 2) / height
            w_normalized = w / width
            h_normalized = h / height
                
            line = f"{names.index(obj_name)} {x_center} {y_center} {w_normalized} {h_normalized}\n"
            label_file.write(line)
                                    
    dataset_info = {
        'path': str(Path(r"C:\Dev_2a\final_project\dataset\randomsplit")),
        'train': str(Path(r"C:\Dev_2a\final_project\dataset\randomsplit\train\images")),
        'val': str(Path(r"C:\Dev_2a\final_project\dataset\randomsplit\validation\images")),
        'test': str(Path(r"C:\Dev_2a\final_project\dataset\randomsplit\test\images")),
        'nc': len(names),
        'names': names
    }
    
    with open(save_dir / 'dataset.yaml', 'w', encoding='utf-8') as dataset_file:
        yaml.dump(dataset_info, dataset_file, sort_keys=False)
        
    # Zip
    if zip:
        print(f'Zipping as {save_dir}.zip...')
        os.system(f'zip -qr {save_dir}.zip {save_dir}')
        
    print('Conversion completed successfully!')
    
if __name__ == '__main__':
    json_dir = Path(r"C:\Dev_2a\final_project\dataset\randomsplit\validation\json")
    
    for json_file in json_dir.glob('*.json'):
        convert(json_file)