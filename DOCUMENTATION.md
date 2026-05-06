# Documentación Técnica - MediTrack

## Tabla de contenidos

1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Base de Datos](#base-de-datos)
5. [Backend](#backend)
6. [Frontend](#frontend)
7. [Integraciones Externas](#integraciones-externas)
8. [Flujo de Datos](#flujo-de-datos)
9. [Componentes Principales](#componentes-principales)
10. [Decisiones de Diseño](#decisiones-de-diseño)

---

## Visión General

**MediTrack** es una aplicación web para la gestión integral de ingresos hospitalarios. Utiliza una arquitectura moderna basada en:

- **Frontend**: Streamlit (interfaz web interactiva)
- **Backend**: Python con Streamlit como servidor
- **Base de Datos**: MongoDB (base de datos NoSQL)
- **IA**: Groq API (generación de informes)
- **APIs Externas**: openFDA (datos farmacológicos)

### Objetivos principales

1. Automatizar el registro de pacientes hospitalarios
2. Generar informes clínicos profesionales con IA
3. Integrar datos reales de medicamentos (openFDA)
4. Proporcionar búsqueda avanzada y paginación
5. Generar PDFs profesionales con formato hospitalario

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  App.py (Main)                                       │   │
│  │  - Gestión de navegación                             │   │
│  │  - Session state                                     │   │
│  │  - Sidebar con menú                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Sections (Módulos de funcionalidad)                 │   │
│  │  ├─ nuevo_informe.py (Registro)                     │   │
│  │  ├─ buscar.py (Búsqueda)                            │   │
│  │  ├─ informes_guardados.py (Visor)                   │   │
│  │  ├─ pacientes_dia.py (Filtro por fecha)             │   │
│  │  └─ estadisticas.py (Dashboard)                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Scripts)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  generar_informe.py                                  │   │
│  │  - Genera texto de informe con IA (Groq)            │   │
│  │  - Incorpora datos de FDA                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  generar_pdf.py                                      │   │
│  │  - Formatea informe en PDF profesional               │   │
│  │  - Llama a generar_informe internamente              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  openfda.py                                          │   │
│  │  - Traduce medicamentos al inglés con IA             │   │
│  │  - Consulta API de openFDA                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  db.py                                               │   │
│  │  - Conexión a MongoDB                                │   │
│  │  - Gestión de colecciones                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  DATOS Y SERVICIOS                           │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    MongoDB       │  │  Groq API    │  │  openFDA API │  │
│  │  - Pacientes     │  │  - IA LLM    │  │  - Fármacos  │  │
│  │  - Índices       │  │  - Informes  │  │  - Info      │  │
│  └──────────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Tecnologías Utilizadas

### Frontend

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Streamlit** | 1.28.0+ | Framework web interactivo |
| **Python** | 3.9+ | Lenguaje principal |

**Por qué Streamlit:**
- Desarrollo rápido de aplicaciones web
- No requiere HTML/CSS/JavaScript
- Session state para manejo de estado
- Widgets interactivos built-in
- Perfect para MVP y prototipos
- Excelente para ciencia de datos

### Backend

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.9+ | Lógica de aplicación |
| **python-dotenv** | 0.21.0+ | Gestión de variables de entorno |
| **requests** | 2.31.0+ | Llamadas HTTP a APIs |

### Base de Datos

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **MongoDB** | 5.0+ | Base de datos NoSQL |
| **pymongo** | 4.5.0+ | Driver Python para MongoDB |

**Por qué MongoDB:**
- Esquema flexible (documentos BSON)
- Escalabilidad horizontal
- Consultas ricas con agregación
- Ideal para datos heterogéneos
- Indexación automática
- Atlas para cloud hosting

### Generación de PDFs

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **ReportLab** | 4.0.0+ | Generación programática de PDFs |

**Por qué ReportLab:**
- Generación de PDFs sin dependencias externas
- Control total sobre layout y estilos
- Tablas, imágenes, textos formateados
- Numeración de páginas
- Perfecto para informes profesionales

### APIs Externas

| Servicio | Propósito | Autenticación |
|----------|----------|---------------|
| **Groq API** | IA/LLM para generar informes | API Key |
| **openFDA API** | Información farmacológica | Pública (sin key) |

---

## Base de Datos

### Esquema MongoDB

#### Colección: `pacientes`

```json
{
  "_id": ObjectId,
  "name": String,
  "age": Integer,
  "gender": String,
  "blood_type": String,
  "medical_condition": String,
  "date_of_admission": DateTime,
  "discharge_date": DateTime,
  "stay_days": Integer,
  "doctor": String,
  "hospital": String,
  "insurance_provider": String,
  "billing_amount": Float,
  "room_number": Integer,
  "admission_type": String,
  "medication": String,
  "dosage": String,
  "test_results": String,
  "antecedentes": String (nullable),
  "comentarios": String (nullable),
  "fda_info": {
    "brand_name": String,
    "generic_name": String,
    "indications": String,
    "warnings": String,
    "adverse_reactions": String,
    "dosage": String
  }
}
```

### Índices

```javascript
db.pacientes.createIndex({ "name": 1 })
db.pacientes.createIndex({ "doctor": 1 })
db.pacientes.createIndex({ "hospital": 1 })
db.pacientes.createIndex({ "medical_condition": 1 })
db.pacientes.createIndex({ "date_of_admission": 1 })
db.pacientes.createIndex({ "gender": 1 })
db.pacientes.createIndex({ "blood_type": 1 })
```

### Conexión

```python
# db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client["meditrack"]
    return db["pacientes"]
```

---

## Backend

### Módulo: `generar_informe.py`

**Responsabilidad:** Generar texto de informe clínico con IA

**Flujo:**
1. Recibe documento del paciente
2. Extrae información de FDA
3. Construye prompt detallado
4. Llama a Groq API
5. Retorna informe en texto

**Prompt principales:**
- Especialista en farmacología
- Análisis detallado de medicamentos
- Consideración de perfil del paciente
- Estructura de 6 secciones

```python
def generar_informe_paciente(doc):
    fda = doc.get("fda_info") or {}
    prompt = f"""
    Eres un médico especialista en farmacología...
    DATOS DEL PACIENTE:
    - Nombre: {doc.get('name')}
    - Edad: {doc.get('age')} años
    ...
    """
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    return respuesta.choices[0].message.content
```

### Módulo: `generar_pdf.py`

**Responsabilidad:** Convertir informe a PDF profesional

**Características:**
- Encabezado con logo
- Tablas con bordes
- Numeración automática de páginas
- Colores corporativos (azul #1f77b4)
- Secciones organizadas

**Clase: `NumeredCanvas`**
- Extiende canvas.Canvas de ReportLab
- Añade numeración automática de páginas

```python
class NumeredCanvas(canvas.Canvas):
    def showPage(self):
        self._add_page_number()
        canvas.Canvas.showPage(self)

    def _add_page_number(self):
        self.setFont("Helvetica", 9)
        self.drawString(19.5 * cm, 1 * cm, 
                       f"Página {self.getPageNumber()}")
```

### Módulo: `openfda.py`

**Responsabilidad:** Integración con API de openFDA

**Flujo:**
1. Traduce medicamento al inglés (con IA)
2. Busca en openFDA por nombre comercial
3. Si no encuentra, busca por nombre genérico
4. Extrae información relevante

```python
def consultar_openfda(medicamento):
    nombre_en = traducir_medicamento(medicamento)
    url = f"https://api.fda.gov/drug/label.json?search=..."
    r = requests.get(url)
    # Procesar respuesta y retornar info
    return {
        "brand_name": ...,
        "generic_name": ...,
        "indications": ...,
        "warnings": ...,
        "adverse_reactions": ...,
        "dosage": ...
    }
```

### Módulo: `db.py`

**Responsabilidad:** Conexión y gestión de MongoDB

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_collection():
    """Retorna colección de pacientes desde MongoDB"""
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["meditrack"]
    return db["pacientes"]
```

---

## Frontend

### Estructura Streamlit

```
view/
├── app.py (Main)
│   ├── set_page_config()
│   ├── Barra lateral (sidebar)
│   └── Ruteador de secciones
└── sections/
    ├── nuevo_informe.py
    ├── buscar.py
    ├── informes_guardados.py
    ├── pacientes_dia.py
    └── estadisticas.py
```

### App.py (Main)

**Responsabilidades:**
- Configuración de página
- Estilos CSS personalizados
- Sidebar con navegación
- Ruteador de secciones

```python
st.set_page_config(
    page_title="MediTrack",
    page_icon="🏥",
    layout="wide"
)

# CSS personalizado
st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-title">MediTrack</p>', 
               unsafe_allow_html=True)
    seccion = st.radio("Navegación", [
        "Nuevo Informe",
        "Buscar y Filtrar",
        "Informes Guardados",
        "Estadísticas",
        "Pacientes del Día"
    ])
```

### nuevo_informe.py

**Flujo:**
1. Formulario con st.form()
2. Validación de campos requeridos
3. Consulta openFDA
4. Inserta en MongoDB
5. Genera informe con IA
6. Genera PDF profesional
7. Ofrece descarga

**Session State:** No requiere (formulario es stateless)

### buscar.py

**Flujo:**
1. Filtros en expander
2. Botón "Buscar"
3. Construye query MongoDB
4. Aplica paginación (20 items/página)
5. Almacena en session_state
6. Navega con botones anterior/siguiente

**Session State:**
```python
st.session_state.pagina_actual = 0
st.session_state.query_almacenada = None
st.session_state.total_resultados = 0
```

### informes_guardados.py

**Flujo:**
1. Lee carpeta `informes/`
2. Aplica filtros locales
3. Ordena por fecha descendente
4. Paginación (10 items/página)
5. Descarga directa

### pacientes_dia.py

**Flujo:**
1. Selecciona fecha
2. Busca por `date_of_admission` o `discharge_date`
3. Muestra en expanders
4. Botón para generar informe individual

### estadisticas.py

**Estado:** En desarrollo

---

## Integraciones Externas

### Groq API

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Modelo usado:** `llama-3.3-70b-versatile`

**Parámetros:**
```python
{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 1500,
    "temperature": 0.3  # Bajo para respuestas consistentes
}
```

**Inicialización:**
```python
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```

**Casos de uso:**

**1. Generación de Informes Clínicos**
```python
def generar_informe_paciente(doc):
    """
    Genera informe clínico detallado basado en datos del paciente
    
    Args:
        doc: Documento de MongoDB con datos del paciente
        
    Returns:
        str: Informe en formato texto
    """
    fda = doc.get("fda_info") or {}
    
    prompt = f"""
    Eres un médico especialista en farmacología redactando un informe clínico formal en español.
    
    DATOS DEL PACIENTE:
    - Nombre: {doc.get('name')}
    - Edad: {doc.get('age')} años
    - Género: {doc.get('gender')}
    - Grupo sanguíneo: {doc.get('blood_type')}
    - Diagnóstico: {doc.get('medical_condition')}
    - Medicación: {doc.get('medication')}
    - Dosificación: {doc.get('dosage')}
    
    INFORMACIÓN FARMACOLÓGICA (openFDA):
    - Indicaciones: {fda.get('indications', 'No disponible')}
    - Advertencias: {fda.get('warnings', 'No disponible')}
    - Reacciones adversas: {fda.get('adverse_reactions', 'No disponible')}
    
    Genera un informe estructurado con:
    1. Datos del paciente
    2. Resumen del ingreso
    3. Análisis farmacológico
    4. Indicaciones vs diagnóstico
    5. Recomendaciones de monitoreo
    6. Conclusiones
    """
    
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    
    return respuesta.choices[0].message.content
```

**2. Traducción de Medicamentos**
```python
def traducir_medicamento(nombre):
    """
    Traduce nombre de medicamento al inglés para búsqueda en openFDA
    
    Args:
        nombre: Nombre del medicamento en español
        
    Returns:
        str: Nombre del medicamento en inglés
    """
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Traduce al inglés: '{nombre}'. "
                      f"Responde SOLO con la traducción, sin puntos ni explicaciones."
        }],
        max_tokens=20,
        temperature=0  # Determinista
    )
    
    return respuesta.choices[0].message.content.strip()
```

**Manejo de Errores:**
```python
try:
    informe = generar_informe_paciente(doc)
except Exception as e:
    st.error(f"Error generando informe: {str(e)}")
    st.info("Verifica que GROQ_API_KEY está configurado en .env")
```

**Limites y Cuotas:**
- Rate limit: 300 requests/minuto
- Contexto máximo: 8k tokens
- Respuesta máxima: 4k tokens

### openFDA API

**Endpoint:** `https://api.fda.gov/drug/label.json`

**Características:**
- Pública (sin autenticación)
- Rate limit: 240 requests/minuto
- Datos verificados por FDA
- Información completa de medicamentos

**Tipos de búsqueda:**

```python
import requests

# 1. Por nombre comercial
url = "https://api.fda.gov/drug/label.json"
params = {
    "search": "openfda.brand_name:Ibuprofen",
    "limit": 1
}
response = requests.get(url, params=params)

# 2. Por nombre genérico
params = {
    "search": "openfda.generic_name:Ibuprofen",
    "limit": 1
}
response = requests.get(url, params=params)
```

**Estructura de Respuesta:**
```json
{
  "results": [
    {
      "openfda": {
        "brand_name": ["Ibuprofen", "Advil"],
        "generic_name": ["Ibuprofen"],
        "manufacturer_name": ["Company Ltd"]
      },
      "indications_and_usage": [
        "For temporary relief of minor..."
      ],
      "warnings": [
        "Do not use if you have..."
      ],
      "adverse_reactions": [
        "Common: Nausea, heartburn..."
      ],
      "dosage_and_administration": [
        "Take 1 tablet every 4-6 hours..."
      ]
    }
  ]
}
```

**Implementación en MediTrack:**

```python
def consultar_openfda(medicamento):
    """
    Consulta openFDA para obtener información farmacológica
    
    Args:
        medicamento: Nombre del medicamento (se traduce automáticamente)
        
    Returns:
        dict: Información de FDA o None si no encuentra
    """
    # Traducir medicamento
    nombre_en = traducir_medicamento(medicamento)
    
    # Buscar por nombre comercial
    url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.brand_name:{nombre_en}",
        "limit": 1
    }
    response = requests.get(url, params=params)
    
    # Si no encuentra, buscar por nombre genérico
    if response.status_code != 200:
        params["search"] = f"openfda.generic_name:{nombre_en}"
        response = requests.get(url, params=params)
    
    # Si aún no encuentra, retornar None
    if response.status_code != 200:
        return None
    
    try:
        data = response.json()
        resultado = data.get("results", [{}])[0]
        
        return {
            "brand_name": resultado.get("openfda", {}).get("brand_name", [None])[0],
            "generic_name": resultado.get("openfda", {}).get("generic_name", [None])[0],
            "indications": resultado.get("indications_and_usage", [None])[0],
            "warnings": resultado.get("warnings", [None])[0],
            "adverse_reactions": resultado.get("adverse_reactions", [None])[0],
            "dosage": resultado.get("dosage_and_administration", [None])[0]
        }
    except (KeyError, IndexError):
        return None
```

**Integración con MongoDB:**
```python
# Obtener info de FDA
fda_data = consultar_openfda("Ibuprofen")

# Guardar en documento
document["fda_info"] = fda_data

# Insertar en MongoDB
col_db.insert_one(document)
```

**Ejemplos de Búsquedas:**

| Medicamento | Búsqueda | Resultado |
|------------|----------|----------|
| Ibuprofeno | Ibuprofen | ✅ Encontrado |
| Paracetamol | Paracetamol/Acetaminophen | ✅ Encontrado |
| Amoxicilina | Amoxicillin | ✅ Encontrado |
| Ácido acetilsalicílico | Acetylsalicylic acid/Aspirin | ✅ Encontrado |

**Manejo de Errores:**
```python
try:
    fda_data = consultar_openfda(medicamento)
    if fda_data:
        st.success("Información de FDA obtenida")
    else:
        st.warning("Medicamento no encontrado en FDA")
except Exception as e:
    st.error(f"Error consultando FDA: {str(e)}")
```

### Integración Completa: Flujo de Datos

```
┌─────────────────────────┐
│  Usuario ingresa dato   │
│  (Medicación: español)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Traducir con Groq      │
│  Español → Inglés       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Consultar openFDA      │
│  Buscar medicamento     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Extraer información    │
│  Indications, Warnings  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Guardar en MongoDB     │
│  doc["fda_info"] = {...}│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Generar Informe IA     │
│  (usa datos de FDA)     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Generar PDF            │
│  Profesional            │
└─────────────────────────┘
```

### Manejo de Errores en APIs

```python
from requests.exceptions import RequestException, Timeout, ConnectionError

def consultar_openfda_seguro(medicamento):
    """Version con manejo robusto de errores"""
    try:
        # Traducir
        nombre_en = traducir_medicamento(medicamento)
        if not nombre_en:
            return None
        
        # Consultar con timeout
        url = "https://api.fda.gov/drug/label.json"
        response = requests.get(
            url,
            params={"search": f"openfda.brand_name:{nombre_en}"},
            timeout=5
        )
        
        response.raise_for_status()  # Lanza excepción si 4xx/5xx
        return response.json()
        
    except Timeout:
        st.warning("Timeout: FDA API responde lentamente")
        return None
    except ConnectionError:
        st.error("Error: No hay conexión a internet")
        return None
    except RequestException as e:
        st.error(f"Error HTTP: {e}")
        return None
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return None
```

---

## Flujo de Datos

### Flujo 1: Registrar Nuevo Paciente

```
Usuario rellena formulario
         ↓
Validación de campos (nombre, médico, hospital)
         ↓
Calcula días de estancia
         ↓
Consulta openFDA (medicación)
         ↓
Inserta documento en MongoDB
         ↓
Genera informe con IA (Groq)
         ↓
Genera PDF profesional
         ↓
Oferece descarga
         ↓
Muestra resumen
```

### Flujo 2: Buscar Paciente

```
Usuario aplica filtros (nombre, fecha, etc.)
         ↓
Construye query MongoDB
         ↓
count_documents() para total
         ↓
find().skip().limit() para paginación
         ↓
Muestra en expanders
         ↓
Usuario selecciona "Generar informe"
         ↓
(Igual que Flujo 1 desde paso 5)
```

### Flujo 3: Ver Informes

```
Lee carpeta /informes/
         ↓
Aplica filtros (nombre, fecha)
         ↓
Paginación (10 items)
         ↓
Ofrece descarga
```

---

## Componentes Principales

### 1. Formulario de Registro

**Componentes Streamlit:**
```python
# Texto
st.text_input("Nombre completo")
st.text_area("Antecedentes / Motivo de consulta")

# Números
st.number_input("Edad", min_value=0, max_value=120)
st.number_input("Importe facturado", min_value=0.0)

# Selects
st.selectbox("Género", ["Male", "Female"])
st.selectbox("Tipo de admisión", ["Urgent", "Elective", "Emergency"])

# Dates y Times
st.date_input("Fecha de ingreso")
st.time_input("Hora de entrada")

# Form submit
st.form_submit_button("Guardar y generar informe")
```

### 2. Generador de PDF

**Componentes ReportLab:**
```python
SimpleDocTemplate()      # Documento PDF
Table()                  # Tablas con datos
TableStyle()             # Estilos de tablas
Paragraph()              # Texto formateado
Spacer()                 # Espacios
```

**Colores corporativos:**
- Azul primario: `#1f77b4`
- Fondo ligero: `#f0f5fa`
- Gris: `#e0e0e0`, `#999999`

### 3. Búsqueda Avanzada

**Operadores MongoDB:**
```python
{"$regex": nombre, "$options": "i"}    # Búsqueda case-insensitive
{"$gte": fecha1, "$lte": fecha2}       # Rango de fechas
```

**Paginación:**
```python
skip = (pagina - 1) * items_por_pagina
limit = items_por_pagina
find().skip(skip).limit(limit)
```

---

## Decisiones de Diseño

### 1. **Por qué Streamlit en lugar de Flask/Django**
- ✅ Desarrollo más rápido
- ✅ Menos boilerplate
- ✅ Session state built-in
- ✅ Perfecto para MVP
- ✅ Ideal para aplicaciones data-driven

### 2. **Por qué MongoDB en lugar de SQL**
- ✅ Esquema flexible (pacientes con distintos campos)
- ✅ Documentos anidados (fda_info)
- ✅ Escalabilidad horizontal
- ✅ Atlas para hosting cloud

### 3. **Por qué Groq en lugar de otros LLMs**
- ✅ API rápida (LPU inference)
- ✅ Gratuita con límites generosos
- ✅ Excelente relación precio/rendimiento
- ✅ Modelo 70B potente

### 4. **Por qué openFDA**
- ✅ Datos reales y verificados
- ✅ API pública sin autenticación
- ✅ Información completa de medicamentos
- ✅ Integración directa

### 5. **Por qué ReportLab para PDFs**
- ✅ Control total sobre layout
- ✅ Sin dependencias externas
- ✅ Generación programática
- ✅ Tablas y formatos complejos

### 6. **Paginación de 20 items en búsqueda**
- ✅ Balance entre rendimiento y UX
- ✅ No sobrecarga la UI
- ✅ Búsquedas ágiles en BD

### 7. **Session State para navegación**
- ✅ Mantiene filtros al cambiar de página
- ✅ No hay recargas innecesarias
- ✅ UX fluida y responsiva

### 8. **Temperatura baja en prompts (0.3)**
- ✅ Respuestas consistentes
- ✅ Información determinista
- ✅ Ideal para informes clínicos

---

## Seguridad

### Variables de Entorno

```env
# .env
GROQ_API_KEY=sk_xxx...
MONGODB_URI=mongodb+srv://...
```

**Protección:**
- Archivo `.env` en `.gitignore`
- Carga con `python-dotenv`
- Nunca exponidas en código

### Validación de Datos

```python
if not name or not doctor or not hospital:
    st.error("Por favor rellena campos requeridos")
    return

if discharge_date < date_of_admission:
    st.error("La fecha de alta no puede ser anterior")
    return
```

### Sanitización de Nombres

```python
nombre_archivo = f"informes/{name.replace(' ', '_')}_{fecha}.pdf"
# Previene inyección de paths
```

---

## Performance

### Optimizaciones Implementadas

1. **Índices en MongoDB**
   - Búsquedas O(log n) en lugar de O(n)

2. **Paginación**
   - Solo carga datos necesarios
   - No descarga 55k documentos de una vez

3. **Session State**
   - Evita consultas repetidas
   - Mantiene filtros en memoria

4. **Lazy loading de sections**
   - Import dinámico de módulos

### Complejidad de Operaciones

| Operación | Complejidad | Tiempo estimado |
|-----------|------------|-----------------|
| Insertar paciente | O(1) | < 100ms |
| Buscar con filtros | O(log n) | < 50ms |
| Generar informe IA | O(m) | ~2-5s |
| Generar PDF | O(1) | ~500ms |
| Consultar openFDA | O(1) | ~500ms |

---

## Testing

### Casos de Prueba (Manual)

```
1. Registro de paciente
   ✅ Rellenar formulario correctamente
   ✅ Validar campos requeridos
   ✅ Verificar en MongoDB
   ✅ Descargar PDF

2. Búsqueda
   ✅ Filtrar por nombre
   ✅ Filtrar por rango de fechas
   ✅ Paginación
   ✅ Generar informe desde búsqueda

3. Informes Guardados
   ✅ Listar archivos
   ✅ Filtrar por fecha
   ✅ Descargar
```

---

## Deployment

### Opciones

1. **Streamlit Cloud**
   - Gratis para proyectos públicos
   - Deploy desde GitHub
   - Auto-redeploy

2. **Heroku**
   - Requiere Procfile
   - Paid tier para siempre activo

3. **Docker**
   ```dockerfile
   FROM python:3.9
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["streamlit", "run", "view/app.py"]
   ```

---

## Roadmap Futuro

### Fase 2
- [ ] Autenticación de usuarios
- [ ] Roles y permisos
- [ ] Audit logs

### Fase 3
- [ ] Dashboard estadístico completo
- [ ] Exportación a Excel
- [ ] Notificaciones por email

### Fase 4
- [ ] Versión móvil
- [ ] Integración con más APIs médicas
- [ ] Análisis predictivo

---

## Referencias

- [Streamlit Docs](https://docs.streamlit.io/)
- [MongoDB Docs](https://docs.mongodb.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [openFDA API Docs](https://open.fda.gov/apis/)
- [ReportLab Docs](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

## Guía de Desarrollo

### Estructura de Ficheros

```
MediTrack/
├── view/
│   ├── app.py                              # Aplicación principal
│   └── sections/
│       ├── nuevo_informe.py               # Registro de pacientes
│       ├── buscar.py                      # Búsqueda y filtrado
│       ├── informes_guardados.py          # Visor de PDFs
│       ├── pacientes_dia.py               # Vista diaria
│       └── estadisticas.py                # Dashboard (desarrollo)
│
├── scripts/
│   ├── db.py                              # Conexión MongoDB
│   ├── generar_informe.py                 # IA generador de informes
│   ├── generar_pdf.py                     # Generador de PDFs
│   ├── openfda.py                         # Integración openFDA
│   └── cargar_dataset.py                  # Cargador de datos
│
├── data/
│   └── healthcare_dataset.csv             # Dataset de ejemplo
│
├── informes/                              # Carpeta de PDFs (gitignored)
│
├── .env                                   # Variables de entorno (gitignored)
├── .gitignore                             # Exclusiones Git
├── requirements.txt                       # Dependencias Python
├── README.md                              # Guía de uso
└── DOCUMENTATION.md                       # Este archivo

```

### Configuración del Entorno de Desarrollo

**1. Instalar Python 3.9+**
```bash
python --version  # Verificar versión
```

**2. Crear virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Crear archivo .env**
```bash
# .env
GROQ_API_KEY=gsk_your_key_here
MONGODB_URI=mongodb://localhost:27017/
```

**5. Iniciar MongoDB**
```bash
mongod  # En otra terminal
```

**6. Ejecutar aplicación**
```bash
streamlit run view/app.py
```

### Workflow de Desarrollo

**Para agregar nueva funcionalidad:**

1. Crear rama feature
```bash
git checkout -b feature/nueva-funcionalidad
```

2. Modificar archivos necesarios
```bash
# Editar scripts/ para backend
# Editar view/sections/ para frontend
```

3. Probar localmente
```bash
streamlit run view/app.py
```

4. Hacer commit
```bash
git add .
git commit -m "feat: descripción de cambios"
```

5. Push y crear Pull Request
```bash
git push origin feature/nueva-funcionalidad
```

### Agregar Nueva Sección a la Aplicación

**Paso 1:** Crear archivo en `view/sections/nueva_seccion.py`
```python
def render():
    st.header("Nueva Sección")
    # Tu código aquí
```

**Paso 2:** Importar en `view/app.py`
```python
elif seccion == "Nueva Sección":
    from view.sections.nueva_seccion import render
    render()
```

**Paso 3:** Agregar opción a sidebar
```python
seccion = st.radio("Navegación", [
    "Nuevo Informe",
    # ... otras secciones ...
    "Nueva Sección"  # Agregar aquí
])
```

---

## Contacto y Soporte

**Autores:** Anas El Ouahabi, Ahmed Berday  
**Curso:** Bases de Datos Avanzadas — 2025/2026  
**Última actualización:** Enero 2025

### Para Reportar Problemas

1. Verificar `.env` tiene `GROQ_API_KEY` configurado
2. Verificar MongoDB corre en `localhost:27017`
3. Revisar logs de Streamlit en consola
4. Contactar a autores con: versión Python, error exacto, pasos para reproducir
