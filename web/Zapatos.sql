CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;

CREATE TABLE zapatos(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    precio_iva DECIMAL(9,2),
    foto VARCHAR(255),
    marca VARCHAR(255)
);

CREATE TABLE comentarios(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);

CREATE TABLE usuarios(
    usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL
);

INSERT INTO zapatos (nombre, descripcion, precio, precio_iva, foto, marca) VALUES 
('Air Max Plus', 'Zapatillas premium con diseño aerodinámico.', 185.00, 223.85, 'airmax_plus.jpg', 'Nike');

INSERT INTO comentarios (usuario, descripcion) VALUES 
('root', 'Se ha actualizado el stock de las zapatillas Nike hoy mismo.');

INSERT INTO usuarios (usuario, clave, perfil) VALUES 
('root', '1234', 'admin');
