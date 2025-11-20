"""
Handler para Vercel Serverless Functions
Expone la aplicación FastAPI como función serverless
"""
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app
from mangum import Mangum

# Handler para Vercel
handler = Mangum(app, lifespan="off")

# Para pruebas locales
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)