import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_file, output_dir, classes):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        image_id = root.find('filename').text.split('.')[0]

        print(f"Processing file: {xml_file}")

        with open(f"{output_dir}/{image_id}.txt", "w") as yolo_file:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in classes:
                    continue
                class_id = classes.index(class_name)
                bndbox = obj.find('bndbox')
                xmin = float(bndbox.find('xmin').text)
                xmax = float(bndbox.find('xmax').text)
                ymin = float(bndbox.find('ymin').text)
                ymax = float(bndbox.find('ymax').text)
                b_width = float(root.find('size').find('width').text)
                b_height = float(root.find('size').find('height').text)

                print(f"Object: {class_name}, xmin: {xmin}, xmax: {xmax}, ymin: {ymin}, ymax: {ymax}, width: {b_width}, height: {b_height}")

                
                if xmin >= xmax or ymin >= ymax:
                    print(f"Invalid bounding box for {class_name} in {xml_file}")
                    continue

                x_center = (xmin + xmax) / 2.0 / b_width
                y_center = (ymin + ymax) / 2.0 / b_height
                width = (xmax - xmin) / b_width
                height = (ymax - ymin) / b_height

                print(f"YOLO format: {class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

                yolo_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")


output_dir = "C:/Users/WorkStation/Desktop/OCR-Esdras/YOLO_labels"
os.makedirs(output_dir, exist_ok=True)
classes = ["placa de veiculo"]  


annotations_dir = "C:/Users/WorkStation/Desktop/OCR-Esdras/placas-OCR/Annotations" 
for xml_file in os.listdir(annotations_dir):
    if xml_file.endswith(".xml"):
        convert_voc_to_yolo(os.path.join(annotations_dir, xml_file), output_dir, classes)
