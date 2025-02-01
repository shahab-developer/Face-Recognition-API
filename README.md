# Face Recognition Attendance System

A FastAPI-based application for marking attendance using face recognition. This system allows you to:
- Register employees with their face images.
- Mark attendance by recognizing faces in real-time.
- Generate attendance reports for employees.

---

## Features

- **Employee Management**:
  - Add new employees with name, department, and position.
  - Upload employee face images for registration.
  - Fetch a list of all employees.

- **Attendance Management**:
  - Mark attendance by uploading an image containing a face.
  - Fetch attendance records for specific employees.

- **Authentication**:
  - JWT-based authentication for secure access.
  - Role-based access control (future implementation).

- **Face Recognition**:
  - Uses **MTCNN** for face detection.
  - Uses **FaceNet** for face encoding.
  - Uses **FAISS** for fast face matching.

---

## Technologies Used

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Face Recognition**: MTCNN, FaceNet, FAISS
- **Authentication**: JWT
- **Caching**: Redis (optional)
- **Deployment**: Docker

---

## Setup and Installation

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- PostgreSQL (or any other supported database)

---

## Local Setup

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/face-attendance-system.git
   cd face-attendance-system
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your database credentials and other settings:
   ```env
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=secret
   POSTGRES_DB=attendance
   DATABASE_URL=postgresql+asyncpg://admin:secret@localhost:5432/attendance
   JWT_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   FACE_REC_THRESHOLD=0.7
   FACE_MODEL_PATH=./face_models/encoder/facenet_keras.h5
   ```

4. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the Application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

6. **Access the API**:
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.
   - Open [http://localhost:8000/redoc](http://localhost:8000/redoc) for the ReDoc UI.

---

## Server Setup

### Using Docker

1. **Build and Run the Application**:
   ```bash
   docker-compose up -d
   ```

2. **Run Database Migrations**:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

3. **Access the Application**:
   - The API will be available at `http://your-server-ip:8000`.

---

## API Endpoints

### Authentication

#### Login: `POST /auth/login`
**Body:**
```json
{
  "username": "admin",
  "password": "secret"
}
```

### Employees

#### Create Employee: `POST /employees`
**Body (form-data):**
- `name`: John Doe
- `department`: IT
- `position`: Developer
- `image`: (Upload employee photo)

#### Get Employee: `GET /employees/{employee_id}`
#### Get All Employees: `GET /employees`

### Attendance

#### Mark Attendance: `POST /attendance/mark`
**Body (form-data):**
- `image`: (Upload attendance photo)

#### Get Attendance Report: `GET /attendance/report/{employee_id}`

---

## Project Structure
```
face-attendance-system/
├── app/
│   ├── core/                 # Core configurations
│   ├── db/                   # Database configuration
│   ├── models/               # Database models
│   ├── routes/               # API endpoints
│   ├── services/             # Business logic
│   ├── utils/                # Helper functions
│   └── main.py               # FastAPI app setup
├── migrations/               # Database migrations
├── face_models/              # Face recognition models
├── tests/                    # Unit tests
├── docker-compose.yml        # Docker setup
├── Dockerfile
├── requirements.txt
├── .env.example              # Environment variables template
└── README.md
```

---

## Testing

### Unit Tests
Run the unit tests using:
```bash
pytest tests/
```

### API Testing
Use the provided Postman collection to test the API endpoints.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **FastAPI** for the web framework.
- **MTCNN** for face detection.
- **FaceNet** for face encoding.
- **FAISS** for fast face matching.

---

## Contact

For any questions or feedback, please contact:

- **Your Name**: your.email@example.com
- **Project Repository**: [GitHub Repo](https://github.com/your-repo)

---
