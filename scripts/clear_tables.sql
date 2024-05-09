-- Limpiar datos de la tabla Oferta_Ropa
DELETE FROM Oferta_Ropa;
-- Reiniciar la secuencia de ID de Oferta_Ropa
ALTER SEQUENCE oferta_ropa_id_seq RESTART WITH 1;

-- Limpiar datos de la tabla Oferta_Categoria
DELETE FROM Oferta_Categoria;
-- Reiniciar la secuencia de ID de Oferta_Categoria
ALTER SEQUENCE oferta_categoria_id_seq RESTART WITH 1;

-- Limpiar datos de la tabla Oferta
DELETE FROM Oferta;
-- Reiniciar la secuencia de ID de Oferta
ALTER SEQUENCE oferta_id_seq RESTART WITH 1;

-- Limpiar datos de la tabla Color
DELETE FROM Color;
-- Reiniciar la secuencia de ID de Color
ALTER SEQUENCE color_id_seq RESTART WITH 1;

-- Limpiar datos de la tabla Producto
DELETE FROM Producto;
-- Reiniciar la secuencia de ID de Producto
ALTER SEQUENCE producto_id_seq RESTART WITH 1;

-- Limpiar datos de la tabla Categoria
DELETE FROM Categoria;
-- Reiniciar la secuencia de ID de Categoria
ALTER SEQUENCE categoria_id_seq RESTART WITH 1;
