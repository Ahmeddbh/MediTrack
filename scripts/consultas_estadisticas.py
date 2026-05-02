from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meditrack"]
collection = db["pacientes"]

print("\n1. Total de ingresos")
print(collection.count_documents({}))

print("\n2. Top 5 diagnósticos")
for r in collection.aggregate([
    {"$group": {"_id": "$medical_condition", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}},
    {"$limit": 5}
]):
    print(r)

print("\n3. Distribución por tipo de admisión")
for r in collection.aggregate([
    {"$group": {"_id": "$admission_type", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]):
    print(r)

print("\n4. Estancia media por diagnóstico")
for r in collection.aggregate([
    {"$group": {"_id": "$medical_condition", "media_estancia": {"$avg": "$stay_days"}}},
    {"$sort": {"media_estancia": -1}}
]):
    print(r)

print("\n5. Top 5 medicamentos más prescritos")
for r in collection.aggregate([
    {"$group": {"_id": "$medication", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}},
    {"$limit": 5}
]):
    print(r)

print("\n6. Resultados de pruebas diagnósticas")
for r in collection.aggregate([
    {"$group": {"_id": "$test_results", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]):
    print(r)

print("\n7. Búsqueda por diagnóstico: Diabetes")
for r in collection.aggregate([
    {"$match": {"medical_condition": "Diabetes"}},
    {"$project": {"_id": 0, "name": 1, "age": 1, "medication": 1}},
    {"$limit": 3}
]):
    print(r)
