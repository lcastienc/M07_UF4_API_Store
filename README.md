# PRÀCTICA FINAL - API REST BOTIGA ONLINE
## Base de Datos
### Descripción de la Base de Datos
En esta práctica se utilizará una base de datos con el nombre `TiendaOnline` hecha con postgresql
### Estructura de las Tablas
![TiendaOnline - public](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/314d139f-13df-4846-ba5f-52427568641d)

## APP CLIENT
### AÑADIR NUEVOS CLIENTES
Implementación del método para añadir un nuevo cliente a la base de datos.

![add_client](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/e2ffee3a-d44f-4397-b33a-99da9447f311)

Codigo para a un nuevo cliente:
```python
@api_view(['POST'])
def add_client(request):
    data = request.data

    # Verificar si el cliente ya existe basado en el correo electrónico
    if Client.objects.filter(email=data.get('email')).exists():
        return Response({"message": "Este cliente ya existe"}, status=400)

    # Serializar los datos
    serializer = ClientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": 'Cliente creado exitosamente', "data": serializer.data}, status=201)
    return Response({"error": serializer.errors, "message": 'No se ha podido crear el cliente'}, status=400)
```
### VER INFORMACIÓN DE TODOS LOS CLIENTES
Implementación del método para leer los datos de los clientes desde la base de datos.

![clietns](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/668d607e-cb5d-4395-b786-8a9e821098ae)

Codigo para ver toda la informacion de los clientes:
```python
@api_view(['GET'])
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response({"status": "success", "message": "Lista de clientes obtenida exitosamente", "data": serializer.data}, status=200)
```

### VER INFORMACIÓN DE UN SOLO CLIENTE
Implementación del método para leer los datos de un cliente desde la base de datos.

![clietns](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/c2ac68dd-6709-4adc-997d-5d17774450f2)

Codigo para ver toda la informacion de un cliente:
```python
@api_view(['GET'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)
    serializer = ClientSerializer(client)
    return Response({"status": "success", "message": "Información del cliente obtenida exitosamente", "data": serializer.data}, status=200)
```

### ACTUALIZAR DATOS CLIENTES
Implementación del método para actualizar los datos de un cliente.

![edit_client](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/61690211-fb78-4a7e-88d0-b30df162e378)

Codigo para actualizar la informacion de un cliente:
```python
@api_view(['PUT'])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)

    serializer = ClientSerializer(client, data=request.data, partial=True)  # partial=True para permitir actualizaciones parciales
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message": "Cliente actualizado exitosamente", "data": serializer.data}, status=200)
    return Response({"error": serializer.errors, "message": "No se ha podido actualizar el cliente"}, status=400)
```

### ELIMINAR UN CLIENTE
Implementación del método para eliminar los datos de un cliente.

![delete_client](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/b3fc461d-bc2e-4f88-97a9-6182b45c1805)

Codigo para eliminar toda la informacion de un cliente:
```python
@api_view(['DELETE'])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)

    client.delete()
    return Response({"status": "success", "message": "Cliente eliminado exitosamente"}, status=200)
```
### URLS CLIENT
```python
urlpatterns = [
    path('add_client/', views.add_client, name='add_client'),
    path('', views.client_list, name='client_list'),
    path('client/<str:pk>/', views.client_detail, name='client_detail'),
    path('update_client/<str:pk>/', views.update_client, name='update_client'),
    path('delete_client/<str:pk>/', views.delete_client, name='delete_client'),
]
```
### MODEL CLIENT
```python
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.id} {self.name} {self.surname} {self.email} {self.password} {self.created_at} {self.updated_at}'
```

## APP CATALEG
### AÑADIR NUEVOS PRODUCTOS
Implementación del método para añadir un nuevo producto a la base de datos.

![add_product](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/6f5a6938-15e3-45b8-97b8-a10ec16277e5)

