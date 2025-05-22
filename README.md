# Pipeline de Ingesta de Datos (ETL) para Base de Datos SQL

Este proyecto es un pipeline **ETL (Extracción, Transformación y Carga)**  en Python que permite cargar datos desde archivos CSV externos hacia una base de datos SQL. Está diseñado para manejar múltiples modelos de datos (como `Category`, `City`, `Customer`, etc.), validando y cargando registros limpios en las tablas correspondientes.

## Estructura del Proyecto

El proyecto se organiza en torno a una clase principal y seis clases de modelos que son aceptados para la ingesta de datos en la base de datos de MySQL:

## 🔹 Clase `DataIngestion`

Esta clase gestiona **todo el proceso de ingesta**, desde la creación de tablas hasta la carga de datos usando `LOAD DATA INFILE` de MySQL.

### Métodos principales:

- `__init__(model_class: type)`  
  Recibe una clase de modelo (por ejemplo, `Category`, `City`) y la asocia con la tabla correspondiente en la base de datos.

- `generate_sql_path(script_name: str)`  
  Construye la ruta al archivo SQL que contiene los `CREATE TABLE`.

- `generate_externaldata_path()`  
  Construye la ruta al archivo CSV correspondiente para el modelo especificado.

- `create_tables_from_sql_file()`  
  Ejecuta el script SQL para crear las tablas en caso de que aún no existan.

- `load_external_data()`  
  Carga el archivo CSV externo en un DataFrame de pandas.

- `upload_data()`  
  Valida los datos usando la clase del modelo, los guarda en un CSV temporal y los carga a la base de datos con `LOAD DATA INFILE`. Si todos los registros ya existen, muestra una advertencia y no se realiza la carga.

---

## ⚙️ Modelos Soportados

La clase `DataIngestion` actualmente soporta los siguientes modelos:

- `Category`
- `City`
- `Customer`
- `Country`
- `Employee`
- `Product`
- `Sale`

---

## ✅ Ejemplo de Uso

```python
from models.Categories import Category
from pipelines.DataIngestion import DataIngestion

categories = DataIngestion(**MODEL)
categories.upload_data()
