# MediTrack - Sistema de Gestión de Ingresos Hospitalarios

**MediTrack** es un sistema integral de gestión de ingresos hospitalarios desarrollado con Streamlit, MongoDB y API de openFDA. Permite registrar pacientes, generar informes clínicos automáticos con IA y mantener un registro centralizado de todos los ingresos hospitalarios.

## 🎯 Características principales

✅ **Registro de pacientes** - Formulario completo con datos personales, clínicos y administrativos  
✅ **Generación automática de informes** - Informes clínicos generados por IA (Groq LLM)  
✅ **Integración openFDA** - Información farmacológica real desde la API de openFDA  
✅ **PDFs profesionales** - Informes con formato hospitalario real  
✅ **Búsqueda avanzada** - Filtrado por múltiples criterios y paginación  
✅ **Visualización de pacientes del día** - Consulta ingresos y altas por fecha  
✅ **Estadísticas** - Dashboard con análisis de datos  
✅ **Base de datos MongoDB** - Almacenamiento centralizado y escalable

## 📋 Requisitos previos

- Python 3.9+
- MongoDB (local o en la nube)
- Cuenta con API Key de Groq
- pip (gestor de paquetes Python)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <repositorio>
cd MediTrack
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/meditrack?retryWrites=true&w=majority
```

**Obtener API Key de Groq:**
1. Ir a https://console.groq.com
2. Crear una cuenta y generar una API key
3. Copiar la clave al archivo `.env`

**Configurar MongoDB:**
- Local: `mongodb://localhost:27017/meditrack`
- Atlas (nube): Obtener URI desde MongoDB Atlas

### 5. Cargar datos iniciales (opcional)

```bash
python scripts/cargar_dataset.py
```

## ▶️ Cómo usar

### Iniciar la aplicación

```bash
streamlit run view/app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📑 Secciones principales

### 1. **Nuevo Informe de Ingreso**
- Rellenar antecedentes del paciente
- Datos personales (nombre, edad, género, grupo sanguíneo, etc.)
- Datos clínicos (diagnóstico, medicación, dosis, tipo de ingreso)
- Fechas y horas precisas (ingreso y alta)
- Comentarios del médico
- Consulta automática a openFDA por medicación
- Generación de informe PDF profesional con análisis farmacológico por IA

**Campos del formulario:**
- Antecedentes / Motivo de consulta
- Nombre, edad, género, grupo sanguíneo
- Aseguradora, importe facturado, número de habitación
- Diagnóstico, tipo de ingreso, medicación, dosis
- Resultado de pruebas, médico responsable, hospital
- Fechas y horas de ingreso y alta

### 2. **Buscar y Filtrar Pacientes**
- Búsqueda por nombre, médico, hospital, diagnóstico
- Filtrado por género, grupo sanguíneo, tipo de ingreso
- Rango de fechas de ingreso
- Paginación de 20 pacientes por página
- Generar informes PDF desde búsqueda
- Descarga de PDFs profesionales

### 3. **Informes Guardados**
- Visor de todos los PDFs generados
- Búsqueda por nombre de paciente y fecha
- Paginación de 10 informes por página
- Descarga rápida de cualquier informe

### 4. **Estadísticas**
- Dashboard con análisis de datos hospitalarios
- Gráficos y visualizaciones

### 5. **Pacientes del Día**
- Consultar ingresos de una fecha específica
- Consultar altas de una fecha específica
- Generar informes individuales por paciente

## 📁 Estructura del proyecto

```
MediTrack/
├── view/
│   ├── app.py                      # Aplicación principal de Streamlit
│   └── sections/
│       ├── nuevo_informe.py        # Registro de nuevos pacientes
│       ├── buscar.py               # Búsqueda y filtrado
│       ├── informes_guardados.py   # Visor de PDFs
│       ├── estadisticas.py         # Dashboard
│       └── pacientes_dia.py        # Pacientes por fecha
├── scripts/
│   ├── db.py                       # Conexión a MongoDB
│   ├── generar_informe.py          # Generación de informes con IA
│   ├── generar_pdf.py              # Formateo profesional de PDFs
│   ├── openfda.py                  # Integración con API openFDA
│   └── cargar_dataset.py           # Script para cargar datos iniciales
├── informes/                       # Carpeta de PDFs generados (gitignored)
├── data/
│   └── healthcare_dataset.csv      # Dataset de ejemplo
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos a ignorar en Git
└── README.md                       # Este archivo
```

## 🔌 API y Datos

### openFDA
- Consulta información farmacológica en tiempo real
- Extrae: nombre comercial, genérico, indicaciones, advertencias, reacciones adversas, dosificación
- Traducción automática de medicamentos al inglés para búsqueda

### MongoDB
- Almacenamiento de registros de pacientes
- Campos indexados para búsqueda rápida
- Historial completo de ingresos y altas

### Groq LLM
- Generación de informes clínicos profesionales
- Análisis farmacológico personalizado
- Modelo: `llama-3.3-70b-versatile`

## 🔄 Flujo de trabajo típico

1. **Registrar nuevo paciente** → Nuevo Informe de Ingreso
2. **Sistema consulta openFDA** → Obtiene datos del medicamento
3. **IA genera informe** → Análisis personalizado basado en FDA
4. **PDF profesional** → Informe descargable con estructura hospitalaria
5. **Buscar pacientes** → Consultas avanzadas y filtrado
6. **Ver pacientes del día** → Ingresos y altas por fecha
7. **Descargar informes** → Desde Informes Guardados

## 🛠️ Configuración de desarrollo

### Base de datos local

```bash
# Instalar MongoDB
# macOS
brew tap mongodb/brew
brew install mongodb-community

# Iniciar servicio
brew services start mongodb-community

# Verificar conexión
mongosh
```

### Variables de entorno para desarrollo

```env
# .env.local
GROQ_API_KEY=sk_test_...
MONGODB_URI=mongodb://localhost:27017/meditrack
```

## 🔧 Troubleshooting

### Error de conexión a MongoDB
```
Verificar que MongoDB esté corriendo
Comprobar MONGODB_URI en .env
```

### Error de API Key de Groq
```
Verificar que GROQ_API_KEY esté correctamente configurada
Ir a https://console.groq.com para regenerar si es necesario
```

### openFDA no encuentra medicamentos
```
El medicamento puede no estar en la base de datos de FDA
Se genera informe con información genérica
```

## 🔒 Seguridad

- `.env` no se sube a Git (protege credenciales)
- `informes/` no se sube a Git (documentos confidenciales)
- Validación de datos en entrada
- Sanitización de nombres de archivo

## 🚦 Mejoras futuras

- 📊 Dashboard estadístico más completo
- 🔐 Sistema de autenticación de usuarios
- 📧 Exportación de informes por email
- 🗂️ Archivo histórico con búsqueda avanzada
- 🔔 Alertas automáticas
- 📱 Versión móvil

## 🛠️ Tecnologías utilizadas

| Tecnología | Propósito |
|-----------|----------|
| **Streamlit** | Framework web frontend |
| **MongoDB** | Base de datos NoSQL |
| **Groq API** | IA para generación de informes |
| **ReportLab** | Generación de PDFs profesionales |
| **openFDA API** | Información farmacológica en tiempo real |
| **Python 3.9+** | Lenguaje de programación |

## 👥 Autores

- Anas El Ouahabi
- Ahmed Berday
- Reparto equitativo

## 📚 Curso

Bases de Datos Avanzadas — 2025/2026