Codigo para añadir un nuevo producto:
```python
@api_view(['POST'])
def add_product(request):
    # Extraer datos del request
    data = request.data
    # Verificar si el producto ya existe basado en algún campo único, por ejemplo, el nombre
    if Product.objects.filter(name=data.get('name')).exists():
        return Response({"message": "El producto ya existe"}, status=400)

    # Serializar los datos
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Producto añadido exitosamente", "data": serializer.data}, status=201)

    return Response({"error": serializer.errors, "message": "No se ha podido añadir el producto"}, status=400)
```
### VER TODOS LOS PRODUCTOS
Implementación del método para leer los datos de los productos de la base de datos.

![list_prod](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/bf6dd67f-a303-4fed-a0c4-991d5109dbb1)

Codigo para ver todos los productos:
```python
@api_view(['GET'])
def products_list(request):
    products = Product.objects.filter(deleted=False)
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success", "message": "Lista de productos obtenida exitosamente", "data": serializer.data}, status=200)
```

### VER INFORMACION DE UN PRODUCTO
Implementación del método para leer los datos de un producto de la base de datos.

![onde_prod](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/41e12719-45bd-4958-8932-85be58ff2f84)

Codigo para ver un producto:
```python
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, deleted=False)
    except Product.DoesNotExist:
        return Response({"error": "El producto que buscas no existe"}, status=404)
    serializer = ProductSerializer(product)
    return Response({"status": "success", "message": "Información del producto obtenida exitosamente", "data": serializer.data}, status=200)
```

### ACTUALIZAR PRODUCTOS
Implementación del método para actualizar los datos de un producto de la base de datos.

![update_prod](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/97f318c1-2e65-42de-ab51-6ebc12c437c7)

Codigo para actualizar los datos de un producto:
```python
@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto que quieres modificar no existe"}, status=404)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": 'Producto actualizado exitosamente', "data": serializer.data}, status=200)
    return Response({"error": serializer.errors, "message": 'No se ha podido actualizar el producto'}, status=400)
```
### ACTUALIZAR STOCK PRODUCTOS
Implementación del método para actualizar el stock de un producto de la base de datos.

![update_stock](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/e521c56f-2bbd-4fcf-b33c-c68da6700c53)

Codigo para actualizar el stock de un producto:
```python
@api_view(['PATCH'])
def update_stock_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto que quieres actulizar el stock no existe"}, status=404)
    product.stock = request.data.get('stock',product.stock)
    product.save()
    return Response({"message": "Producto actualizado exitosamente"}, status=200)
```

### ELIMINAR PRODUCTOS MEDIANTE BORRADO LOGICO
Implementación del método para eliminar los datos de un producto de la base de datos.

![del_prod](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/420fd800-6ac7-45f3-a9bd-85441ef36bc1)

Codigo para eliminar un producto:
```python
@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto no existe"}, status=404)

    product.deleted = True
    product.save()

    return Response({"status": "success", "message": "Producto marcado como eliminado"}, status=200)
```
### URLS CATALEG
```python
urlpatterns = [
    path('products/add_product/', views.add_product, name='add_product'),
    path('products/update_product/<str:pk>/', views.update_product, name='update_product'),
    path('products/update_stock_product/<str:pk>/', views.update_stock_product, name='update_stock_product'),
    path('products/delete_product/<str:pk>/', views.delete_product, name='delete_product'),
    path('products/', views.products_list, name='products_list'),
    path('products/<str:pk>', views.product_detail, name='product_detail'),
]
```
### MODEL CATALEG
```python
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    fabrication = models.CharField(max_length=100)
    OriginCountry = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name} {self.price} {self.description} {self.stock} {self.fabrication} {self.OriginCountry} {self.deleted} {self.created_at} {self.updated_at}'
```

## APP CARRETO
### CREAR UN NUEVO CARRITO
Implementación del método para crear un nuevo carrito a la base de datos.

![create_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/096b0e0f-af47-49ad-afa4-847ae35bd9a0)

