import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import ultralytics
import os
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model_path = 'AI_model/besfdsdat.pt'
output_labels_path = 'outputs/labels'
output_images_path = 'outputs/images'

model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

def predict(image_path, model_path, conf_threshold=0.2, iou_threshold=0.45):
  
    model.conf = conf_threshold  # порог уверенности
    model.iou = iou_threshold    # порог NMS
    
    img = Image.open(image_path)
    results = model(img)
    # results.show()
    preds = results.xyxy[0].cpu().numpy()

    label_path = os.path.join(output_labels_path, os.path.splitext(os.path.basename(image_path))[0] + '.txt')
    with open(label_path, 'w') as f:
        for pred in preds:
            x1, y1, x2, y2, conf, cls = pred
            # Конвертация координат в формат YOLO
            img_width, img_height = img.size
            x_center = (x1 + x2) / 2 / img_width
            y_center = (y1 + y2) / 2 / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height
            f.write(f'{int(cls)} {x_center} {y_center} {width} {height}\n')
    print(f'Saved YOLO labels to {label_path}')
    return results

def picture_handling(input_image_path, model_path, output_images_path):
    results = predict(input_image_path, model_path)

    annotated_img = results.render()[0]
    annotated_img = Image.fromarray(annotated_img)
    annotated_img_path = os.path.join(output_images_path, os.path.basename(input_image_path))
    annotated_img.save(annotated_img_path)
    print(f'Saved annotated image to {annotated_img_path}')
    
    return (annotated_img_path)
