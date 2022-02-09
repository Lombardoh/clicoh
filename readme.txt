EndPoints 

Todos los enpoints comienzan con api/ y siguen como esta detallado abajo, por ejemplo para crear una orden (asumiendo localhost) seria http://127.0.0.1:8000/api/orders-create/

- registrar prod	/products
- editar prod	/products/pk
- Eliminar un producto	/products/pk
- Consultar un producto	/products/pk
- Listar todos los productos	/products
- Modificar stock de un producto	/products/pk
	
- Listar todas las ordenes	/orders
- Consultar una orden y sus detalles	/oders/pk
	
- registrar orden	orders-create/ (tiene un template custom a fin de agilizar el proceso, idealmente usar web y no postman)
- editar orden	/oders/pk
- Eliminar una orden. Restaura stock del producto /oders/pk	


los auth token estan apagados momentanemente a fin de agilizar las pruebas (se pueden descomentar en cualquier momento desde views.py, usar el token 40f4b55c413490f1ab557a5ac271e8d0afa1b76c)