Codigo para crear un nuevo carrito:
```python
@api_view(['POST'])
def create_carreto(request):
    client_id = request.data.get('client_id')
    if not Client.objects.filter(id=client_id).exists():
        return Response({"error": "Cliente no encontrado"}, status=404)
    if Carreto.objects.filter(client_id=client_id, finalitzat=False).exists():
        return Response({"error": "Ya existe un carrito abierto para este cliente"}, status=400)

    carreto = Carreto.objects.create(client_id=client_id)
    serializer = CarretoSerializer(carreto)
    return Response({"status": "success", "message": "Carrito creado exitosamente", "data": serializer.data}, status=201)
```

### VER INFORMACION DE TODOS LOS CARRITOS
Implementación del método para crear un nuevo carrito a la base de datos.

![list_carretons](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/5a28184d-f8e5-4eea-bf0c-727a1c1fa66c)

Codigo para crear un nuevo carrito:
```python
@api_view(['GET'])
def list_all_carretos(request):
    carretos = Carreto.objects.all()
    response_data = []

    for carreto in carretos:
        carreto_data = CarretoSerializer(carreto).data
        carreto_products = CarretoProduct.objects.filter(carreto=carreto)
        carreto_products_data = CarretoProductSerializer(carreto_products, many=True).data

        carreto_info = {
            "carreto_info": carreto_data,
            "carreto_products": carreto_products_data
        }

        response_data.append(carreto_info)

    return Response({"status": "success", "message": "Todos los carritos encontrados exitosamente", "data": response_data}, status=200)
```

### AÑADIR PRODUCTOS AL CARRITO
Implementación del método para añadir productos a un carrito a la base de datos.

![add_prod_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/b8f2cda4-f699-4403-800a-f2a177330f1c)

Codigo para añadir productos a un carrito:
```python
@api_view(['POST'])
def add_product_to_carreto(request):
    carreto_id = request.data.get('carreto_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        carreto = Carreto.objects.get(id=carreto_id, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "No hay carrito abierto para este cliente"}, status=404)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"status": "error", "message": "Producto no encontrado"}, status=404)

    if product.stock < quantity:
        return Response({"status": "error", "message": "No hay suficiente stock disponible"}, status=400)

    # Calcular el precio total por la cantidad de productos
    total_price = product.price * quantity

    # Crear la relación CarretoProduct
    carreto_product = CarretoProduct.objects.create(carreto=carreto, product=product, quantitat=quantity, preu=total_price)

    # Actualizar el precio total del carrito
    carreto.preu_total += total_price
    carreto.save()

    # Construir la respuesta completa
    response_data = {
        "status": "success",
        "message": "Producto agregado al carrito exitosamente",
        "carreto_info": {
            "id": carreto.id,
            "client": carreto.client.id,
            "preu_total": carreto.preu_total,
            "finalitzat": carreto.finalitzat,
            "created_at": carreto.created_at,
            "updated_at": carreto.updated_at,
        },
        "product_info": {
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity,
            "total_price_for_this_product": total_price
        }
    }
    return Response(response_data, status=201)
```

### ELIMINAR PRODUCTOS DEL CARRITO
Implementación del método para eliminar productos de un carrito de la base de datos.

![delete_prod_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/8880b5c7-5557-498b-8a28-b10e056c9b56)

Codigo para eliminar los productos de un carrito:
```python
@api_view(['POST'])
def delete_product_from_carreto(request):
    carreto_id = request.data.get('carreto_id')
    product_id = request.data.get('product_id')

    try:
        carreto = Carreto.objects.get(id=carreto_id, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "No hay carrito abierto para este cliente"}, status=404)

    carreto_products = CarretoProduct.objects.filter(carreto=carreto, product_id=product_id)

    if not carreto_products.exists():
        return Response({"status": "error", "message": "El producto no está en el carrito"}, status=404)

    # Calcular el precio total a restar del carrito
    total_price_to_subtract = sum(cp.preu for cp in carreto_products)

    # Actualizar el precio total del carrito
    carreto.preu_total -= total_price_to_subtract
    carreto.save()

    # Eliminar todos los productos del carrito
    carreto_products.delete()

    # Serializar la respuesta
    carreto_serializer = CarretoSerializer(carreto)

    # Construir la respuesta completa
    response_data = {
        "status": "success",
        "message": "Producto(s) eliminado(s) del carrito exitosamente",
        "carreto_info": carreto_serializer.data
    }
    return Response(response_data, status=200)
```

