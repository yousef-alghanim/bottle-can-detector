import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request
from ultralytics import YOLO
from werkzeug.utils import secure_filename


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
RESULT_FOLDER = BASE_DIR / "static" / "results"
MODEL_PATH = BASE_DIR / "best.pt"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

model = YOLO(str(MODEL_PATH))


def allowed_file(filename: str) -> bool:
    """Check whether the uploaded file has a supported extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result_image = None
    detections = []

    if request.method == "POST":
        if "image" not in request.files:
            error = "No image was submitted."
            return render_template("index.html", error=error)

        uploaded_file = request.files["image"]

        if uploaded_file.filename == "":
            error = "Please select an image."
            return render_template("index.html", error=error)

        if not allowed_file(uploaded_file.filename):
            error = "Supported formats are PNG, JPG, JPEG, and WEBP."
            return render_template("index.html", error=error)

        original_name = secure_filename(uploaded_file.filename)
        extension = original_name.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{extension}"

        upload_path = UPLOAD_FOLDER / unique_name
        uploaded_file.save(upload_path)

        try:
            results = model.predict(
                source=str(upload_path),
                conf=0.35,
                imgsz=640,
                verbose=False
            )

            result = results[0]

            annotated_image = result.plot()

            result_name = f"result_{unique_name}"
            result_path = RESULT_FOLDER / result_name

            import cv2

            cv2.imwrite(str(result_path), annotated_image)

            result_image = f"results/{result_name}"

            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls.item())
                    confidence = float(box.conf.item())
                    class_name = model.names[class_id]

                    detections.append(
                        {
                            "class_name": class_name,
                            "confidence": round(confidence * 100, 2)
                        }
                    )

        except Exception as exc:
            error = f"Prediction failed: {exc}"

    return render_template(
        "index.html",
        error=error,
        result_image=result_image,
        detections=detections
    )


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html",
        error="The uploaded image is too large. Maximum size is 10 MB."
    ), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)