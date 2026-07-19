# Bottle and Can Detector

A Dockerized Flask web application that uses a custom-trained
YOLOv8 model to detect bottles and metal cans in uploaded images.

## Project Overview

The application allows users to upload an image through a web
interface. The trained YOLO model processes the image and returns:

- Bounding boxes around detected objects
- Predicted class names
- Confidence scores
- An annotated output image

## Detected Classes

1. Bottle
2. Metal can

## Technologies Used

- Python
- Flask
- Ultralytics YOLOv8
- OpenCV
- Gunicorn
- Docker
- HTML and CSS

## Project Structure

```text
bottle-can-detector/
├── app.py
├── best.pt
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    ├── uploads/
    └── results/
