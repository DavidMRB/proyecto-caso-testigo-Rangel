# 📁 Estructura del Proyecto para Vercel

```
proyecto-caso-testigo-[apellido]/
│
├── api/                          # ← Vercel Serverless Functions
│   └── index.py                  # Handler principal
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── e2e/
│   │   └── performance/
│   │
│   └── requirements.txt          # Dependencias Python 3.13
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── store/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.production
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
│
├── vercel.json                   # ← Configuración Vercel
├── runtime.txt                   # Python version local
├── requirements.txt              # Dependencias para Vercel
├── .vercelignore
├── README.md
└── .gitignore
```

## 🚀 Pasos para Deploy en Vercel

### 1. Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2. Configurar Proyecto

**Crear `.vercelignore`:**
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.pytest_cache/
htmlcov/
.coverage
node_modules/
.DS_Store
```

**Crear `requirements.txt` en raíz:**
```
fastapi==0.115.0
mangum==0.18.0
pydantic==2.9.2
```

### 3. Configurar Frontend

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
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### 4. Deploy

**Desde la terminal:**
```bash
# Login a Vercel
vercel login

# Deploy a preview
vercel

# Deploy a producción
vercel --prod
```

**O conectar con GitHub:**
1. Ve a [vercel.com](https://vercel.com)
2. Import Git Repository
3. Conecta tu repo de GitHub
4. Vercel detectará automáticamente la configuración
5. Click en "Deploy"

### 5. Variables de Entorno en Vercel

En el dashboard de Vercel:
- Settings → Environment Variables
- Agregar:
  - `PYTHON_VERSION`: `3.9` (Vercel aún no soporta 3.13)
  - `VITE_API_URL`: `/api`

## ⚠️ Importante sobre Python 3.13

**Problema:** Vercel actualmente soporta hasta Python 3.9 en serverless functions.

**Soluciones:**

### Opción A: Usar Python 3.9 en Vercel (Recomendado)
- Desarrolla localmente con 3.13
- Deploy usa 3.9 automáticamente
- Las dependencias actualizadas funcionan en ambas versiones

### Opción B: Backend separado
Si necesitas 3.13 absolutamente:
1. Deploy backend en **Railway** o **Render** (soportan 3.13)
2. Deploy frontend en **Vercel**
3. Configurar CORS adecuadamente

### Opción C: Vercel con Docker (Beta)
Vercel ahora soporta Docker en beta, pero es más complejo.

## 🔄 Flujo de Trabajo

```bash
# Desarrollo local
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev

# Tests antes de deploy
pytest backend/tests/ -v
npm run build  # en frontend

# Deploy
vercel --prod
```

## 📊 URLs después del Deploy

Después de deployar, tendrás:

- **Production**: `https://tu-proyecto.vercel.app`
- **API**: `https://tu-proyecto.vercel.app/api/tasks`
- **Docs**: `https://tu-proyecto.vercel.app/api/docs`
- **Preview**: Una URL única por cada push

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Asegurar que requirements.txt está en raíz
cp backend/requirements.txt requirements.txt
```

### Error: "Build failed"
- Verificar que `api/index.py` existe
- Confirmar que `vercel.json` está bien formado
- Ver logs en Vercel dashboard

### Frontend no conecta con API
- Verificar `VITE_API_URL=/api` en producción
- Confirmar CORS en `main.py`
- Check Network tab en DevTools

## ✅ Checklist Pre-Deploy

- [ ] `vercel.json` configurado
- [ ] `api/index.py` creado
- [ ] `requirements.txt` en raíz
- [ ] `.vercelignore` creado
- [ ] Frontend build exitoso localmente
- [ ] Tests pasando
- [ ] CORS configurado para dominio Vercel
- [ ] Variables de entorno configuradas