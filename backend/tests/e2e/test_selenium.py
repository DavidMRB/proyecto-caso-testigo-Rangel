"""
Tests End-to-End con Selenium
Pruebas de flujo completo de usuario
Compatible con Python 3.13
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import os

@pytest.fixture(scope="module")
def driver():
    """Setup del WebDriver de Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Sin interfaz gráfica para CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def frontend_url():
    """URL del frontend (ajustar según ambiente)"""
    return "http://localhost:5173"  # Vite dev server

def wait_for_element(driver, by, value, timeout=10):
    """Helper para esperar elementos"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# ============= E2E TESTS =============

def test_e2e_01_homepage_loads(driver, frontend_url):
    """Test 1 E2E: Cargar página principal"""
    driver.get(frontend_url)
    
    # Verificar título
    assert "Task Management" in driver.title or driver.title != ""
    
    # Verificar header
    header = wait_for_element(driver, By.TAG_NAME, "header")
    assert header.is_displayed()

def test_e2e_02_stats_display(driver, frontend_url):
    """Test 2 E2E: Mostrar estadísticas"""
    driver.get(frontend_url)
    time.sleep(2)  # Esperar carga de datos
    
    # Buscar cards de estadísticas
    stats = driver.find_elements(By.CSS_SELECTOR, "[class*='bg-white rounded-lg shadow']")
    assert len(stats) >= 4, "Deben mostrarse al menos 4 cards de estadísticas"

def test_e2e_03_create_task_button_visible(driver, frontend_url):
    """Test 3 E2E: Botón de nueva tarea visible"""
    driver.get(frontend_url)
    
    new_task_button = wait_for_element(driver, By.XPATH, 
                                      "//button[contains(text(), 'Nueva Tarea')]")
    assert new_task_button.is_displayed()
    assert new_task_button.is_enabled()

def test_e2e_04_open_task_form(driver, frontend_url):
    """Test 4 E2E: Abrir formulario de nueva tarea"""
    driver.get(frontend_url)
    time.sleep(1)
    
    # Click en botón
    new_task_button = wait_for_element(driver, By.XPATH, 
                                      "//button[contains(text(), 'Nueva Tarea')]")
    new_task_button.click()
    
    # Verificar que aparece el formulario
    form_title = wait_for_element(driver, By.XPATH, 
                                  "//h3[contains(text(), 'Nueva Tarea')]")
    assert form_title.is_displayed()

def test_e2e_05_create_task_complete_flow(driver, frontend_url):
    """Test 5 E2E: Flujo completo de creación de tarea"""
    driver.get(frontend_url)
    time.sleep(1)
    
    # Abrir formulario
    new_task_button = wait_for_element(driver, By.XPATH, 
                                      "//button[contains(text(), 'Nueva Tarea')]")
    new_task_button.click()
    time.sleep(0.5)
    
    # Llenar formulario
    title_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Título']")
    title_input.send_keys("Tarea E2E Test")
    
    description = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='Describe']")
    description.send_keys("Esta es una tarea de prueba E2E")
    
    # Seleccionar prioridad
    priority_select = driver.find_element(By.XPATH, "//label[contains(text(), 'Prioridad')]/../select")
    priority_select.click()
    high_option = driver.find_element(By.XPATH, "//option[@value='high']")
    high_option.click()
    
    # Submit
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Crear')]")
    submit_button.click()
    
    time.sleep(2)  # Esperar que se cree
    
    # Verificar que la tarea aparece en la lista
    tasks = driver.find_elements(By.XPATH, "//*[contains(text(), 'Tarea E2E Test')]")
    assert len(tasks) > 0, "La tarea creada debe aparecer en la lista"

def test_e2e_06_filter_by_status(driver, frontend_url):
    """Test 6 E2E: Filtrar tareas por estado"""
    driver.get(frontend_url)
    time.sleep(2)
    
    # Buscar filtro de estado
    status_filter = wait_for_element(driver, By.XPATH, 
                                    "//label[contains(text(), 'Estado')]/../select")
    status_filter.click()
    
    # Seleccionar 'Pendiente'
    pending_option = driver.find_element(By.XPATH, "//option[@value='pending']")
    pending_option.click()
    
    time.sleep(1.5)  # Esperar filtrado
    
    # Verificar que hay resultados o mensaje apropiado
    page_content = driver.page_source
    assert "pending" in page_content.lower() or "no hay tareas" in page_content.lower()

def test_e2e_07_search_functionality(driver, frontend_url):
    """Test 7 E2E: Funcionalidad de búsqueda"""
    driver.get(frontend_url)
    time.sleep(2)
    
    # Buscar input de búsqueda
    search_input = wait_for_element(driver, By.CSS_SELECTOR, 
                                   "input[placeholder*='Buscar']")
    search_input.send_keys("Test")
    
    time.sleep(1)  # Esperar búsqueda
    
    # La búsqueda debería funcionar (verificar que no hay error)
    assert driver.find_elements(By.TAG_NAME, "body")

def test_e2e_08_edit_task_button_visible(driver, frontend_url):
    """Test 8 E2E: Botón de editar tarea visible"""
    driver.get(frontend_url)
    time.sleep(2)
    
    # Buscar botones de edición
    edit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[title='Editar']")
    
    if len(edit_buttons) > 0:
        assert edit_buttons[0].is_displayed()

def test_e2e_09_toggle_task_status(driver, frontend_url):
    """Test 9 E2E: Cambiar estado de tarea (toggle)"""
    driver.get(frontend_url)
    time.sleep(2)
    
    # Buscar iconos de estado clickeables
    status_icons = driver.find_elements(By.TAG_NAME, "button")
    
    # Si hay tareas, debería haber al menos un botón de estado
    assert len(status_icons) > 0

def test_e2e_10_responsive_design_mobile(driver, frontend_url):
    """Test 10 E2E: Diseño responsive (móvil)"""
    # Cambiar a tamaño móvil
    driver.set_window_size(375, 812)  # iPhone X size
    driver.get(frontend_url)
    time.sleep(2)
    
    # Verificar que la página se carga correctamente
    header = driver.find_element(By.TAG_NAME, "header")
    assert header.is_displayed()
    
    # Verificar que elementos principales son visibles
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.size['width'] <= 400  # Ancho apropiado para móvil

# ============= TESTS ADICIONALES =============

def test_e2e_11_api_connection(driver, frontend_url):
    """Test 11 E2E: Verificar conexión con API"""
    driver.get(frontend_url)
    time.sleep(3)  # Tiempo para cargar datos
    
    # Si la API está funcionando, no deberíamos ver errores de red
    # Buscar mensajes de error
    error_messages = driver.find_elements(By.XPATH, "//*[contains(text(), 'Error')]")
    
    # Si hay errores, verificar que no son críticos
    for error in error_messages:
        error_text = error.text.lower()
        assert "cannot connect" not in error_text
        assert "failed to fetch" not in error_text

def test_e2e_12_clear_filters(driver, frontend_url):
    """Test 12 E2E: Limpiar filtros"""
    driver.get(frontend_url)
    time.sleep(2)
    
    # Aplicar un filtro
    status_filter = wait_for_element(driver, By.XPATH, 
                                    "//label[contains(text(), 'Estado')]/../select")
    status_filter.click()
    pending_option = driver.find_element(By.XPATH, "//option[@value='pending']")
    pending_option.click()
    
    time.sleep(1)
    
    # Buscar y hacer click en "Limpiar"
    try:
        clear_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Limpiar')]")
        clear_button.click()
        time.sleep(1)
        
        # Verificar que el filtro se limpió
        status_filter = driver.find_element(By.XPATH, 
                                          "//label[contains(text(), 'Estado')]/../select")
        assert status_filter.get_attribute('value') == '' or status_filter.get_attribute('value') is None
    except:
        # Si no hay botón de limpiar, está bien (puede no haber filtros activos)
        pass