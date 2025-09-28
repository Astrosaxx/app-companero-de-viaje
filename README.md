# 🛫 Compañero de Viaje

Una aplicación web moderna para planificar y organizar viajes en grupo. Permite a los usuarios crear viajes, unirse a viajes de otros usuarios y gestionar sus aventuras de manera colaborativa.

## ✨ Características

- 🎯 **Crear viajes**: Organiza tus propias aventuras con fechas, destinos y descripciones
- 👥 **Unirse a viajes**: Únete a viajes creados por otros usuarios
- 📊 **Dashboard inteligente**: Estadísticas en tiempo real de tus viajes
- 🎨 **Interfaz moderna**: Diseño glass con gradientes y animaciones suaves
- 📱 **Responsive**: Funciona perfectamente en móvil, tablet y desktop
- 🔐 **Autenticación segura**: Sistema de login y registro con validaciones
- 🎭 **Roles de usuario**: Organizadores y participantes con permisos diferenciados

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web ligero
- **MySQL** - Base de datos relacional
- **Bcrypt** - Encriptación de contraseñas
- **Python-dotenv** - Gestión de variables de entorno

### Frontend
- **Bootstrap 5.3** - Framework CSS responsive
- **FontAwesome 6.4** - Iconografía
- **CSS3** - Estilos personalizados con variables CSS
- **JavaScript** - Interactividad del cliente

### Base de Datos
- **MySQL 8.0+** - Sistema de gestión de base de datos
- **Relaciones** - Usuarios, viajes, participantes y roles

## 📋 Requisitos del Sistema

- Python 3.8 o superior
- MySQL 8.0 o superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

## 🛠️ Instalación

### Opción A: Instalación Automática (Recomendada)

```bash
# 1. Clonar el repositorio
git clone https://github.com/Astrosaxx/app-compa-ero-de-viaje.git
cd app-compa-ero-de-viaje

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Ejecutar instalación automática
python install.py
```

### Opción B: Instalación Manual

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/Astrosaxx/app-compa-ero-de-viaje.git
cd app-compa-ero-de-viaje
```

#### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
MYSQL_DB=compañero_de_viaje_db
MYSQL_USER=tu_usuario_mysql
MYSQL_PASSWORD=tu_contraseña_mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
SECRET_KEY=tu_clave_secreta_muy_segura
```

### 5. Configurar Base de Datos

#### Opción A: Usar el script automático
```bash
python setup_database.py
```

#### Opción B: Configuración manual

1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE compañero_de_viaje_db;
```

2. Ejecutar el script SQL:
```bash
mysql -u tu_usuario -p compañero_de_viaje_db < compañero-de-viaje.sql
```

3. Inicializar los roles:
```bash
python -c "
from app.config.mysqlconnection import connectToMySQL
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv('MYSQL_DB')

roles = [(1, 'Organizador'), (2, 'Participante')]
for rol_id, nombre in roles:
    query = 'INSERT IGNORE INTO roles_viaje (id, nombre) VALUES (%s, %s);'
    connectToMySQL(db).query_db(query, (rol_id, nombre))
    print(f'Rol {nombre} insertado')
"
```

## 🚀 Inicialización

### 1. Ejecutar la Aplicación

```bash
python server.py
```

La aplicación estará disponible en: `http://127.0.0.1:5014`

### 2. Acceder a la Aplicación

1. Abrir el navegador
2. Navegar a `http://127.0.0.1:5014`
3. Registrar una cuenta nueva
4. Iniciar sesión

## ⚡ Comandos Rápidos

```bash
# Instalación completa
python install.py

# Ejecutar servidor
python server.py

# Configurar base de datos
python setup_database.py

# Instalar dependencias
pip install -r requirements.txt

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Activar entorno virtual (macOS/Linux)
source .venv/bin/activate
```

## 📖 Uso de la Aplicación

### 🎯 Dashboard Principal

El dashboard muestra:
- **Estadísticas**: Viajes creados, unidos, disponibles y total participando
- **Tu agenda**: Viajes que has creado y a los que te has unido
- **Viajes disponibles**: Viajes de otros usuarios a los que puedes unirte

### ✈️ Crear un Viaje

1. Hacer clic en **"Crear viaje"**
2. Completar el formulario:
   - **Destino**: Título del viaje
   - **Descripción**: Detalles del viaje
   - **Fechas**: Inicio y fin del viaje
3. Hacer clic en **"Crear viaje"**

### 👥 Unirse a un Viaje

