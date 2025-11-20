
# 📦 Sistema de Gestión de Tareas Empresariales  
### **Proyecto Caso Testigo — Rangel**

Este repositorio contiene un sistema completo de **gestión de tareas empresariales**, desarrollado como proyecto caso testigo para demostrar:

- Buenas prácticas de **arquitectura backend y frontend**  
- Implementación profesional de **CI/CD con GitHub Actions**  
- Despliegue moderno usando **Render (backend)** y **Vercel (frontend)**  
- Integración total mediante API REST  
- Uso de herramientas de **testing, métricas y validación de calidad**  

El proyecto refleja un entorno realista de desarrollo, pruebas, automatización y despliegue continuo como se haría en un entorno profesional.

---

# 📘 1. Descripción General del Proyecto

El sistema permite administrar tareas empresariales mediante un frontend atractivo y un backend escalable.  
Su propósito es ser un **caso testigo** que evidencie capacidades técnicas en:

- Desarrollo **Full Stack**
- Pruebas automatizadas
- Arquitectura limpia
- CI/CD moderno
- Integración frontend-backend
- Buenas prácticas de programación

### ✔️ Funcionalidades principales

- Crear tareas  
- Listar todas las tareas  
- Filtrar por estado  
- Actualizar tareas  
- Eliminar tareas  
- Estados disponibles: *pending*, *in_progress*, *completed*  
- Comunicación mediante API REST JSON  
- UI rápida, moderna y responsive  

---

# 🏗️ 2. Arquitectura del Sistema

La arquitectura se divide en dos capas independientes, comunicadas por HTTP:

```
┌─────────────────────────┐         ┌─────────────────────────┐
│        FRONTEND          │  HTTP   │         BACKEND          │
│ React + Zustand + Vite   │◄──────►│ FastAPI + Python         │
└─────────────────────────┘         └─────────────────────────┘
           │                                   │
           ▼                                   ▼
  Estado global en navegador          Lógica de negocio / DB
```

---

## 🧩 Backend — FastAPI

El backend sigue un enfoque modular:

```
backend/
│── app/
│   │── main.py          → Inicialización del servidor y rutas
│   │── routers/         → Endpoints organizados
│   │── services/        → Lógica de negocio (TaskService)
│   │── repositories/    → Capa de persistencia
│   │── schemas/         → Modelos Pydantic v2
│   └── utils/           → Utilidades
```

Principales características:

- Arquitectura desacoplada
- Validación de datos con Pydantic v2
- Endpoints REST estructurados
- Manejo correcto de estados HTTP
- Inyección de dependencias

---

## 🎨 Frontend — React + Zustand + Vite

```
frontend/
│── src/
│   │── components/
│   │── store/        → Zustand global
│   │── hooks/
│   │── pages/
│   └── main.jsx
```

Características:

- Administración global con **Zustand**
- Arquitectura modular
- Renderización eficiente
- Tailwind para estilos consistentes
- Axios para comunicación con backend

---

# 🚀 4. CI/CD — GitHub Actions

El proyecto cuenta con pipelines automatizados para garantizar calidad y estabilidad.

### ✔️ Validación automática al hacer push

- Instalación de dependencias  
- Limpieza y preparación del entorno  
- Ejecución de pruebas backend  
- Linting de código  
- Validación de build del frontend  
- Generación automática del paquete para despliegue  

### ✔️ Beneficios

- Evita mezclar código roto en producción  
- Garantiza calidad uniforme  
- Automatiza repetitivos manuales  
- Prepara automáticamente los artefactos para deploy  

---

# ☁️ 5. Despliegue (Render + Vercel)

La aplicación se encuentra desplegada de forma separada, siguiendo buenas prácticas modernas.

---

## 🔵 Backend — Render

Render está configurado como **Web Service**, con:

- Build Command:  
  ```
  pip install -r backend/requirements.txt
  ```
- Start Command:  
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Health Check Endpoint:  
  ```
  /health
  ```

El servicio se reinicia automáticamente en cada push a `main`.

---

## 🟣 Frontend — Vercel

El frontend está desplegado en Vercel.  
URL pública de producción:

👉 **https://proyecto-caso-testigo-rangel-uyso.vercel.app/**

Variables de entorno:

```
VITE_API_URL=https://<backend-api>.onrender.com
```

Integración:

- Cada build toma automáticamente el código del repo  
- Se genera un artefacto optimizado  
- Vercel distribuye la app mediante CDN global  

---

# 🧪 6. Testing y Métricas de Calidad

El proyecto sigue una estrategia de validación progresiva.

## ✔️ Herramientas usadas

- **pytest** → pruebas unitarias e integración  
- **coverage.py** → reporte de cobertura  
- **requests** → testing de endpoints  
- **GitHub Actions** → ejecución automatizada  

## ✔️ Tipos de pruebas integradas

| Tipo | Objetivo |
|------|----------|
| Unitarias | Validar cada servicio individual |
| Integración | Probar endpoint + servicio + repositorio |
| Contratos | Validar esquemas Pydantic y respuestas |
| Smoke tests | Verificar que todo arranca correctamente |

## ✔️ Métricas sugeridas

- Tiempo de respuesta API: **20–60 ms**
- Cobertura esperada: **70–90%**
- Tiempo de ejecución total CI: **40–60 segundos**

---

# 📝 9. Licencia y Créditos

Proyecto desarrollado por:

👤 **David Mauricio Rangel Báez**  
GitHub: https://github.com/DavidMRB  

Licencia: **MIT License**  
Puedes usar y modificar libremente este proyecto con fines educativos o profesionales.

---

### ✅ Proyecto Caso Testigo completado con prácticas profesionales de desarrollo, testing y despliegue.