### ELIMINAR EL CARRITO
Implementación del método para eliminar un carrito de la base de datos.

![delete_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/623e4e60-4284-45dc-96ef-9c75bbac98d9)

Codigo para eliminar un carrito:
```python
@api_view(['DELETE'])
def delete_carreto(request, client_id, carreto_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    try:
        carreto = Carreto.objects.get(id=carreto_id, client=client, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "Carrito no encontrado o ya finalizado"}, status=404)

    carreto.delete()

    return Response({"status": "success", "message": "Carrito eliminado exitosamente"}, status=200)
```

### MODIFICAR CANTIDAD DE PRODUCTOS DEL CARRITO
Implementación del método para actualizar la cantidad de los productos de un carrito.

![update_quantity_prod](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/2bb69550-1d5b-4692-bf72-9bcbb044f659)

Codigo para actualizar la cantidad de los productos del carrito:
```python
@api_view(['PUT'])
def update_product_quantity(request):
    client_id = request.data.get('client_id')
    carreto_id = request.data.get('carreto_id')
    product_id = request.data.get('product_id')
    new_quantity = request.data.get('new_quantity')

    if not (client_id and carreto_id and product_id and new_quantity):
        return Response({"status": "error", "message": "Se requieren todos los campos: client_id, carreto_id, product_id y new_quantity"}, status=400)

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    try:
        carreto = Carreto.objects.get(id=carreto_id, client=client, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "Carrito no encontrado o ya finalizado"}, status=404)

    try:
        carreto_product = CarretoProduct.objects.get(carreto=carreto, product_id=product_id)
    except CarretoProduct.DoesNotExist:
        return Response({"status": "error", "message": "Producto no encontrado en el carrito"}, status=404)

    try:
        new_quantity = int(new_quantity)
        if new_quantity < 1:
            return Response({"status": "error", "message": "La cantidad debe ser al menos 1"}, status=400)
    except ValueError:
        return Response({"status": "error", "message": "La cantidad debe ser un número entero"}, status=400)

    if new_quantity > carreto_product.product.stock:
        return Response({"status": "error", "message": "La cantidad solicitada excede el stock disponible"}, status=400)

    # Actualizar la cantidad y el precio total del carrito
    previous_quantity = carreto_product.quantitat
    carreto_product.quantitat = new_quantity
    carreto_product.preu = carreto_product.product.price * new_quantity
    carreto_product.save()

    carreto.preu_total += (new_quantity - previous_quantity) * carreto_product.product.price
    carreto.save()

    carreto_serializer = CarretoSerializer(carreto)
    carreto_products = carreto.carretoproduct_set.all()
    carreto_products_serializer = CarretoProductSerializer(carreto_products, many=True)

    response_data = {
        "status": "success",
        "message": "Cantidad del producto actualizada exitosamente",
        "carreto_info": carreto_serializer.data,
        "carreto_products": carreto_products_serializer.data
    }

    return Response(response_data, status=200)
```

### CONSULTAR LISTADO DE PRODUCTOS DEL CARRITO
Implementación del método para leer informacion de los productos de un carrito de la base de datos.

![list_prod_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/7d99cd0d-4422-468c-b1f7-c74dca3a4c7c)

