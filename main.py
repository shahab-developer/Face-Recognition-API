from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sklearn.neighbors import KDTree
import face_recognition
import pickle
import numpy as np
import os

# Initialize FastAPI
app = FastAPI()

# Authentication token
AUTH_TOKEN = "your_secure_auth_token"

# Directory and file for storing known faces and encodings
KNOWN_FACES_DIR = "known_faces"
ENCODINGS_FILE = "encodings.pkl"

# Class for handling token-based authentication
class TokenAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if credentials.scheme != "Bearer" or credentials.credentials != AUTH_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid or missing authentication token.")
        return credentials.credentials

# Load cached face encodings
if not os.path.exists(ENCODINGS_FILE):
    raise FileNotFoundError("Encodings file not found. Run preprocess.py to generate encodings.")

with open(ENCODINGS_FILE, "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Build KDTree for fast matching
kdtree = KDTree(np.array(known_face_encodings))

@app.get("/")
def root():
    """Root endpoint to verify the API is running."""
    return {"message": "Face Recognition API is live!"}

@app.post("/classify-face")
async def classify_face(
    file: UploadFile = File(...),
    token: str = Depends(TokenAuth())
):
    """Classify an uploaded image as 'wild' or 'not wild'."""
    try:
        if not file.filename.endswith(("jpg", "jpeg", "png")):
            raise HTTPException(status_code=400, detail="Invalid file format. Only jpg, jpeg, and png are allowed.")

        # Load image and process it
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) == 0:
            return {"message": "No face detected in the image.", "status": "wild"}

        # Match faces using KDTree
        for face_encoding in face_encodings:
            distances, indices = kdtree.query([face_encoding], k=1)
            if distances[0][0] < 0.6:  # Similarity threshold
                recognized_name = known_face_names[indices[0][0]]
                return {"message": f"Face recognized as {recognized_name}.", "status": "not wild"}

        return {"message": "Face is not recognized.", "status": "wild"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/add-face")
async def add_face(
    file: UploadFile = File(...),
    name: str = None,
    token: str = Depends(TokenAuth())
):
    """Endpoint to add a new face image to the known faces."""
    try:
        if not file.filename.endswith(("jpg", "jpeg", "png")):
            raise HTTPException(status_code=400, detail="Invalid file format. Only jpg, jpeg, and png are allowed.")

        if not name:
            raise HTTPException(status_code=400, detail="Name of the person must be provided.")

        # Load image and extract face encodings
        image = face_recognition.load_image_file(file.file)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) == 0:
            raise HTTPException(status_code=400, detail="No face detected in the image.")

        # Save the image to the known faces directory
        new_face_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
        with open(new_face_path, "wb") as f:
            f.write(await file.read())

        # Update encodings and names
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)

        # Update KDTree and encodings cache
        kdtree = KDTree(np.array(known_face_encodings))
        
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump((known_face_encodings, known_face_names), f)

        return {"message": f"Face for {name} added successfully.", "status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")