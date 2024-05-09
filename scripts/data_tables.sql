-- Datos de ejemplo para la tabla Categoria
INSERT INTO Categoria (nombre) VALUES
    ('Ropa hombre'),
    ('Ropa mujer'),
    ('Zapatos'),
    ('Accesorios'),
    ('Bolsos');

-- Datos de ejemplo para la tabla Producto
INSERT INTO Producto (nombre, numero_referencia, coleccion, es_personalizable, id_categoria) VALUES
    ('Camisa de vestir', 'ABC123', 'Primavera', true, 1),
    ('Pantalón vaquero', 'XYZ456', 'Verano', false, 1),
    ('Vestido estampado', 'DEF789', 'Otoño', true, 2),
    ('Zapatos de cuero', 'GHI101', 'Invierno', false, 3),
    ('Bolso de mano negro', 'JKL112', 'Primavera', false, 5);

-- Datos de ejemplo para la tabla Color
INSERT INTO Color (nombre, precio, composicion, id_producto) VALUES
    ('Azul', 29.99, 'Algodón', 1),
    ('Negro', 39.99, 'Denim', 2),
    ('Rojo', 49.99, 'Poliéster', 3),
    ('Marrón', 59.99, 'Cuero', 4),
    ('Blanco', 19.99, 'Poliéster', 5),
    ('Verde', 34.99, 'Algodón', 1),
    ('Blanco', 29.99, 'Algodón', 1),
    ('Negro', 49.99, 'Denim', 2),
    ('Gris', 39.99, 'Denim', 2),
    ('Amarillo', 54.99, 'Poliéster', 3),
    ('Negro', 59.99, 'Poliéster', 3),
    ('Café', 69.99, 'Cuero', 4),
    ('Negro', 79.99, 'Cuero', 4),
    ('Azul', 24.99, 'Poliéster', 5),
    ('Negro', 19.99, 'Poliéster', 5);

-- Datos de ejemplo para la tabla Oferta
INSERT INTO Oferta (nombre_oferta, porcentaje_oferta, fecha_inicio, fecha_fin) VALUES
    ('Rebaja Primavera 2023', 20, '2024-03-01', '2024-04-01'),
    ('Oferta Verano 2023', 30, '2024-06-15', '2024-07-15'),
    ('Descuento Invierno 2023', 25, '2024-10-01', '2024-12-01'),
    ('Promoción Otoño 2023', 15, '2024-09-01', '2024-10-01'),
    ('Oferta Navideña 2023', 50, '2024-12-15', '2024-12-31');

INSERT INTO Oferta (nombre_oferta, porcentaje_oferta, fecha_inicio) VALUES
    ('Rebaja Primavera 2024', 20, '2024-03-01'),
    ('Oferta Verano 2024', 30, '2024-06-15');

-- Datos de ejemplo para la tabla Oferta_Ropa
INSERT INTO Oferta_Ropa (id_oferta, id_color) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 7),
    (3, 8),
    (4, 9),
    (5, 10);

-- Datos de ejemplo para la tabla Oferta_Categoria
INSERT INTO Oferta_Categoria (id_oferta, id_categoria) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 1),
    (5, 5);
