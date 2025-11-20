# 🚀 Guía Completa de Deployment en Vercel

## 📋 Pre-requisitos

- ✅ Cuenta en GitHub
- ✅ Cuenta en Vercel (gratis): https://vercel.com/signup
- ✅ Proyecto funcionando localmente
- ✅ Tests pasando

---

## 🔧 PASO 1: Preparar el Proyecto

### 1.1 Crear archivos necesarios

**Crear `api/index.py` en raíz:**

```python
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app
from mangum import Mangum

handler = Mangum(app, lifespan="off")
```

**Crear `requirements.txt` en raíz:**

```txt
fastapi==0.115.0
mangum==0.18.0
pydantic==2.9.2
```

**Crear `vercel.json` en raíz:**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "frontend/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Crear `.vercelignore`:**

```
__pycache__/
*.pyc
venv/
.pytest_cache/
htmlcov/
.coverage
node_modules/
backend/tests/
.git/
*.log
```

### 1.2 Ajustar Frontend para Producción

**frontend/.env.production:**

```env
VITE_API_URL=/api
```

**frontend/vite.config.js:**

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist'
  }
})
```

**frontend/package.json - agregar script:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "vercel-build": "npm run build"
  }
}
```

### 1.3 Ajustar Store para usar rutas relativas

**frontend/src/store/taskStore.js:**

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## 🌐 PASO 2: Deploy con Vercel (Opción A - UI)

### Método más fácil - Desde el Dashboard

1. **Ir a Vercel**: https://vercel.com/dashboard

2. **Importar Proyecto**:
   - Click en "Add New" → "Project"
   - Seleccionar tu repositorio de GitHub
   - Click en "Import"

3. **Configurar Build Settings**:
   ```
   Framework Preset: Other
   Build Command: (dejar vacío o "cd frontend && npm run build")
   Output Directory: frontend/dist
   Install Command: npm install
   ```

4. **Environment Variables**:
   - Agregar `PYTHON_VERSION` = `3.9`
   - Agregar `VITE_API_URL` = `/api`

5. **Deploy**:
   - Click en "Deploy"
   - Esperar 2-3 minutos
   - ¡Listo! 🎉

---

## 💻 PASO 3: Deploy con Vercel CLI (Opción B - Terminal)

### Para más control

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy preview (primero siempre)
vercel

# Seguir prompts:
# - Set up and deploy? Yes
# - Which scope? Tu usuario
# - Link to existing project? No
# - Project name? proyecto-caso-testigo-[apellido]
# - Directory? ./
# - Override settings? No

# 4. Ver preview
# Vercel te dará un URL: https://proyecto-xxx.vercel.app

# 5. Probar preview
curl https://tu-preview.vercel.app/api/health

# 6. Si funciona, deploy a producción
vercel --prod
```

---

## 🔐 PASO 4: Configurar Secrets para GitHub Actions

Si quieres deploy automático desde GitHub:

1. **Obtener token de Vercel**:
   - Ir a https://vercel.com/account/tokens
   - Crear nuevo token
   - Copiar el token

2. **Agregar a GitHub Secrets**:
   - Ir a tu repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `VERCEL_TOKEN`
   - Value: [tu token]
   - Save

3. **Obtener IDs de Vercel**:
   ```bash
   # En tu proyecto local
   vercel link
   
   # Esto crea .vercel/project.json con:
   # - projectId
   # - orgId
   ```

4. **Agregar más secrets**:
   - `VERCEL_ORG_ID`: del archivo .vercel/project.json
   - `VERCEL_PROJECT_ID`: del archivo .vercel/project.json

---

## ✅ PASO 5: Verificar Deployment

### Checklist de pruebas:

```bash
# URL base
curl https://tu-proyecto.vercel.app

# Health check
curl https://tu-proyecto.vercel.app/api/health

# Listar tareas
curl https://tu-proyecto.vercel.app/api/tasks

# Crear tarea
curl -X POST https://tu-proyecto.vercel.app/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test desde producción"}'

# Docs de API
# Abrir en navegador:
https://tu-proyecto.vercel.app/api/docs
```

### En el navegador:

1. ✅ Abrir `https://tu-proyecto.vercel.app`
2. ✅ Crear una tarea
3. ✅ Editar una tarea
4. ✅ Filtrar por estado
5. ✅ Eliminar una tarea
6. ✅ Verificar responsive en móvil

