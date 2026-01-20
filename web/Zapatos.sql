CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;

CREATE TABLE zapatos(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
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
('Air Max Plus', 'Zapatillas de running con amortiguación premium y diseño aerodinámico.', 185.50, 'airmax_plus.jpg', 'Nike'),
('Classic Leather', 'Calzado casual de cuero blanco, ideal para uso diario.', 89.99, 'classic_leather.png', 'Reebok'),
('Ultraboost 22', 'Zapatillas de alto rendimiento con retorno de energía superior.', 160.00, 'ultraboost.jpg', 'Adidas'),
('Old Skool', 'Zapatillas de lona clásicas con la icónica banda lateral.', 75.00, 'vans_oldskool.jpg', 'Vans'),
('Chuck Taylor All Star', 'Botas de lona de corte alto, un clásico que nunca muere.', 65.00, 'converse_high.jpg', 'Converse');

INSERT INTO comentarios (usuario, descripcion) VALUES 
('juan_perez', 'Las Air Max son comodísimas, valen cada céntimo.'),
('maria_sneakers', 'Me encantaron las Vans, el envío fue muy rápido.'),
('juan_perez', '¿Tienen las Adidas en color azul? No las veo en el catálogo.'),
('root', 'Se ha actualizado el stock de las Converse hoy mismo.'),
('maria_sneakers', 'Las Reebok son un poco estrechas, recomiendo pedir media talla más.');

INSERT INTO usuarios (usuario, clave, perfil) VALUES 
('root', '1234', 'admin'),
('test', 'test', 'test'),
('admin_ventas', 'admin2026', 'empleado');
