# Henry - Proyecto Final Integrador

El siguiente proyecto consiste en un pipeline ejecutado a traves de una API REST construida con FastAPI que permite:

- Validar y cargar datos de un archivo .csv a una base de datos MySQL
- Establecer una unica conexion a MySQL para ejecutar consultar a traves de jupyter notebooks
- Implementacion de patrones Factory y Singleton.
- Crear dinamicamente las tablas de nuestra base de datos a traves de la carga de un script de sql

## 📁 Estructura del Proyecto

```css
Proyecto Final Integrador/
├── .venv/
├── documentation/
├── sql/
│   ├── create_tables.sql
|   └── load_data.sql
├── data/
│   ├── categories.csv
│   ├── cities.csv
│   ├── countries.csv
│   ├── customers.csv
│   ├── employees.csv
│   ├── products.csv
│   └── sales.csv
├── src/
│   ├── app/
│   │   ├── controllers.py
│   │   └── api.py  
│   ├── models/
│   │   ├── Categories.py
│   │   ├── Countries.py
│   │   ├── Cities.py
│   │   ├── Customers.py
│   │   ├── Employees.py
│   │   ├── Products.py
│   │   └── Sales.py
│   ├── database/
│   │   ├── DataBase__singleton.py
│   │   └── QueryBuilder.py
|   ├── factory/
│   │   ├── abstract/
│   │   ├── concrete/
│   │   ├── DataLoaderFactory.py
│   │   ├── DataValidationFactory.py
|   ├── pipelines/
│   │   ├── DataIngestion.py
│   ├── main.py
│
├── requirements.txt
└── README.md
```

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/garciaMatiasNicolas/Henry-PI-Base.git
cd Henry-PI-Base
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv .venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo .env en la raíz del proyecto con la siguiente estructura:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_base_de_datos
```
Asegúrate de que los valores coincidan con tu configuración local de MySQL.

### 5. Ejecutar la aplicación
```bash
uvicorn src.main:app --reload # podemos pasarle un puerto especifico por parametros --port 8080 (por defecto corre en el 8000)
```
La API estará disponible en http://127.0.0.1:8000.

## 📚 Documentación de la API
FastAPI genera automáticamente documentación interactiva. Puedes acceder a ella en:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## 📌 Endpoints Disponibles
### 1. Cargar Data de un modelo en expecifico desde CSV
Endpoint: *POST /pipeline/upload/{model_name}*

Descripción: Validacion y carga dinamica de los datos de un modelo en especifico (Categories, Cities, etc,) especificado en la ruta o de todos los modelos si se especifica all.

Respuesta exitosa 200 OK:
```json
{
  "message": "Data for <model_name> was uploaded successfully to the database."
}

{
  "message": "Data upload completed. Successfully processed models: products, customers.",
  "warning": "The following models failed to upload data: employees."
}
```
Respuesta 404 Not Found:
```json
{
  "detail": "Model 'invalid_model' not found. Available models are categories, cities, countries, products, employees, customers"
}
```
Respuesta 500 Internal Server Error:
```json
{
  "detail": "Failed to upload data for <model_name>: <error_details>"
}
```
Ejemplo de solicitud:
```bash
POST /pipeline/upload/customers
POST /pipeline/upload/all
```

## 🛠️ Consideraciones Técnicas
* Framework: FastAPI
* Base de Datos: Conexion con patron singleton a MySQL
* Data validation: Implementación personalizada con patron Factory
* Data Loader: Implementación personalizada con patron Factory

## 🛠️ Documentacion completa del sistema
Para mas documentacion y entendimiento del sistema, se encuentra un .docx dentro de la carpeta /documentation
Aqui encontraran informacion de los patrones implementados, de las clases y de la idea en si