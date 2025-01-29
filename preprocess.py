import os
import pickle
import face_recognition

KNOWN_FACES_DIR = "known_faces"
ENCODINGS_FILE = "encodings.pkl"

def create_encodings():
    known_face_encodings = []
    known_face_names = []
    
    for file_name in os.listdir(KNOWN_FACES_DIR):
        image_path = os.path.join(KNOWN_FACES_DIR, file_name)
        try:
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(os.path.splitext(file_name)[0])
        except IndexError:
            print(f"Warning: No face found in {file_name}. Skipping.")
    
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)
        print(f"Encodings saved to {ENCODINGS_FILE}.")

if __name__ == "__main__":
    create_encodings()