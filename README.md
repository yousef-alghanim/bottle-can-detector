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
```

## Prerequisites

- Docker installed and running, with support for Linux containers.
- Git to clone the repository, or a downloaded and extracted repository ZIP.
- Internet access for the image build to download the base image and dependencies.
- A web browser and a test image containing bottles or metal cans.

The Docker image provides Python 3.11 and the project dependencies; no local Python
environment is required. The trained model, `best.pt`, is included in the repository,
so no separate model download or training step is needed.

## Docker Quickstart

Clone the repository, then build and run the image from the repository root:

```bash
git clone https://github.com/yousef-alghanim/bottle-can-detector.git
cd bottle-can-detector
docker build -t bottle-can-detector .
docker run --rm -p 5000:5000 bottle-can-detector
```

If you downloaded the ZIP, open a terminal in the extracted project directory and
start with the `docker build` command.

Wait for Gunicorn to start, then open [http://localhost:5000](http://localhost:5000)
in your browser. The Dockerfile starts Gunicorn on container port 5000 by default;
`-p 5000:5000` maps it to port 5000 on your machine. That host port must be free.

To stop the container, find its ID with `docker ps` and run
`docker stop <container-id>` in another terminal. The quickstart uses `--rm`, so
stopping the container removes it along with its uploaded images and results.

## Supported Images

- Supported filename extensions: `.png`, `.jpg`, `.jpeg`, and `.webp`
  (case-insensitive).
- The total upload request is limited to 10 MiB (10 × 1024 × 1024 bytes),
  shown as "10 MB" in the application. Keep the image below this limit because
  the multipart request also includes form overhead.
- Upload a valid image; a supported extension alone does not guarantee it can
  be decoded.

## Detection Workflow

1. Select an image in the browser and click **Run Detection**.
2. Flask saves the upload under `static/uploads/` with a unique filename and runs
   the bundled `best.pt` model with a confidence threshold of 0.35 and
   `imgsz=640`.
3. The application saves an annotated image under `static/results/` and displays
   it with detected class names and confidence percentages. If no objects pass
   the threshold, the page displays a no-detections message.

The upload and result directories are created automatically when the app starts.

## Manual Smoke Test

After starting the container, load the page, submit a supported image below the
request limit, and check that the result image loads. The page should show either
detected objects with confidence percentages or the no-detections message.
A successful upload does not guarantee that every bottle or can will be detected.

### Verification Status

These instructions were checked against the repository's Dockerfile, dependencies,
application code, upload form, and Docker ignore rules, including the presence of
`best.pt`. Docker was unavailable in the documentation review environment, so the
image build, container startup, and real-model predictions were not executed.
The quickstart and smoke test describe source-based expectations, not a completed
end-to-end test.
