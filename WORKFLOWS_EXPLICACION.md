# 🔄 Flujo Completo CI/CD con GitHub Actions + Vercel

## 📋 ¿Qué son los Workflows?

Los workflows son archivos YAML en `.github/workflows/` que definen automáticamente qué hacer cuando hay cambios en el código.

```
Haces un push a GitHub
         ↓
GitHub Actions lee los workflows
         ↓
Ejecuta pruebas automáticamente
         ↓
Si todo está OK → Despliega a Vercel
```

---

## 🔄 FLUJO ACTUAL DE TU PROYECTO

### 1️⃣ **TRIGGER** (Qué causa la ejecución)

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

**Significa:**
- ✅ Se ejecuta cuando haces `git push` a `main` o `develop`
- ✅ Se ejecuta cuando abres un Pull Request a `main`
- ❌ NO se ejecuta en otras ramas

---

## 📊 WORKFLOW BACKEND (`backend-ci.yml`)

Se ejecuta cuando hay cambios en: `backend/**`, `api/**`

```
┌─────────────────────────────────────────────────────────┐
│ 1. CODE QUALITY (Black, Flake8, Pylint)                │
│    ✅ Si pasa → continúa                               │
│    ⚠️  Si falla → solo advertencia, continúa           │
└──────────────┬──────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────┐
│ 2. UNIT TESTS (80% coverage requerido)                 │
│    ✅ Si pasa → continúa                               │
│    ❌ Si falla → DETIENE EL PIPELINE                   │
└──────────────┬──────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────┐
│ 3. INTEGRATION TESTS                                    │
│    ✅ Si pasa → continúa                               │
│    ❌ Si falla → DETIENE EL PIPELINE                   │
└──────────────┬──────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────┐
│ 4. E2E TESTS (con Selenium + Frontend)                 │
│    ✅ Si pasa → continúa                               │
│    ⚠️  Si falla → solo advertencia                     │
└──────────────┬──────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────┐
│ 5. PERFORMANCE TESTS (benchmark)                        │
│    ✅ Si pasa → continúa                               │
│    ⚠️  Si falla → solo advertencia                     │
└──────────────┬──────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────────────┐
│ 6. DEPLOY A VERCEL (solo si rama=main AND push)        │
│    ✅ Despliega automáticamente                        │
│    ❌ Si tests fallaron en paso 2-3 → NO DESPLIEGA    │
└─────────────────────────────────────────────────────────┘
```

### Código del Deploy

```yaml
deploy-vercel:
  needs: [unit-tests, integration-tests]  # ← Solo si estos pasaron
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  
  steps:
  - Install Vercel CLI
  - Deploy to Vercel Production
```

**Explicación:**
- `needs: [unit-tests, integration-tests]` = Depende de que estos pasen
- `if: github.ref == 'refs/heads/main'` = Solo en rama `main`
- `github.event_name == 'push'` = Solo en pushes, no en PRs

---

## 📊 WORKFLOW FRONTEND (`frontend-ci.yml`)

Se ejecuta cuando hay cambios en: `frontend/**`

```
┌──────────────────────────────┐
│ 1. LINT (ESLint)             │
│    ✅ Si pasa → continúa     │
│    ⚠️  Si falla → advertencia│
└──────────┬───────────────────┘
           ↓
┌──────────────────────────────┐
│ 2. BUILD (npm run build)     │
│    ✅ Si pasa → continúa     │
│    ❌ Si falla → DETIENE     │
└──────────┬───────────────────┘
           ↓
┌──────────────────────────────┐
│ 3. DEPLOY A GITHUB PAGES     │
│    (Opcional, Vercel es     │
│     quien sirve el frontend) │
└──────────────────────────────┘
```

---

## 🚀 FLUJO COMPLETO: DE PUSH A VERCEL LIVE

### Escenario: Haces cambios en backend y frontend

