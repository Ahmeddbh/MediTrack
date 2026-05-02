import pandas as pd
from pymongo import MongoClient

CSV_PATH = "data/healthcare_dataset.csv"

client = MongoClient("mongodb://localhost:27017/")
db = client["meditrack"]
collection = db["pacientes"]

collection.delete_many({})

df = pd.read_csv(CSV_PATH)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df["date_of_admission"] = pd.to_datetime(df["date_of_admission"])
df["discharge_date"] = pd.to_datetime(df["discharge_date"])

df["stay_days"] = (df["discharge_date"] - df["date_of_admission"]).dt.days
df["fda_info"] = None

records = df.to_dict(orient="records")

if records:
    collection.insert_many(records)

collection.create_index("medical_condition")
collection.create_index("medication")
collection.create_index("admission_type")
collection.create_index("doctor")

print("Carga completada.")
print("Documentos insertados:", collection.count_documents({}))
print("Índices creados:")
for name, info in collection.index_information().items():
    print(name, info)
