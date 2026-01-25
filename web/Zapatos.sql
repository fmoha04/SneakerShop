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

INSERT INTO zapatos (nombre, descripcion, precio, foto, marca) VALUES 
('Air Max Plus', 'Zapatillas de running premium y diseño aerodinámico.', 185.50, 'airmax_plus.jpg', 'Nike'),
('Ultraboost 22', 'Zapatillas de alto rendimiento.', 160.00, 'ultraboost.jpg', 'Adidas'),
('Old Skool', 'Zapatillas de lona clásicas con la icónica banda lateral.', 75.00, 'vans_oldskool.jpg', 'Vans');

INSERT INTO comentarios (usuario, descripcion) VALUES 
('root', 'Se ha actualizado el stock de las Converse hoy mismo.');

INSERT INTO usuarios (usuario, clave, perfil) VALUES 
('root', '1234', 'admin'),
('test', 'test', 'normal');
