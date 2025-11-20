"""
API REST para Gestión de Tareas Empresariales
Implementa principios SOLID y patrones de diseño
Compatible con Python 3.13 y Vercel Deployment
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator
from datetime import datetime
from enum import Enum
import uuid

# ============= MODELS (Single Responsibility) =============

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Implementar autenticación",
                "description": "Agregar JWT a la API",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "john.doe@empresa.com",
                "due_date": "2024-12-31T23:59:59",
                "created_at": "2024-11-01T10:00:00",
                "updated_at": "2024-11-15T14:30:00"
            }
        }

# ============= REPOSITORY PATTERN (Dependency Inversion) =============

class TaskRepository:
    """Interface para repositorio de tareas (Abstracción)"""
    def create(self, task: TaskCreate) -> Task:
        raise NotImplementedError
    
    def get_all(self) -> List[Task]:
        raise NotImplementedError
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        raise NotImplementedError
    
    def update(self, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        raise NotImplementedError
    
    def delete(self, task_id: str) -> bool:
        raise NotImplementedError

class InMemoryTaskRepository(TaskRepository):
    """Implementación concreta del repositorio en memoria"""
    def __init__(self):
        self._tasks: dict[str, Task] = {}
    
    def create(self, task: TaskCreate) -> Task:
        task_id = str(uuid.uuid4())
        now = datetime.now()
        new_task = Task(
            id=task_id,
            **task.model_dump(),
            created_at=now,
            updated_at=now
        )
        self._tasks[task_id] = new_task
        return new_task
    
    def get_all(self) -> List[Task]:
        return list(self._tasks.values())
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)
    
    def update(self, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        updated_task = task.model_copy(update={
            **update_data,
            "updated_at": datetime.now()
        })
        self._tasks[task_id] = updated_task
        return updated_task
    
    def delete(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# ============= SERVICE LAYER (Business Logic) =============

class TaskService:
    """Capa de servicio para lógica de negocio"""
    def __init__(self, repository: TaskRepository):
        self._repository = repository
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Crear nueva tarea con validaciones de negocio"""
        if task_data.due_date and task_data.due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")
        return self._repository.create(task_data)
    
    def list_tasks(self, status: Optional[TaskStatus] = None, 
                   priority: Optional[TaskPriority] = None) -> List[Task]:
        """Listar tareas con filtros opcionales"""
        tasks = self._repository.get_all()
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)
    
    def get_task(self, task_id: str) -> Task:
        """Obtener tarea por ID"""
        task = self._repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        return task
    
    def update_task(self, task_id: str, task_update: TaskUpdate) -> Task:
        """Actualizar tarea existente"""
        task = self._repository.update(task_id, task_update)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        return task
    
    def delete_task(self, task_id: str) -> dict:
        """Eliminar tarea"""
        if not self._repository.delete(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        return {"message": f"Task {task_id} deleted successfully"}

# ============= API APPLICATION =============

app = FastAPI(
    title="Enterprise Task Management API",
    description="API REST para gestión de tareas con principios SOLID",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection
repository = InMemoryTaskRepository()
task_service = TaskService(repository)

# ============= ROUTES =============

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Task Management API",
        "version": "1.0.0"
    }

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Crear nueva tarea"""
    try:
        return task_service.create_task(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/tasks", response_model=List[Task])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
):
    """Listar todas las tareas con filtros opcionales"""
    return task_service.list_tasks(status, priority)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    """Obtener tarea por ID"""
    return task_service.get_task(task_id)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate):
    """Actualizar tarea existente"""
    return task_service.update_task(task_id, task_update)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    """Eliminar tarea"""
    return task_service.delete_task(task_id)

@app.get("/health")
def health_check():
    """Endpoint de salud para monitoreo"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "total_tasks": len(repository.get_all())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)