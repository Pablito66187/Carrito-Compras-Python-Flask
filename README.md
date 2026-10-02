# Vivero Raíz — Carrito de compras (Flask + MySQL + JS)

Proyecto de ejemplo de una tienda en línea con carrito de compras funcional:
catálogo de productos, agregar/actualizar/eliminar ítems del carrito vía AJAX
(sin recargar la página) y confirmación de pedido, todo con sesión de
navegador (no requiere login).

## Estructura del proyecto

```
carrito_flask/
├── app.py                 # Rutas Flask (vistas + endpoints AJAX)
├── cart.py                # Lógica de negocio del carrito
├── db.py                  # Conexión a MySQL (pool de conexiones)
├── config.py               # Configuración (lee variables de entorno)
├── requirements.txt
├── .env.example
├── database/
│   └── schema.sql          # Tablas + datos de ejemplo
├── templates/              # HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── product_detail.html
│   └── cart.html
└── static/
    ├── css/style.css
    └── js/cart.js           # Llamadas fetch a los endpoints /api/carrito/*
```

## 1. Requisitos

- Python 3.10+
- MySQL 8.x (o MariaDB) corriendo localmente o accesible por red

## 2. Instalación

```bash
cd carrito_flask
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configurar la base de datos

```bash
mysql -u root -p < database/schema.sql
```

Esto crea la base `vivero_raiz` con las tablas `categorias`, `productos`,
`carritos`, `carrito_items`, `pedidos`, `pedido_items` y algunos productos
de ejemplo.

## 4. Variables de entorno

Copia `.env.example` a `.env` y ajusta tus credenciales de MySQL:

```bash
cp .env.example .env
```

## 5. Ejecutar la aplicación

```bash
python app.py
```

Abre `http://127.0.0.1:5000` en tu navegador.

## Cómo funciona el carrito

- Cada visitante recibe un `session_id` guardado en la cookie de sesión de
  Flask, ligado a una fila en la tabla `carritos`. No hace falta iniciar
  sesión para comprar.
- Los botones "Agregar al carrito" llaman a `POST /api/carrito/agregar`
  vía `fetch()` (ver `static/js/cart.js`), y el badge del carrito en el
  header se actualiza sin recargar la página.
- En `/carrito`, cambiar la cantidad dispara `POST /api/carrito/actualizar`
  y el botón "Eliminar" dispara `POST /api/carrito/eliminar`.
- Al confirmar el pedido (`POST /checkout`) se crea una fila en `pedidos`
  con sus `pedido_items`, se descuenta el stock y se vacía el carrito.

## Posibles mejoras

- Agregar autenticación de usuarios (Flask-Login) para historial de pedidos.
- Subir imágenes reales de productos (actualmente se usa un placeholder).
- Integrar una pasarela de pago (Stripe, MercadoPago, etc.) en `/checkout`.
- Agregar paginación y buscador de texto en el catálogo.
# Carrito-Compras-Python-Flask
