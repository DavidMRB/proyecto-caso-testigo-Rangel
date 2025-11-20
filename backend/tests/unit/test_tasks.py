"""
Tests Unitarios para Task Management API
Cobertura de modelos, servicios y repositorios
"""
import pytest
from datetime import datetime, timedelta
from app.main import (
    Task, TaskCreate, TaskUpdate, TaskPriority, TaskStatus,
    InMemoryTaskRepository, TaskService
)
from fastapi import HTTPException

# ============= FIXTURES =============

@pytest.fixture
def repository():
    """Fixture para repositorio limpio"""
    return InMemoryTaskRepository()

@pytest.fixture
def service(repository):
    """Fixture para servicio con repositorio"""
    return TaskService(repository)

@pytest.fixture
def sample_task_data():
    """Datos de ejemplo para crear tarea"""
    return TaskCreate(
        title="Test Task",
        description="Test Description",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING,
        assigned_to="test@example.com",
        due_date=datetime.now() + timedelta(days=7)
    )

# ============= MODEL TESTS =============

def test_task_create_valid():
    """Test 1: Crear tarea con datos válidos"""
    task = TaskCreate(
        title="Valid Task",
        description="Valid description",
        priority=TaskPriority.MEDIUM
    )
    assert task.title == "Valid Task"
    assert task.priority == TaskPriority.MEDIUM
    assert task.status == TaskStatus.PENDING

def test_task_title_validation():
    """Test 2: Validar longitud mínima del título"""
    with pytest.raises(ValueError):
        TaskCreate(title="ab")  # Menos de 3 caracteres

def test_task_title_strip_whitespace():
    """Test 3: Validar que se eliminen espacios del título"""
    task = TaskCreate(title="  Test Task  ")
    assert task.title == "Test Task"

def test_task_empty_title_rejected():
    """Test 4: Rechazar título vacío"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        TaskCreate(title="   ")

# ============= REPOSITORY TESTS =============

def test_repository_create_task(repository, sample_task_data):
    """Test 5: Crear tarea en repositorio"""
    task = repository.create(sample_task_data)
    assert task.id is not None
    assert task.title == sample_task_data.title
    assert task.created_at is not None
    assert task.updated_at is not None

def test_repository_get_all_tasks(repository, sample_task_data):
    """Test 6: Obtener todas las tareas"""
    task1 = repository.create(sample_task_data)
    task2 = repository.create(TaskCreate(title="Second Task"))
    
    all_tasks = repository.get_all()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks

def test_repository_get_by_id(repository, sample_task_data):
    """Test 7: Obtener tarea por ID"""
    created_task = repository.create(sample_task_data)
    retrieved_task = repository.get_by_id(created_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title

def test_repository_get_nonexistent_task(repository):
    """Test 8: Intentar obtener tarea inexistente"""
    task = repository.get_by_id("nonexistent-id")
    assert task is None

def test_repository_update_task(repository, sample_task_data):
    """Test 9: Actualizar tarea existente"""
    task = repository.create(sample_task_data)
    
    update = TaskUpdate(
        title="Updated Title",
        status=TaskStatus.COMPLETED
    )
    updated_task = repository.update(task.id, update)
    
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.updated_at > task.updated_at

def test_repository_delete_task(repository, sample_task_data):
    """Test 10: Eliminar tarea"""
    task = repository.create(sample_task_data)
    assert repository.delete(task.id) is True
    assert repository.get_by_id(task.id) is None

def test_repository_delete_nonexistent_task(repository):
    """Test 11: Intentar eliminar tarea inexistente"""
    result = repository.delete("nonexistent-id")
    assert result is False

# ============= SERVICE TESTS =============

def test_service_create_task(service, sample_task_data):
    """Test 12: Crear tarea a través del servicio"""
    task = service.create_task(sample_task_data)
    assert task.id is not None
    assert task.title == sample_task_data.title

def test_service_create_task_past_due_date(service):
    """Test 13: Rechazar tarea con fecha de vencimiento pasada"""
    task_data = TaskCreate(
        title="Past Due Task",
        due_date=datetime.now() - timedelta(days=1)
    )
    
    with pytest.raises(ValueError, match="Due date cannot be in the past"):
        service.create_task(task_data)

def test_service_list_tasks(service, sample_task_data):
    """Test 14: Listar todas las tareas"""
    service.create_task(sample_task_data)
    service.create_task(TaskCreate(title="Second Task"))
    
    tasks = service.list_tasks()
    assert len(tasks) == 2

def test_service_filter_tasks_by_status(service):
    """Test 15: Filtrar tareas por estado"""
    service.create_task(TaskCreate(title="Pending Task", status=TaskStatus.PENDING))
    service.create_task(TaskCreate(title="Completed Task", status=TaskStatus.COMPLETED))
    
    pending_tasks = service.list_tasks(status=TaskStatus.PENDING)
    assert len(pending_tasks) == 1
    assert pending_tasks[0].status == TaskStatus.PENDING

def test_service_filter_tasks_by_priority(service):
    """Test 16: Filtrar tareas por prioridad"""
    service.create_task(TaskCreate(title="High Priority", priority=TaskPriority.HIGH))
    service.create_task(TaskCreate(title="Low Priority", priority=TaskPriority.LOW))
    
    high_priority = service.list_tasks(priority=TaskPriority.HIGH)
    assert len(high_priority) == 1
    assert high_priority[0].priority == TaskPriority.HIGH

def test_service_get_task(service, sample_task_data):
    """Test 17: Obtener tarea específica"""
    created_task = service.create_task(sample_task_data)
    retrieved_task = service.get_task(created_task.id)
    
    assert retrieved_task.id == created_task.id

def test_service_get_nonexistent_task(service):
    """Test 18: Intentar obtener tarea inexistente"""
    with pytest.raises(HTTPException) as exc_info:
        service.get_task("nonexistent-id")
    
    assert exc_info.value.status_code == 404

def test_service_update_task(service, sample_task_data):
    """Test 19: Actualizar tarea"""
    task = service.create_task(sample_task_data)
    
    update = TaskUpdate(status=TaskStatus.IN_PROGRESS)
    updated_task = service.update_task(task.id, update)
    
    assert updated_task.status == TaskStatus.IN_PROGRESS

def test_service_delete_task(service, sample_task_data):
    """Test 20: Eliminar tarea"""
    task = service.create_task(sample_task_data)
    result = service.delete_task(task.id)
    
    assert "deleted successfully" in result["message"]
    
    with pytest.raises(HTTPException):
        service.get_task(task.id)