# ⚡ INICIO RÁPIDO - Proyecto CI/CD

## 🎯 Para Python 3.13 + Vercel

### ⏱️ Setup en 15 minutos

---

## 1️⃣ CREAR REPOSITORIO (2 min)

```bash
# En GitHub
# Crear repo: proyecto-caso-testigo-[tu-apellido]
# ✓ Add README
# ✓ Add .gitignore (Python)

# Clonar
git clone https://github.com/tu-usuario/proyecto-caso-testigo-[apellido].git
cd proyecto-caso-testigo-[apellido]
```

---

## 2️⃣ ESTRUCTURA DEL PROYECTO (1 min)

```bash
# Crear carpetas
mkdir -p backend/app backend/tests/{unit,integration,e2e,performance}
mkdir -p frontend/src/{components,store}
mkdir -p api .github/workflows docs

# Estructura final:
# ├── api/
# │   └── index.py
# ├── backend/
# │   ├── app/
# │   └── tests/
# ├── frontend/
# │   └── src/
# ├── .github/workflows/
# ├── vercel.json
# └── requirements.txt
```

---

## 3️⃣ BACKEND (5 min)

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Crear requirements.txt
cat > requirements.txt << EOF
fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.9.2
pytest==8.3.3
pytest-cov==5.0.0
pytest-asyncio==0.24.0
pytest-benchmark==4.0.0
httpx==0.27.2
selenium==4.25.0
black==24.10.0
flake8==7.1.1
python-multipart==0.0.12
mangum==0.18.0
EOF

# Instalar
pip install -r requirements.txt

# Copiar código de main.py (del artifact anterior)
# backend/app/main.py

# Probar
uvicorn app.main:app --reload
# Abrir: http://localhost:8000/docs
```

---

## 4️⃣ FRONTEND (4 min)

```bash
cd frontend

# Crear proyecto Vite
npm create vite@latest . -- --template react
npm install

# Instalar dependencias
npm install zustand axios lucide-react date-fns
npm install -D tailwindcss postcss autoprefixer

# Configurar Tailwind
npx tailwindcss init -p

# tailwind.config.js
cat > tailwind.config.js << EOF
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: [],
}
EOF

# src/index.css
cat > src/index.css << EOF
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Copiar componentes (de artifacts anteriores)
# src/App.jsx
# src/store/taskStore.js
# src/components/*.jsx

# Probar
npm run dev
# Abrir: http://localhost:5173
```

---

## 5️⃣ CONFIGURAR VERCEL (3 min)

```bash
# En raíz del proyecto

# 1. requirements.txt (raíz)
cat > requirements.txt << EOF
fastapi==0.115.0
mangum==0.18.0
pydantic==2.9.2
EOF

# 2. api/index.py
cat > api/index.py << 'EOF'
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))
from app.main import app
from mangum import Mangum
handler = Mangum(app, lifespan="off")
EOF

# 3. vercel.json
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {"src": "api/index.py", "use": "@vercel/python"},
    {"src": "frontend/package.json", "use": "@vercel/static-build", "config": {"distDir": "frontend/dist"}}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"handle": "filesystem"},
    {"src": "/(.*)", "dest": "/index.html"}
  ]
}
EOF

# 4. .vercelignore
cat > .vercelignore << EOF
__pycache__/
*.pyc
venv/
.pytest_cache/
node_modules/
backend/tests/
EOF

# 5. frontend/.env.production
cd frontend
echo "VITE_API_URL=/api" > .env.production

# 6. frontend/package.json - agregar script
# "vercel-build": "npm run build"
```

---

## 6️⃣ TESTS (Ya incluidos en código)

```bash
cd backend

# Unitarios
pytest tests/unit/ -v --cov=app

# Integración
pytest tests/integration/ -v

# Performance
pytest tests/performance/ -v --benchmark-only

# E2E (requiere Chrome)
pytest tests/e2e/ -v

# Cobertura completa
pytest -v --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 7️⃣ DEPLOY

```bash
# Desde raíz del proyecto

# Commit todo
git add .
git commit -m "Initial complete implementation"
git push origin main

# Deploy en Vercel (Opción A - UI)
# 1. Ir a https://vercel.com/dashboard
# 2. New Project
# 3. Import tu repo de GitHub
# 4. Deploy

# O (Opción B - CLI)
npm install -g vercel
vercel login
vercel --prod

# ¡Listo! 🎉
# Tu app: https://proyecto-caso-testigo-[apellido].vercel.app
```

---

## ✅ VERIFICAR

```bash
# API
curl https://tu-proyecto.vercel.app/api/health

# Frontend
# Abrir en navegador: https://tu-proyecto.vercel.app
```

---

## 🎓 ORDEN RECOMENDADO DE IMPLEMENTACIÓN

### Semana 1
- [ ] Día 1: Repo + Backend básico
- [ ] Día 2: Tests unitarios (10+)
- [ ] Día 3: Tests integración (20+)
- [ ] Día 4: Frontend setup + componentes

### Semana 2
- [ ] Día 5-6: Completar componentes React (6+)
- [ ] Día 7: Tests E2E (10+)
- [ ] Día 8: Tests performance (5+)

### Semana 3
- [ ] Día 9: GitHub Actions workflows
- [ ] Día 10: Configurar Vercel
- [ ] Día 11: Deploy y pruebas
- [ ] Día 12: Documentación completa

### Semana 4
- [ ] Día 13: Video demostración
- [ ] Día 14: Entrega final

---

## 🐛 PROBLEMAS COMUNES

### "Module not found: app"
```bash
# Verificar que existe: backend/app/main.py
# Y que api/index.py tiene el path correcto
```

### "Build failed in frontend"
```bash
cd frontend
npm run build  # Ver errores
# Corregir y volver a intentar
```

### "CORS error"
```python
# En backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O tu dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Tests E2E fallan
```bash
# Instalar ChromeDriver
# Linux: sudo apt-get install chromium-chromedriver
# Mac: brew install chromedriver
# Windows: Descargar de chromedriver.chromium.org
```

---

## 📚 ARCHIVOS CLAVE

| Archivo | Propósito |
|---------|-----------|
| `backend/app/main.py` | API FastAPI |
| `backend/requirements.txt` | Deps Python |
| `api/index.py` | Handler Vercel |
| `requirements.txt` (raíz) | Deps para Vercel |
| `vercel.json` | Config deployment |
| `frontend/src/App.jsx` | App principal React |
| `frontend/src/store/taskStore.js` | State management |
| `.github/workflows/backend-ci.yml` | Pipeline CI/CD |

---

## 🎯 OBJETIVOS MÍNIMOS

- ✅ 5 endpoints CRUD funcionando
- ✅ 10+ tests unitarios (>80% coverage)
- ✅ 20+ tests integración
- ✅ 10+ tests E2E
- ✅ 5+ tests performance
- ✅ 6+ componentes React
- ✅ Pipeline CI/CD funcional
- ✅ 10+ builds exitosos
- ✅ Deploy en Vercel
- ✅ Video 10 minutos

---

## 🚀 SIGUIENTE PASO

**Comienza con el backend:**

```bash
# 1. Crea el repo
# 2. Copia backend/app/main.py del artifact
# 3. Instala dependencias
# 4. Ejecuta: uvicorn app.main:app --reload
# 5. Abre http://localhost:8000/docs
# 6. ¡Funciona! ✅
```

---

**¿Dudas?** Revisa los artifacts completos o la guía detallada en GUIA_DEPLOYMENT_VERCEL.md