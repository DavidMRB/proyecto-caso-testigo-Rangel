"""
Tests de Integración para API REST
Pruebas de endpoints completos con FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app, TaskStatus, TaskPriority

@pytest.fixture
def client():
    """Cliente de pruebas de FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_task():
    """Datos de muestra para crear tarea"""
    return {
        "title": "Integration Test Task",
        "description": "Testing API integration",
        "priority": "high",
        "status": "pending",
        "assigned_to": "tester@company.com",
        "due_date": (datetime.now() + timedelta(days=5)).isoformat()
    }

# ============= HEALTH CHECK TESTS =============

def test_root_endpoint(client):
    """Test 1: Verificar endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_health_endpoint(client):
    """Test 2: Verificar endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "total_tasks" in data

# ============= CREATE TASK TESTS =============

def test_create_task_success(client, sample_task):
    """Test 3: Crear tarea exitosamente"""
    response = client.post("/tasks", json=sample_task)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == sample_task["title"]
    assert data["priority"] == sample_task["priority"]
    assert "id" in data
    assert "created_at" in data

def test_create_task_minimal_data(client):
    """Test 4: Crear tarea con datos mínimos"""
    minimal_task = {"title": "Minimal Task"}
    response = client.post("/tasks", json=minimal_task)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["priority"] == "medium"  # Default
    assert data["status"] == "pending"   # Default

def test_create_task_invalid_title_short(client):
    """Test 5: Rechazar título muy corto"""
    invalid_task = {"title": "ab"}
    response = client.post("/tasks", json=invalid_task)
    assert response.status_code == 422  # Validation error

def test_create_task_missing_title(client):
    """Test 6: Rechazar tarea sin título"""
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_create_task_past_due_date(client):
    """Test 7: Rechazar fecha de vencimiento pasada"""
    task = {
        "title": "Past Due Task",
        "due_date": (datetime.now() - timedelta(days=1)).isoformat()
    }
    response = client.post("/tasks", json=task)
    assert response.status_code == 400
    assert "past" in response.json()["detail"].lower()

# ============= READ TASKS TESTS =============

def test_list_tasks_empty(client):
    """Test 8: Listar tareas cuando está vacío"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_tasks_with_data(client, sample_task):
    """Test 9: Listar tareas con datos"""
    # Crear dos tareas
    client.post("/tasks", json=sample_task)
    client.post("/tasks", json={"title": "Second Task"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2

def test_list_tasks_filter_by_status(client, sample_task):
    """Test 10: Filtrar tareas por estado"""
    # Crear tareas con diferentes estados
    task1 = sample_task.copy()
    task1["status"] = "pending"
    client.post("/tasks", json=task1)
    
    task2 = sample_task.copy()
    task2["title"] = "Completed Task"
    task2["status"] = "completed"
    client.post("/tasks", json=task2)
    
    # Filtrar por pending
    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["status"] == "pending" for task in tasks)

def test_list_tasks_filter_by_priority(client, sample_task):
    """Test 11: Filtrar tareas por prioridad"""
    task1 = sample_task.copy()
    task1["priority"] = "urgent"
    client.post("/tasks", json=task1)
    
    task2 = sample_task.copy()
    task2["title"] = "Low Priority Task"
    task2["priority"] = "low"
    client.post("/tasks", json=task2)
    
    response = client.get("/tasks?priority=urgent")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["priority"] == "urgent" for task in tasks)

def test_get_task_by_id(client, sample_task):
    """Test 12: Obtener tarea específica por ID"""
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task["title"]

def test_get_nonexistent_task(client):
    """Test 13: Intentar obtener tarea inexistente"""
    response = client.get("/tasks/nonexistent-id-12345")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# ============= UPDATE TASK TESTS =============

def test_update_task_success(client, sample_task):
    """Test 14: Actualizar tarea exitosamente"""
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    update_data = {
        "title": "Updated Title",
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"
    assert data["id"] == task_id

def test_update_task_partial(client, sample_task):
    """Test 15: Actualización parcial de tarea"""
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Solo actualizar estado
    response = client.put(f"/tasks/{task_id}", json={"status": "completed"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "completed"
    assert data["title"] == sample_task["title"]  # Sin cambios

def test_update_nonexistent_task(client):
    """Test 16: Intentar actualizar tarea inexistente"""
    response = client.put("/tasks/fake-id", json={"title": "New Title"})
    assert response.status_code == 404

# ============= DELETE TASK TESTS =============

def test_delete_task_success(client, sample_task):
    """Test 17: Eliminar tarea exitosamente"""
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verificar que ya no existe
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client):
    """Test 18: Intentar eliminar tarea inexistente"""
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404

# ============= WORKFLOW TESTS =============

def test_complete_crud_workflow(client):
    """Test 19: Flujo completo CRUD"""
    # CREATE
    task_data = {
        "title": "Workflow Test Task",
        "description": "Testing complete workflow",
        "priority": "medium"
    }
    create_resp = client.post("/tasks", json=task_data)
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]
    
    # READ
    read_resp = client.get(f"/tasks/{task_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["title"] == task_data["title"]
    
    # UPDATE
    update_resp = client.put(f"/tasks/{task_id}", json={"status": "completed"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"
    
    # DELETE
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    
    # VERIFY DELETION
    verify_resp = client.get(f"/tasks/{task_id}")
    assert verify_resp.status_code == 404

def test_concurrent_operations(client, sample_task):
    """Test 20: Operaciones concurrentes"""
    # Crear múltiples tareas
    task_ids = []
    for i in range(5):
        task = sample_task.copy()
        task["title"] = f"Concurrent Task {i}"
        response = client.post("/tasks", json=task)
        task_ids.append(response.json()["id"])
    
    # Verificar que todas existen
    response = client.get("/tasks")
    tasks = response.json()
    assert len(tasks) >= 5
    
    # Actualizar todas
    for task_id in task_ids:
        client.put(f"/tasks/{task_id}", json={"status": "completed"})
    
    # Verificar actualizaciones
    completed_tasks = client.get("/tasks?status=completed").json()
    assert len(completed_tasks) >= 5