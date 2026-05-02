# MediTrack — Guía de inicio para la Parte 2

Este repositorio contiene la Parte 1 del proyecto MediTrack: carga del dataset hospitalario en MongoDB y consultas estadísticas básicas.

## 1. Clonar el repositorio

```bash
git clone https://github.com/Ahmeddbh/MediTrack.git
cd MediTrack
2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
4. Descargar el dataset

Descargar desde Kaggle:

Healthcare Dataset — Prasad Patil

El archivo debe llamarse:

healthcare_dataset.csv

Colocarlo en:

data/healthcare_dataset.csv

La estructura debe quedar así:

MediTrack/
├── data/
│   └── healthcare_dataset.csv
├── scripts/
│   ├── cargar_dataset.py
│   └── consultas_estadisticas.py
├── docs/
├── requirements.txt
└── README.md
5. Comprobar que MongoDB está activo
sudo systemctl status mongod

Debe aparecer:

active (running)

Si está parado:

sudo systemctl start mongod
6. Cargar el dataset en MongoDB
python3 scripts/cargar_dataset.py

Resultado esperado:

Documentos insertados: 55500

Esto crea:

Base de datos: meditrack
Colección: pacientes

También añade los campos:

stay_days
fda_info

El campo fda_info está preparado para que en la Parte 2 se rellene con datos de openFDA.

7. Ejecutar consultas de prueba
python3 scripts/consultas_estadisticas.py

Este script comprueba que los datos están bien cargados mediante 7 consultas estadísticas.

8. Conexión desde Python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meditrack"]
collection = db["pacientes"]
9. Comprobar número de documentos
python3 -c "from pymongo import MongoClient; c=MongoClient('mongodb://localhost:27017/'); print(c['meditrack']['pacientes'].count_documents({}))"

Resultado esperado:

55500
10. Ver un documento de ejemplo
python3 -c "from pymongo import MongoClient; import pprint; c=MongoClient('mongodb://localhost:27017/'); pprint.pp(c['meditrack']['pacientes'].find_one())"
Estado actual
MongoDB instalado y funcionando.
Dataset cargado correctamente.
Base de datos meditrack creada.
Colección pacientes creada.
55.500 documentos insertados.
Índices creados sobre:
medical_condition
medication
admission_type
doctor
