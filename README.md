# Face Recognition API

This project provides a FastAPI-based face recognition system that classifies uploaded images as either recognized ("not wild") or unrecognized ("wild"). The system supports adding new faces and uses token-based authentication for security.

## Features
- **Face Classification**: Identify if a face is known or unknown.
- **Add New Faces**: Upload and store new faces for future recognition.
- **Fast Processing**: Uses KDTree for optimized nearest neighbor search.
- **Authentication**: Secure API with Bearer token.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/face_recognition_api.git
cd face_recognition_api
```

2. **Create a virtual environment and activate it:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Setup

1. **Prepare Known Faces**
   - Place images of known people in the `known_faces/` directory.
   - Run the preprocessing script to generate face encodings:
   ```bash
   python preprocess.py
   ```

2. **Start the API**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. **Classify Face**
**Endpoint:** `POST /classify-face`

**Headers:**
```
Authorization: Bearer your_secure_auth_token
```

**Request:**
```
Form-data:
- file: (image file)
```

**Response:**
```json
{
    "message": "Face recognized as John_Doe.",
    "status": "not wild"
}
```

### 2. **Add a New Face**
**Endpoint:** `POST /add-face`

**Headers:**
```
Authorization: Bearer your_secure_auth_token
```

**Request:**
```
Form-data:
- file: (image file)
- name: "Person_Name"
```

**Response:**
```json
{
    "message": "Face for Person_Name added successfully.",
    "status": "success"
}
```

## Deployment
To deploy the FastAPI server using Docker:

1. **Build the Docker image:**
```bash
docker build -t face_recognition_api .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 face_recognition_api
```

## License
This project is licensed under the MIT License.

---
**Maintainer:** Your Name (@yourgithub)
