# MediTrack
# MediTrack — Parte 1

Proyecto de **Bases de Datos Avanzadas (2025/2026)**  
Sistema de gestión de ingresos hospitalarios usando **MongoDB + Python**

---

## 📌 Descripción

En esta parte del proyecto se ha preparado todo el entorno necesario para trabajar con datos hospitalarios:

- Instalación y configuración de MongoDB en local (Ubuntu)
- Carga de un dataset clínico (~55.500 registros)
- Transformación de datos (CSV → JSON)
- Creación de índices para optimización
- Implementación de consultas estadísticas con Aggregation Pipeline

La base queda lista para que en la Parte 2 se integre la API de openFDA y se generen informes.

---

## 🗂 Estructura del proyecto
MediTrack/
│
├── data/ # Dataset (NO incluido en el repo)
├── scripts/ # Scripts Python
│ ├── cargar_dataset.py
│ └── consultas_estadisticas.py
│
├── docs/ # Documentación
├── requirements.txt # Dependencias
└── README.md

---

## ⚙️ Requisitos

- Ubuntu 20.04 o superior
- Python 3.10+
- MongoDB 7.0 (instalado en local)

---

## 🔗 Conexión a MongoDB

```text
mongodb://localhost:27017/
Base de datos:

meditrack

Colección:

pacientes