```
1. Tu máquina:
   $ git add .
   $ git commit -m "Fix: tasks endpoint"
   $ git push origin main

2. GitHub recibe el push
   ↓
3. GitHub Actions inicia workflows:
   - backend-ci.yml (porque hay cambios en backend/)
   - frontend-ci.yml (porque hay cambios en frontend/)

4. Backend CI:
   Step 1: Code Quality (Black, Flake8) → ✅ OK
   Step 2: Unit Tests → ✅ PASAN (coverage 85%)
   Step 3: Integration Tests → ✅ PASAN
   Step 4: E2E Tests → ✅ PASAN
   Step 5: Performance Tests → ✅ OK
   Step 6: DEPLOY A VERCEL → Ejecuta
   
5. Frontend CI:
   Step 1: Lint (ESLint) → ⚠️ Warnings ignorados
   Step 2: Build → ✅ Build OK (250KB)
   Step 3: GitHub Pages → ✅ Deploy OK (innecesario)

6. Vercel recibe trigger de Deploy
   - Ejecuta: npm run build (frontend)
   - Instala requirements.txt (backend)
   - Compila todo
   - Despliega en https://tu-proyecto.vercel.app

7. GitHub Pages TAMBIÉN recibe el build
   - Extra, no necesario, pero OK

8. Tu proyecto está LIVE:
   ✅ https://tu-proyecto.vercel.app
   ✅ API funcionando
   ✅ Frontend funcionando
   ✅ Todos los tests pasados
   ✅ Logs disponibles en GitHub Actions
   ✅ Logs disponibles en Vercel Dashboard
```

---

## 📱 VISUALIZAR EN GITHUB

### Ver estado de workflows
```
Tu repo → Actions tab
       → Mostrar todos los runs
       → Click en un commit
       → Ver qué workflows se ejecutaron
       → Click en un workflow → ver logs detallados
```

### Ver si deployment fue exitoso
```
Vercel Dashboard → Tu proyecto → Deployments
                                → Ver logs de build
                                → Ver si está live
```

---

## ✅ REQUISITOS PARA QUE FUNCIONE

### 1. **Variables de Entorno en GitHub Secrets**
```
Necesitas agregar:
VERCEL_TOKEN         ← Para que GitHub Actions pueda deployar
VERCEL_ORG_ID        ← (Opcional)
VERCEL_PROJECT_ID    ← (Opcional)
```

**Cómo agregar:**
```
Tu repo en GitHub
  → Settings
  → Secrets and variables
  → Actions
  → New repository secret
  → VERCEL_TOKEN = [tu token de Vercel]
```

### 2. **Tests tienen que pasar**
Si el test de cobertura requiere 80% y tienes 79%, el deployment NO ocurre.

### 3. **vercel.json debe existir**
Sin esto, Vercel no sabe cómo buildear.

---

## 🔄 CASOS ESPECIALES

### Caso 1: Cambios solo en frontend
```
Push con cambios en frontend/
  → Frontend CI se ejecuta (lint, build)
  → Backend CI NO se ejecuta
  → Deploy a Vercel (frontend parte)
```

### Caso 2: Cambios solo en backend
```
Push con cambios en backend/
  → Backend CI se ejecuta (tests, quality)
  → Frontend CI NO se ejecuta
  → Deploy a Vercel (backend parte)
```

### Caso 3: Pull Request
```
Abres PR a main
  → Workflows se ejecutan
  → Tests corren
  → Pero NO despliega a Vercel
  → Muestran resultados en GitHub
  → Puedes ver si está OK antes de mergear
```

### Caso 4: Push a rama develop
```
Push a develop
  → Workflows se ejecutan
  → Tests corren
  → Pero NO despliega a Vercel
  → Solo corre en rama main
```

---

## 🧪 DEBUGGING: ¿Por qué no despliega?

### Checklist:

1. ¿Estoy en rama `main`?
   ```bash
   git branch
   ```
   Si dice `develop`, primero mergea a main

2. ¿Los tests pasaron?
   ```
   GitHub → Actions → tu commit
   Busca ✅ o ❌ en cada step
   ```

3. ¿Está el `vercel.json`?
   ```bash
   ls vercel.json
   ```

4. ¿Tiene el VERCEL_TOKEN?
   ```
   GitHub Settings → Secrets
   Debe mostrar VERCEL_TOKEN ✅
   ```

5. ¿El build de frontend está OK?
   ```
   GitHub Actions → Frontend CI → Build step
   Debe mostrar ✅
   ```

---

## 📊 ESTADO ACTUAL DE TU CONFIGURACIÓN

✅ **Workflows:** Bien configurados
✅ **Backend tests:** Todo OK
✅ **Frontend build:** Funciona
✅ **vercel.json:** Actualizado
⚠️  **PENDIENTE:** Agregar VERCEL_TOKEN a GitHub Secrets

**Próximo paso:**
```
1. Ir a Vercel, obtener token
2. GitHub Settings → Secrets → Add VERCEL_TOKEN
3. Hacer push a main
4. Ver cómo despliega automáticamente
```