---

## 🐛 TROUBLESHOOTING

### Error: "Build failed"

**Problema**: Frontend no compila

**Solución**:
```bash
# Probar build localmente
cd frontend
npm run build

# Si falla, corregir errores y commit
```

### Error: "Module not found: app"

**Problema**: Backend no encuentra módulos

**Solución 1**: Verificar estructura
```
proyecto/
├── api/
│   └── index.py     ← Debe existir
├── backend/
│   └── app/
│       └── main.py  ← Debe existir
```

**Solución 2**: Verificar `requirements.txt` en raíz

### Error: "API returns 404"

**Problema**: Rutas no configuradas

**Solución**: Verificar `vercel.json` routes:
```json
{
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "handle": "filesystem" },
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

### Error: CORS en producción

**Problema**: Frontend no puede llamar al API

**Solución**: Actualizar CORS en `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tu-proyecto.vercel.app",
        "https://*.vercel.app"  # Para previews
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Logs no muestran errores

**Solución**: Ver logs en Vercel:
1. Dashboard → tu proyecto
2. Tab "Deployments"
3. Click en el deployment
4. Tab "Functions" → Ver logs de cada función

---

## 🎯 ALTERNATIVAS SI VERCEL NO FUNCIONA

### Opción A: Railway (Recomendado para Python 3.13)

```bash
# 1. Crear cuenta en railway.app
# 2. Install CLI
npm install -g @railway/cli

# 3. Login
railway login

# 4. Deploy backend
cd backend
railway init
railway up

# 5. Deploy frontend en Vercel apuntando a Railway
```

### Opción B: Render

1. Ir a render.com
2. "New Web Service"
3. Conectar GitHub repo
4. Build Command: `cd backend && pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Opción C: PythonAnywhere

1. Crear cuenta en pythonanywhere.com
2. Upload código
3. Configurar WSGI
4. Frontend separado en Netlify/Vercel

---

## 📊 MONITOREO POST-DEPLOYMENT

### Métricas en Vercel:

1. **Analytics**: Ver tráfico y performance
2. **Speed Insights**: Tiempo de carga
3. **Logs**: Errores en tiempo real

### Configurar alertas:

1. Vercel Dashboard → Settings → Notifications
2. Activar:
   - Deployment failed
   - Deployment succeeded
   - Performance issues

---

## 🔄 FLUJO DE TRABAJO CONTINUO

### Development → Staging → Production

```bash
# Branch develop → Preview deployment
git checkout develop
git push origin develop
# Vercel auto-deploys preview

# Test en preview
# https://proyecto-git-develop-usuario.vercel.app

# Si funciona → Merge a main
git checkout main
git merge develop
git push origin main
# Vercel auto-deploys production
```

---

## 📈 OPTIMIZACIONES POST-DEPLOYMENT

### 1. Performance
- Habilitar Edge Caching en Vercel
- Comprimir assets en build
- Lazy load componentes React

### 2. SEO
- Agregar meta tags
- Configurar og:image
- Crear sitemap

### 3. Security
- Habilitar HTTPS (automático en Vercel)
- Configurar Headers de seguridad
- Rate limiting en API

---

## ✅ CHECKLIST FINAL

- [ ] `vercel.json` configurado
- [ ] `api/index.py` existe y funciona
- [ ] `requirements.txt` en raíz
- [ ] `.vercelignore` creado
- [ ] Frontend build exitoso
- [ ] CORS configurado para producción
- [ ] Variables de entorno en Vercel
- [ ] Deployment exitoso
- [ ] Health check funciona
- [ ] Frontend conecta con API
- [ ] Tests E2E pasan en producción
- [ ] Dominio personalizado (opcional)
- [ ] SSL activo
- [ ] Logs monitoreados

---

## 🎓 RECURSOS ADICIONALES

- [Vercel Docs - Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI on Vercel](https://github.com/vercel/examples/tree/main/python/fastapi)
- [Mangum Documentation](https://mangum.io/)
- [Vite Build Options](https://vitejs.dev/config/build-options.html)

---

**¡Deployment exitoso!** 🚀

Tu proyecto estará disponible en:
- **URL principal**: `https://proyecto-caso-testigo-[apellido].vercel.app`
- **API**: `/api/*`
- **Docs**: `/api/docs`