Codigo para leer los productos de un carrito:
```python
@api_view(['GET'])
def list_carreto_products(request, client_id, carreto_id):
    if not client_id or not carreto_id:
        return Response({"status": "error", "message": "Se requiere el ID del cliente y el ID del carrito"}, status=400)

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    try:
        carreto = Carreto.objects.get(id=carreto_id, client=client, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "No hay carrito abierto para este cliente"}, status=404)

    carreto_serializer = CarretoSerializer(carreto)
    carreto_products = carreto.carretoproduct_set.all()
    carreto_products_serializer = CarretoProductSerializer(carreto_products, many=True)

    response_data = {
        "status": "success",
        "message": "Carrito y productos encontrados exitosamente",
        "carreto_info": carreto_serializer.data,
        "carreto_products": carreto_products_serializer.data
    }

    return Response(response_data, status=200)
```

### COMPRAR CARRITO
Implementación del método para realizar la conpra de un carrito.

![comprar_carreto](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/972d95ca-f99d-48bc-94e4-1b014b6b01cf)

Codigo para comprar un carrito:
```python
@api_view(['POST'])
def realitzar_compra(request):
    client_id = request.data.get('client_id')
    carreto_id = request.data.get('carreto_id')

    if not client_id or not carreto_id:
        return Response({"status": "error", "message": "Se requieren los campos: client_id y carreto_id"}, status=400)

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    try:
        carreto = Carreto.objects.get(id=carreto_id, client=client, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "Carrito no encontrado o ya finalizado"}, status=404)

    # Actualizar el estado del carrito a finalizado
    carreto.finalitzat = True
    carreto.save()

    # Crear un nuevo registro en la tabla de comanda
    comanda = Comanda.objects.create(client=client, carreto=carreto)

    # Serializar los datos
    comanda_serializer = ComandaSerializer(comanda)
    carreto_products = CarretoProduct.objects.filter(carreto=carreto)
    carreto_products_serializer = CarretoProductSerializer(carreto_products, many=True)

    response_data = {
        "status": "success",
        "message": "Compra realizada exitosamente",
        "comanda_info": comanda_serializer.data,
        "carreto_products": carreto_products_serializer.data
    }

    return Response(response_data, status=200)
```
### URLS CARRITO
```python
urlpatterns = [
    path('create_carreto/', views.create_carreto, name='create_carreto'),
    path('add_product_carreto/', views.add_product_to_carreto, name='add_product_carreto'),
    path('delete_product_carreto/', views.delete_product_from_carreto, name='delete_product_carreto'),
    path('delete_carreto/<int:client_id>/<int:carreto_id>/', views.delete_carreto, name='delete_carreto'),
    path('update_quantity_product/', views.update_product_quantity, name='update_quantity_product'),
    path('list_products_carreto/<int:client_id>/<int:carreto_id>/', views.list_carreto_products, name='list_carreto_products'),
    path('comprar_carreto/', views.realitzar_compra, name='comprar_carreto'),
    path('', views.list_all_carretos, name='list_all_carretos'),
]
```
### MODEL CARRITO
```python
class Carreto(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    #especifico el valor del precion del carrito como 0
    preu_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    finalitzat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.client} {self.preu_total} {self.finalitzat} {self.created_at} {self.updated_at}'

class CarretoProduct(models.Model):
    id = models.AutoField(primary_key=True)
    carreto = models.ForeignKey(Carreto, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantitat = models.PositiveIntegerField(default=1)
    preu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f'{self.id} {self.carreto} {self.product} {self.quantitat} {self.price}'
```

## APP COMANDES
### MOSTRAR HISTORIAL DE COMANDES
Implementación del método para leer las comandes desde la base de datos.

![list_comandes](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/8d4f184b-bd0b-497c-8258-5b41fde6a7ef)

Codigo para ver las comandes:
```python
@api_view(['GET'])
def list_comandes(request):
    comandes = Comanda.objects.all()
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes recuperado exitosamente", "data": serializer.data})
```

### MOSTRAR HISTORIAL COMANDES DE UN CLIENTE
Implementación del método para leer las comandes de un solo cliente desde la base de datos.