1. En la sección **"Viajes de otros usuarios"**
2. Hacer clic en **"Ver"** para ver detalles
3. Hacer clic en **"Unirme"** para unirse al viaje

### 🎛️ Gestionar Viajes

#### Viajes Creados
- **Ver**: Ver detalles del viaje
- **Editar**: Modificar información del viaje
- **Eliminar**: Eliminar el viaje (solo el creador)

#### Viajes Unidos
- **Ver**: Ver detalles del viaje
- **Salir**: Abandonar el viaje

### 👤 Gestión de Perfil

- **Registro**: Crear nueva cuenta
- **Login**: Iniciar sesión
- **Logout**: Cerrar sesión

## 🗂️ Estructura del Proyecto

```
app-compa-ero-de-viaje/
├── app/
│   ├── __init__.py              # Inicialización de Flask
│   ├── config/
│   │   └── mysqlconnection.py   # Conexión a MySQL
│   ├── controllers/
│   │   ├── usuarios.py          # Controlador de usuarios
│   │   └── viajes.py            # Controlador de viajes
│   ├── models/
│   │   ├── usuario_model.py     # Modelo de usuario
│   │   └── viaje_model.py       # Modelo de viaje
│   ├── static/
│   │   └── css/
│   │       └── style.css        # Estilos personalizados
│   └── templates/
│       ├── base.html            # Template base
│       ├── auth.html            # Autenticación
│       ├── dashboard.html        # Panel principal
│       ├── crear_viaje.html     # Crear viaje
│       ├── detalle_viaje.html   # Detalle del viaje
│       └── editar_viaje.html    # Editar viaje
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── compañero-de-viaje.sql       # Script de base de datos
├── requirements.txt             # Dependencias Python
├── server.py                    # Servidor Flask
└── setup_database.py            # Script de configuración
```

## 🎨 Características de Diseño

### 🎭 Interfaz Moderna
- **Glass Effect**: Efectos de cristal con backdrop-filter
- **Gradientes**: Colores suaves y profesionales
- **Animaciones**: Transiciones suaves y efectos hover
- **Responsive**: Adaptable a todos los dispositivos

### 🎨 Paleta de Colores
- **Navy**: `#0b2b40` - Azul marino
- **Teal**: `#1eb6c1` - Verde azulado
- **Mint**: `#dff7f9` - Verde menta
- **Sand**: `#fff6e5` - Arena
- **Ink**: `#12222e` - Tinta

### 📱 Responsive Design
- **Mobile First**: Optimizado para móviles
- **Breakpoints**: 576px, 768px, 992px, 1200px
- **Flexbox**: Layout moderno y flexible
- **Grid System**: Sistema de rejilla de Bootstrap

## 🔧 Configuración Avanzada

### Variables de Entorno

```env
# Base de datos
MYSQL_DB=compañero_de_viaje_db
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Seguridad
SECRET_KEY=clave_super_secreta_para_sesiones

# Desarrollo
FLASK_ENV=development
FLASK_DEBUG=True
```

### Personalización de Estilos

El archivo `app/static/css/style.css` contiene variables CSS que puedes modificar:

```css
:root {
  --navy: #0b2b40;        /* Color principal */
  --teal: #1eb6c1;        /* Color secundario */
  --mint: #dff7f9;        /* Color de fondo */
  --sand: #fff6e5;        /* Color de acento */
  --ink: #12222e;         /* Color de texto */
}
```

## 🐛 Solución de Problemas

### Error de Conexión a Base de Datos
```bash
# Verificar que MySQL esté ejecutándose
# Verificar credenciales en .env
# Verificar que la base de datos existe
```

### Error de Roles
```bash
# Ejecutar script de inicialización de roles
python -c "
from app.config.mysqlconnection import connectToMySQL
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv('MYSQL_DB')
roles = [(1, 'Organizador'), (2, 'Participante')]
for rol_id, nombre in roles:
    query = 'INSERT IGNORE INTO roles_viaje (id, nombre) VALUES (%s, %s);'
    connectToMySQL(db).query_db(query, (rol_id, nombre))
"
```

### Puerto en Uso
```bash
# Cambiar puerto en server.py
app.run(port=5015, debug=True)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Alonso Gatica** - [@Astrosaxx](https://github.com/Astrosaxx)

## 🙏 Agradecimientos

- Bootstrap por el framework CSS
- FontAwesome por los iconos
- Flask por el framework web
- MySQL por la base de datos
- Profesora liza molina

---

**¡Disfruta planificando tus aventuras! 🛫✈️🌍**
