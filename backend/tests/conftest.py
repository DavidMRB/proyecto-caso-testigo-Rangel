"""
Configuración global para pytest
Agrega el directorio backend al path de Python
"""
import sys
from pathlib import Path

# Agregar el directorio padre (backend) al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