![list_comandes_client](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/da70ffc1-5ed2-4ad3-9ffe-61dc71458f94)

Codigo para ver las comandes de un cliente:
```python
@api_view(['GET'])
def list_comandes_by_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    comandes = Comanda.objects.filter(client=client)
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes del cliente recuperado exitosamente", "data": serializer.data})
```

### MOSTRAR HISTORIAL COMANDES NO FINALIZADAS
Implementación del método para leer las comandes no finalizadas desde la base de datos.

![comandes_no_finalizadas](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/c48027ac-c5a7-4d3f-85f7-48ba7c2aa1a4)

Codigo para ver las comandes no finalizadas:
```python
@api_view(['GET'])
def list_open_comandes(request):
    comandes = Comanda.objects.filter(estat='Obert')
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes abiertas recuperado exitosamente", "data": serializer.data})
```
### URLS COMANDES
```python
urlpatterns = [
    path('llista_comandes/', views.list_comandes, name='list_comandes'),
    path('comandes_client/<int:client_id>/', views.list_comandes_by_client, name='list_comandes_by_client'),
    path('comandes_obertes/', views.list_open_comandes, name='list_open_comandes'),
]
```
### MODEL COMANDES
```python
class Comanda(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    carreto = models.ForeignKey(Carreto, on_delete=models.CASCADE)
    estat = models.CharField(max_length=20, default='Obert')
    data_comanda = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.client} - {self.carreto} - {self.estat} - {self.data_comanda} - {self.created_at} - {self.updated_at}'
```


## APP PAGAMENT
### PAGAR UNA COMANDA
Implementación del método para pagar una comanda.

![pagar_comanda](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/ea20c723-231c-4980-be5d-853c7b42868a)

Codigo para pagar una comanda:
```python
@api_view(['POST'])
def pagar_comanda(request):
    comanda_id = request.data.get('comanda_id')
    card_number = request.data.get('card_number')
    expiry_date = request.data.get('expiry_date')
    cvc = request.data.get('cvc')

    # Verificar si la comanda está abierta
    try:
        comanda = Comanda.objects.get(id=comanda_id, estat='Obert')
    except Comanda.DoesNotExist:
        return Response({"status": "error", "message": "La comanda no está abierta"}, status=400)

    # Realizar el pago y actualizar el estado de la comanda
    payment = Pagament(comanda=comanda, card_number=card_number, data_expiration=expiry_date, cvc=cvc)
    payment.save()

    comanda.estat = 'Tancat'  # Actualizar el estado de la comanda a 'Tancat'
    comanda.save()

    return Response({"status": "success", "message": "El pago se ha realizado con éxito"}, status=200)
```

### CONSULTAR ESTADO DE UNA COMANDA
Implementación del método para leer el estado de una comanda desde la base de datos.

![estat_comanda](https://github.com/lcastienc/M07_UF4_API_Store/assets/102548167/810d14c7-3279-4bb0-9c51-23f99212602f)

Codigo para ver el estado de la comanda:
```python
@api_view(['GET'])
def consultar_estat_comanda(request, comanda_id):
    try:
        comanda = Comanda.objects.get(id=comanda_id)
    except Comanda.DoesNotExist:
        return Response({"status": "error", "message": "Comanda no encontrada"}, status=404)

    return Response({"status": "success", "message": f"El estado de la comanda {comanda_id} es {comanda.estat}"}, status=200)
```
### URLS PAGAMENT
```python
urlpatterns = [
    path('pagar_comanda/', views.pagar_comanda, name='pagar_comanda'),
    path('consultar_estat_comanda/<int:comanda_id>/', views.consultar_estat_comanda, name='consultar_estat_comanda'),
]
```
### MODEL PAGAMENT
```python
class Pagament(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    data_expiration = models.CharField(max_length=7)
    cvc = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.comanda} {self.card_number} {self.data_expiration} {self.cvc}'
```
