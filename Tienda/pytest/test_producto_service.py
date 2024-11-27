import pytest
from Tienda.models import Producto, CategoriaProducto
from Tienda.Producto.service import ProductoService

@pytest.mark.django_db
def test_listar_productos():
    # Arrange: Create mock products
    categoria = CategoriaProducto.objects.create(nombre="Electronics", descripcion="Electronic items")
    Producto.objects.create(
        nombre="Laptop", categoria=categoria, precio=1200.00, stock=10, descripcion="High-end laptop"
    )
    Producto.objects.create(
        nombre="Smartphone", categoria=categoria, precio=800.00, stock=20, descripcion="Latest smartphone"
    )
    
    # Act: Call the service method
    productos = ProductoService.listar_productos()
    
    # Assert: Verify the result
    assert len(productos) == 2
    assert productos[0]['nombre'] == "Laptop"
    assert productos[1]['nombre'] == "Smartphone"

@pytest.mark.django_db
def test_crear_producto():
    # Arrange: Create a category
    categoria = CategoriaProducto.objects.create(nombre="Home Appliances", descripcion="Appliances for home")
    data = {
        'nombre': 'Microwave',
        'categoria': categoria.id,
        'precio': 150.00,
        'stock': 5,
        'descripcion': 'Compact microwave oven'
    }
    
    # Act: Call the service method
    producto = ProductoService.crear_producto(data, None)  # Passing None as fotografia
    
    # Assert: Verify the result
    assert producto['nombre'] == 'Microwave'
    assert producto['categoria']['nombre'] == 'Home Appliances'  # Ensure category name is correct

@pytest.mark.django_db
def test_actualizar_producto():
    # Arrange: Create a product and update data
    categoria = CategoriaProducto.objects.create(nombre="Furniture", descripcion="Home furniture")
    producto = Producto.objects.create(
        nombre="Chair", categoria=categoria, precio=50.00, stock=20, descripcion="Comfortable chair"
    )
    update_data = {
        'nombre': 'Office Chair',
        'precio': 75.00,
        'stock': 15,
        'descripcion': 'Ergonomic office chair'
    }
    
    # Act: Call the service method
    updated_producto = ProductoService.actualizar_producto(producto.id, update_data)
    
    # Assert: Verify the result
    assert updated_producto['nombre'] == 'Office Chair'
    assert float(updated_producto['precio']) == 75.00  # Convert string to float for comparison
    assert updated_producto['stock'] == 15

@pytest.mark.django_db
def test_eliminar_producto():
    # Arrange: Create a product
    categoria = CategoriaProducto.objects.create(nombre="Toys", descripcion="Kids' toys")
    producto = Producto.objects.create(
        nombre="Toy Car", categoria=categoria, precio=20.00, stock=30, descripcion="Small toy car"
    )
    
    # Act: Call the service method
    result = ProductoService.eliminar_producto(producto.id)
    
    # Assert: Verify the result
    assert result["mensaje"] == "Producto eliminado correctamente"
    assert not Producto.objects.filter(id=producto.id).exists()

@pytest.mark.django_db
def test_crear_categoria_de_producto():
    # Arrange: Prepare category data
    data = {
        'nombre': 'Books',
        'descripcion': 'Various kinds of books'
    }
    
    # Act: Call the service method
    categoria = ProductoService.crear_categoria_de_producto(data)
    
    # Assert: Verify the result
    assert categoria['nombre'] == 'Books'
    assert CategoriaProducto.objects.filter(nombre='Books').exists()

@pytest.mark.django_db
def test_actualizar_categoria_de_producto():
    # Arrange: Create a category and update data
    categoria = CategoriaProducto.objects.create(nombre="Clothing", descripcion="Wearable items")
    update_data = {
        'nombre': 'Fashion',
        'descripcion': 'Trendy clothing'
    }
    
    # Act: Call the service method
    updated_categoria = ProductoService.actualizar_categoria_de_producto(categoria.id, update_data)
    
    # Assert: Verify the result
    assert updated_categoria['nombre'] == 'Fashion'
    assert updated_categoria['descripcion'] == 'Trendy clothing'

@pytest.mark.django_db
def test_eliminar_categoria_de_producto():
    # Arrange: Create a category
    categoria = CategoriaProducto.objects.create(nombre="Sports", descripcion="Sports equipment")
    
    # Act: Call the service method
    result = ProductoService.eliminar__categoria_de_producto(categoria.id)
    
    # Assert: Verify the result
    assert result["mensaje"] == "Categoría de producto eliminada correctamente"
    assert not CategoriaProducto.objects.filter(id=categoria.id).exists()

@pytest.mark.django_db
def test_listar_categorias_de_productos():
    # Arrange: Create mock categories
    CategoriaProducto.objects.create(nombre="Books", descripcion="Various kinds of books")
    CategoriaProducto.objects.create(nombre="Electronics", descripcion="Electronic items")
    
    # Act: Call the service method
    categorias = ProductoService.listar_categorias_de_productos()
    
    # Assert: Verify the result
    assert len(categorias) == 2
    assert categorias[0]['nombre'] == "Books"
    assert categorias[1]['nombre'] == "Electronics"
