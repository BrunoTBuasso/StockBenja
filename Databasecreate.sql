CREATE DATABASE lara;
-- Usar la base de datos
USE lara;
-- Crear la tabla para almacenar los registros
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_apellido VARCHAR(255) NOT NULL,
    producto VARCHAR(255) NOT NULL,
    celular VARCHAR(20) NOT NULL
);
ALTER TABLE clientes
ADD COLUMN fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP;