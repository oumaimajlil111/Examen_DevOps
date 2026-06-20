# Ticket Management API

A FastAPI-based ticket management system with DevSecOps integration.

## Features

- Create tickets with title, description, and username
- View all tickets with optional status filtering
- Update ticket status and add agent responses
- Status validation (Ouvert, En cours, Résolu, Fermé)
- SQLite database with SQLAlchemy ORM
- Docker containerization support

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/oumaimajlil111/Examen_DevOps.git
cd Examen_DevOps
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Option 2: Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/oumaimajlil111/Examen_DevOps.git
cd Examen_DevOps
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Option 3: Kubernetes Deployment

1. Clone the repository:
```bash
git clone https://github.com/oumaimajlil111/Examen_DevOps.git
cd Examen_DevOps
```

2. Build the local image with the proper tag:
```bash
docker build -t examen-devops:latest .
```

3. Ensure you have a local Kubernetes cluster running:

**Option A: Docker Desktop with Kubernetes enabled**
- Open Docker Desktop
- Go to Settings → Kubernetes
- Enable Kubernetes
- **Important**: Under "Cluster Settings", select "kubernetes" (NOT "kind")
- Click "Apply & Restart"
- Wait for Kubernetes to start

**Option B: Minikube**
```bash
minikube start
```

**Option C: Kind**
```bash
kind create cluster
```

3. Apply the Kubernetes configurations:
```bash
# Deploy the application (creates 2 replicas)
kubectl apply -f k8s-deployment.yml

# Expose the application via NodePort service
kubectl apply -f k8s-service.yml
```

4. Verify the deployment:
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

5. Access the API:

**For Docker Desktop Kubernetes:**
```bash
# The API is accessible directly via localhost
# Access the API at: http://localhost:30080/docs
```

**For Minikube:**
```bash
# Get the service URL
minikube service examen-devops-service --url
# Or access directly: http://localhost:30080
```

**For Kind:**
```bash
# Get the node port and access via the node IP
kubectl get services examen-devops-service
# Access via: http://<NODE_IP>:30080/docs
```

The API will be available at `http://localhost:30080/docs` for Docker Desktop and Minikube

If you need to reapply the service configuration after making changes:
```bash
kubectl apply -f k8s-service.yml
```

## Testing

### Manual Testing

Use curl or any HTTP client to test the endpoints:

**Create a ticket:**
```bash
curl -X POST http://localhost:8000/tickets/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Ticket","description":"This is a test","username":"testuser"}'
```

**Get all tickets:**
```bash
curl http://localhost:8000/tickets/
```

**Filter tickets by status:**
```bash
curl "http://localhost:8000/tickets/?status=Ouvert"
```

**Update ticket status:**
```bash
curl -X PUT http://localhost:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"En cours","response":"Working on it"}'
```

### Automated Testing

Run the test suite:
```bash
pytest app/test_main.py -v
```

## API Endpoints

- `POST /tickets/` - Create a new ticket
- `GET /tickets/` - Get all tickets (optional status filter)
- `PUT /tickets/{ticket_id}` - Update ticket status and response

## Project Structure

```
Examen_DevOps/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # Database configuration
│   └── test_main.py     # Test suite
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── k8s-deployment.yml   # Kubernetes deployment configuration
├── k8s-service.yml      # Kubernetes service configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Environment Variables

- `DATABASE_URL` - Database connection string (default: `sqlite:///./tickets.db`)
- `TESTING` - Set to `1` to skip automatic table creation during testing

## Troubleshooting

**Port already in use:**
- Change the port in docker-compose.yml or use a different port with uvicorn

**Database errors:**
- Ensure the database file has write permissions
- Check that SQLAlchemy is properly installed

**Import errors:**
- Make sure you're running from the project root directory
- Verify all dependencies are installed

**Fatal error in launcher (Windows Python reinstall issue):**
```
Fatal error in launcher: Unable to create process using '"C:\Program Files\Python310\python.exe"  "C:\Users\i\AppData\Roaming\Python\Python310\Scripts\uvicorn.exe" app.main:app --reload --host 0.0.0.0 --port 8000': The system cannot find the file specified.
```
This happens when you uninstall an older Python version and install a fresh one on Windows. Windows keeps a dirty caching shortcut (uvicorn.exe) in your roaming app data folder that points to the old, deleted Python path.

**Solution:**
- Delete the stale cache folder: `C:\Users\{your_username}\AppData\Roaming\Python\Python310\Scripts\`
- Reinstall uvicorn: `pip install uvicorn`
- Or use the Python module directly: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Or use a virtual environment (venv) to avoid system-wide cache issues:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # On Windows
  pip install -r requirements.txt
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
