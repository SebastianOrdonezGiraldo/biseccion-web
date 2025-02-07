# 📌 Método de Bisección y Newton-Raphson - Aplicación Web

## 📖 Descripción
Esta es una aplicación web que implementa los métodos numéricos de **Bisección** y **Newton-Raphson** para encontrar raíces de ecuaciones. Permite ingresar una función matemática, definir el intervalo o punto inicial, seleccionar el método de cálculo y visualizar los resultados en forma de tabla y gráfica.

## 🚀 Características
✅ **Soporte para Bisección y Newton-Raphson** 📊
✅ **Interfaz moderna con Bootstrap** 🎨
✅ **Gráfica de convergencia interactiva** 📈
✅ **Exportación de resultados en CSV y PDF** 📄
✅ **Detección automática de intervalos** (en desarrollo) 🔍
✅ **Barra de progreso durante el cálculo** ⏳

## 📂 Estructura del Proyecto
```
biseccion-web/
│── app.py                   # Servidor Flask
│── requirements.txt          # Dependencias
│── static/                   # Archivos estáticos
│   ├── css/styles.css        # Estilos
│   ├── js/script.js          # Lógica de la interfaz
│── templates/                # Plantillas HTML
│   ├── index.html            # Interfaz principal
│── README.md                 # Documentación
```

## 🛠 Instalación y Ejecución
### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/SebastianOrdonezGiraldo/biseccion-web.git
cd biseccion-web
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar la aplicación
```bash
python app.py
```

### 4️⃣ Abrir en el navegador
```
http://127.0.0.1:5000/
```

## 🎯 Cómo Usar
1️⃣ **Ingresar la función** en términos de `x` (Ejemplo: `x**3 - 4*x - 9`).
2️⃣ **Seleccionar el método** (`Bisección` o `Newton-Raphson`).
3️⃣ **Definir el intervalo o punto inicial** (`a` y `b` para bisección, solo `a` para Newton-Raphson).
4️⃣ **Definir la tolerancia** (`1e-6` por defecto).
5️⃣ **Presionar "Calcular"** y esperar los resultados.
6️⃣ **Exportar en CSV o PDF** si se desea guardar los datos.

## 🔧 Dependencias
- **Flask** (Framework web)
- **NumPy** (Cálculos numéricos)
- **SymPy** (Manipulación simbólica)
- **Pandas** (Manejo de tablas y exportación de datos)
- **FPDF** (Generación de reportes PDF)
- **Plotly** (Gráficas interactivas)



---
📩 **Contacto**: [Sebastian Ordoñez Giraldo] - [sebastian789go@gmail.com] - [GitHub](https://github.com/tu-usuario)

