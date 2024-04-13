# cardhub-back
# Setup

- Descargar el entorno virtual virtual env
    
    
    ```bash
    pip install virtualenv
    ```
    
- Inicia el entorno virtual en la carpeta actual
    
    ```bash
    virtualenv .
    ```
    
- Abre tu entorno virtual
    
    ```bash
    source Scripts/activate
    ```
    
- Instala el resto de dependencias usando el archivo requirements
    
    ```bash
    pip install -r requirements.txt
    ```
    
- Crea el archivo .env con las variables de entorno. 
    
    
    Nota: Debes colocar la base de datos que estés usando, gracias a las migraciones, no hace falta que sea postgres. Puedes usar la que quieras pero debes colocar la información en este archivo. Lo único que no cambia es el SECRET_KEY.
    
- Crear la base de datos: En el manejador de base de datos que elijas (sé que funciona en MySQL y en postgres) crea una tabla con el mismo nombre que pusiste en DB_NAME en el paso anterior.
- Hacer las migraciones
    
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    

# Iniciar el proyecto

- Correr el servidor con django
    
    ```bash
    python manage.py runserver
    ```
    
