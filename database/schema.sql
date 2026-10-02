-- Esquema de base de datos para el carrito de compras "Vivero Raíz"
-- Ejecutar con: mysql -u root -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS vivero_raiz CHARACTER SET utf8mb4;
USE vivero_raiz;

CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    imagen VARCHAR(255) DEFAULT '',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Un carrito por sesión de navegador (sin necesidad de login)
CREATE TABLE IF NOT EXISTS carritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) UNIQUE NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS carrito_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrito_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    FOREIGN KEY (carrito_id) REFERENCES carritos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    UNIQUE KEY unico_item (carrito_id, producto_id)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(30) DEFAULT 'pendiente',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pedido_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
);

-- Datos de ejemplo
INSERT INTO categorias (nombre) VALUES ('Interior'), ('Exterior'), ('Suculentas'), ('Macetas y accesorios');

INSERT INTO productos (categoria_id, nombre, descripcion, precio, stock, imagen) VALUES
(1, 'Monstera Deliciosa', 'Planta de interior de hojas grandes y perforadas, ideal para espacios luminosos.', 450.00, 15, 'monstera.jpg'),
(1, 'Potus Dorado', 'Enredadera resistente que purifica el aire, requiere poca luz.', 180.00, 30, 'potus.jpg'),
(3, 'Echeveria Elegans', 'Suculenta compacta de roseta azulada, muy fácil de cuidar.', 95.00, 50, 'echeveria.jpg'),
(3, 'Cactus San Pedro', 'Cactus columnar de crecimiento rápido, perfecto para exteriores soleados.', 220.00, 20, 'cactus.jpg'),
(2, 'Lavanda', 'Arbusto aromático de flores moradas, atrae polinizadores.', 150.00, 25, 'lavanda.jpg'),
(2, 'Romero', 'Arbusto perenne aromático, ideal para huerto y cocina.', 120.00, 40, 'romero.jpg'),
(4, 'Maceta de barro 20cm', 'Maceta de barro cocido con plato, drenaje incluido.', 130.00, 60, 'maceta_barro.jpg'),
(4, 'Sustrato universal 5L', 'Mezcla de tierra balanceada para plantas de interior y exterior.', 85.00, 100, 'sustrato.jpg');
