# GitHub Actions & Vercel Setup Guide

## 🔐 GitHub Secrets Requeridos

Para que los workflows de CI/CD funcionen correctamente, debes configurar los siguientes secrets en tu repositorio de GitHub:

### Backend (Python)
- No hay secrets obligatorios para el backend CI/CD

### Vercel Deployment
Necesitas configurar en **Settings > Secrets and variables > Actions**:

```
VERCEL_TOKEN         # Token de acceso personal de Vercel
VERCEL_ORG_ID        # ID de la organización en Vercel (opcional)
VERCEL_PROJECT_ID    # ID del proyecto en Vercel (opcional)
```

## 📋 Pasos para Configurar

### 1. Obtener VERCEL_TOKEN
```bash
# Desde https://vercel.com/account/tokens
# Crea un token nuevo con scope "Full Account"
```

### 2. Obtener VERCEL_ORG_ID y VERCEL_PROJECT_ID
```bash
# Desde la carpeta del proyecto
vercel env pull
# Esto crea un archivo .env.local con los valores
# O desde https://vercel.com/dashboard/[org-name]/[project-name]/settings
```

### 3. Agregar Secrets a GitHub
```bash
# Via GitHub CLI
gh secret set VERCEL_TOKEN --body "your-token"
gh secret set VERCEL_ORG_ID --body "your-org-id"
gh secret set VERCEL_PROJECT_ID --body "your-project-id"

# O manualmente en:
# https://github.com/[owner]/[repo]/settings/secrets/actions
```

## 🔄 Workflows Configurados

### Backend CI/CD (`.github/workflows/backend-ci.yml`)
Se ejecuta cuando hay cambios en:
- `backend/**`
- `api/**`
- `.github/workflows/backend-ci.yml`

**Pasos:**
1. ✅ Code Quality (Black, Flake8, Pylint)
2. ✅ Unit Tests + Coverage (80% requerido)
3. ✅ Integration Tests
4. ✅ E2E Tests (Selenium)
5. ✅ Performance Tests
6. ✅ Deploy a Vercel (solo en `main`)

### Frontend CI/CD (`.github/workflows/frontend-ci.yml`)
Se ejecuta cuando hay cambios en:
- `frontend/**`
- `.github/workflows/frontend-ci.yml`

**Pasos:**
1. ✅ ESLint + Formateo
2. ✅ Build Vite
3. ✅ Chequeo de tamaño de build
4. ✅ Deploy a GitHub Pages (opcional)

## 📦 Vercel Configuration

El archivo `vercel.json` está configurado para:
- **API Backend**: `api/index.py` → Python 3.13 con Mangum
- **Frontend**: `frontend/dist` → Build estático de Vite
- **Routes**: 
  - `/api/*` → Maneja las requests del backend
  - `/*` → Sirve archivos estáticos del frontend

### Variables de Entorno en Vercel
```
VITE_API_URL=/api    # URL relativa para producción
```

## 🚀 Deployment Automático

**Rama `main`:**
- ✅ Código pasa todos los tests
- ✅ Build exitoso
- ✅ Deploy automático a Vercel

**Rama `develop`:**
- ✅ Solo ejecuta tests
- ❌ No despliega automáticamente

## 🧪 Ejecutar Tests Localmente

```bash
# Backend
cd backend
pytest tests/unit/ -v                    # Unit tests
pytest tests/integration/ -v             # Integration tests
pytest tests/performance/ --benchmark-only  # Performance

# Frontend
cd frontend
npm run lint                             # ESLint
npm run build                            # Build

# Local development
# Terminal 1: Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

## 📊 Monitoreo

- **Codecov**: Coverage reports en cada PR
- **GitHub Artifacts**: Reportes de tests descargables
- **Vercel**: Dashboard en https://vercel.com/dashboard

## ⚠️ Troubleshooting

### Tests fallan localmente pero pasan en GitHub Actions
- Verifica la versión de Python: `python --version`
- Instala dependencias: `pip install -r backend/requirements.txt`
- Limpia caché: `pytest --cache-clear`

### Deploy a Vercel falla
- Verifica que los secrets estén configurados correctamente
- Revisa logs en: https://vercel.com/dashboard/[project]/deployments
- Verifica permisos en el token

### Frontend no se sirve correctamente
- Verifica que `vercel.json` tenga las rutas correctas
- Build local: `cd frontend && npm run build && npm run preview`

