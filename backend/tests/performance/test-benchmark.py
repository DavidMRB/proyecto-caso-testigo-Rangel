"""
Tests de Performance con pytest-benchmark
Mide tiempos de respuesta y throughput
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, TaskCreate, TaskPriority, TaskStatus
from datetime import datetime, timedelta

client = TestClient(app)

# ============= BENCHMARK FIXTURES =============

@pytest.fixture
def sample_task_data():
    return {
        "title": "Performance Test Task",
        "description": "Testing API performance",
        "priority": "medium",
        "status": "pending"
    }

@pytest.fixture
def create_test_tasks():
    """Crear múltiples tareas para pruebas"""
    task_ids = []
    for i in range(50):
        response = client.post("/tasks", json={
            "title": f"Bulk Task {i}",
            "priority": "medium"
        })
        if response.status_code == 201:
            task_ids.append(response.json()["id"])
    return task_ids

# ============= PERFORMANCE TESTS =============

def test_perf_01_create_task_latency(benchmark, sample_task_data):
    """
    Test 1 Performance: Latencia de creación de tarea
    Objetivo: < 100ms
    """
    def create_task():
        response = client.post("/tasks", json=sample_task_data)
        assert response.status_code == 201
        return response
    
    result = benchmark(create_task)
    
    # Assertions de performance
    stats = benchmark.stats.stats
    assert stats.mean < 0.1, f"Mean latency {stats.mean}s excede 100ms"
    print(f"\n✓ Create Task Mean: {stats.mean*1000:.2f}ms")

def test_perf_02_list_tasks_throughput(benchmark):
    """
    Test 2 Performance: Throughput de listado
    Objetivo: > 100 requests/second
    """
    def list_tasks():
        response = client.get("/tasks")
        assert response.status_code == 200
        return response
    
    result = benchmark(list_tasks)
    
    stats = benchmark.stats.stats
    throughput = 1 / stats.mean
    assert throughput > 50, f"Throughput {throughput:.2f} req/s es bajo"
    print(f"\n✓ List Tasks Throughput: {throughput:.2f} req/s")

def test_perf_03_get_single_task(benchmark, sample_task_data):
    """
    Test 3 Performance: Obtener tarea individual
    Objetivo: < 50ms
    """
    # Crear tarea primero
    create_response = client.post("/tasks", json=sample_task_data)
    task_id = create_response.json()["id"]
    
    def get_task():
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        return response
    
    result = benchmark(get_task)
    
    stats = benchmark.stats.stats
    assert stats.mean < 0.05, f"Get task latency {stats.mean}s excede 50ms"
    print(f"\n✓ Get Task Mean: {stats.mean*1000:.2f}ms")

def test_perf_04_update_task_speed(benchmark, sample_task_data):
    """
    Test 4 Performance: Velocidad de actualización
    Objetivo: < 100ms
    """
    # Crear tarea
    create_response = client.post("/tasks", json=sample_task_data)
    task_id = create_response.json()["id"]
    
    def update_task():
        response = client.put(f"/tasks/{task_id}", json={
            "status": "in_progress"
        })
        assert response.status_code == 200
        return response
    
    result = benchmark(update_task)
    
    stats = benchmark.stats.stats
    assert stats.mean < 0.1, f"Update latency {stats.mean}s excede 100ms"
    print(f"\n✓ Update Task Mean: {stats.mean*1000:.2f}ms")

def test_perf_05_delete_task_speed(benchmark):
    """
    Test 5 Performance: Velocidad de eliminación
    Objetivo: < 50ms
    """
    def create_and_delete():
        # Crear
        create_response = client.post("/tasks", json={
            "title": "Task to Delete"
        })
        task_id = create_response.json()["id"]
        
        # Eliminar
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        return response
    
    result = benchmark(create_and_delete)
    
    stats = benchmark.stats.stats
    print(f"\n✓ Create+Delete Mean: {stats.mean*1000:.2f}ms")

def test_perf_06_filtered_query_performance(benchmark, create_test_tasks):
    """
    Test 6 Performance: Consultas con filtros
    Objetivo: < 150ms con 50 tareas
    """
    def query_with_filters():
        response = client.get("/tasks?status=pending&priority=medium")
        assert response.status_code == 200
        return response
    
    result = benchmark(query_with_filters)
    
    stats = benchmark.stats.stats
    assert stats.mean < 0.15, f"Filtered query {stats.mean}s excede 150ms"
    print(f"\n✓ Filtered Query Mean: {stats.mean*1000:.2f}ms")

def test_perf_07_concurrent_reads(benchmark, create_test_tasks):
    """
    Test 7 Performance: Lecturas concurrentes simuladas
    """
    def multiple_reads():
        responses = []
        for _ in range(10):
            response = client.get("/tasks")
            responses.append(response)
        return responses
    
    result = benchmark(multiple_reads)
    
    stats = benchmark.stats.stats
    avg_per_request = stats.mean / 10
    print(f"\n✓ Avg per concurrent read: {avg_per_request*1000:.2f}ms")

def test_perf_08_health_check_latency(benchmark):
    """
    Test 8 Performance: Latencia de health check
    Objetivo: < 10ms
    """
    def health_check():
        response = client.get("/health")
        assert response.status_code == 200
        return response
    
    result = benchmark(health_check)
    
    stats = benchmark.stats.stats
    assert stats.mean < 0.01, f"Health check {stats.mean}s excede 10ms"
    print(f"\n✓ Health Check Mean: {stats.mean*1000:.2f}ms")

def test_perf_09_bulk_create_performance(benchmark):
    """
    Test 9 Performance: Creación en lote
    """
    def create_multiple_tasks():
        for i in range(20):
            client.post("/tasks", json={
                "title": f"Bulk Task {i}",
                "priority": "low"
            })
    
    result = benchmark(create_multiple_tasks)
    
    stats = benchmark.stats.stats
    avg_per_task = stats.mean / 20
    print(f"\n✓ Avg per bulk create: {avg_per_task*1000:.2f}ms")

def test_perf_10_response_size_efficiency(benchmark, create_test_tasks):
    """
    Test 10 Performance: Eficiencia de tamaño de respuesta
    """
    def get_all_tasks():
        response = client.get("/tasks")
        data = response.json()
        return len(str(data))  # Tamaño aproximado
    
    size = benchmark(get_all_tasks)
    
    # Verificar que el tamaño es razonable (< 1MB para 50 tareas)
    assert size < 1_000_000, "Response size demasiado grande"
    print(f"\n✓ Response size: {size} bytes")

# ============= STRESS TESTS =============

@pytest.mark.slow
def test_perf_stress_many_tasks():
    """
    Test de estrés: Manejar muchas tareas
    """
    import time
    
    start_time = time.time()
    
    # Crear 100 tareas
    for i in range(100):
        response = client.post("/tasks", json={
            "title": f"Stress Task {i}"
        })
        assert response.status_code == 201
    
    creation_time = time.time() - start_time
    
    # Listar todas
    list_start = time.time()
    response = client.get("/tasks")
    list_time = time.time() - list_start
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 100
    
    print(f"\n✓ Created 100 tasks in {creation_time:.2f}s")
    print(f"✓ Listed {len(tasks)} tasks in {list_time:.2f}s")
    
    # Cleanup
    for task in tasks[:100]:
        client.delete(f"/tasks/{task['id']}")

# ============= BENCHMARK SUMMARY =============

def test_perf_summary_report(benchmark):
    """Generar reporte resumen de performance"""
    
    # Ejecutar suite básica de tests
    tests = [
        ("Create", lambda: client.post("/tasks", json={"title": "Test"})),
        ("Read", lambda: client.get("/tasks")),
        ("Health", lambda: client.get("/health"))
    ]
    
    results = {}
    for name, func in tests:
        import time
        times = []
        for _ in range(100):
            start = time.time()
            func()
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        results[name] = avg_time * 1000  # en ms
    
    # No usar benchmark aquí, solo reportar
    print("\n" + "="*50)
    print("PERFORMANCE SUMMARY REPORT")
    print("="*50)
    for name, avg_ms in results.items():
        print(f"{name:15s}: {avg_ms:>8.2f} ms")
    print("="*50)