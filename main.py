import flet as ft
import mysql.connector

# Conexión a la base de datos MySQL
def conectar_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="lara"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Función para verificar si un celular ya existe y obtener el producto asociado
def verificar_celular_existe(celular):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT producto FROM clientes WHERE celular = %s", (celular,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado  # Devuelve el producto si existe, None si no

# Función para obtener todos los productos que un cliente ha comprado
def obtener_compras_cliente(celular):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT producto FROM clientes WHERE celular = %s", (celular,))
    productos = cursor.fetchall()
    conexion.close()
    return productos  # Devuelve la lista de productos comprados

# Función para agregar registros a la base de datos con fecha de compra
def agregar_registro_db(nombre_apellido, producto, celular):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre_apellido, producto, celular, fecha_compra) VALUES (%s, %s, %s, NOW())",
        (nombre_apellido, producto, celular)
    )
    conexion.commit()
    conexion.close()

# Función para obtener todos los registros de la base de datos, ordenados por fecha
def obtener_registros_db():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre_apellido, producto, celular, fecha_compra FROM clientes ORDER BY fecha_compra DESC")
    registros = cursor.fetchall()
    conexion.close()
    return registros

def main(page: ft.Page):
    page.title = "Registro de Clientes"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centrar horizontalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER    # Centrar verticalmente
   
    # Campos de entrada
    nombre_apellido_input = ft.TextField(label="Nombre y Apellido", width=300)
    celular_input = ft.TextField(label="Número de Celular", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    producto_input = ft.TextField(label="Qué Compró", width=300)
   
    # Función para agregar un registro
    def agregar_registro(e):
        # Obtener los valores de los campos
        nombre_apellido = nombre_apellido_input.value
        producto = producto_input.value
        celular = celular_input.value
       
        if nombre_apellido and producto and celular:
            # Verificar si el celular ya existe
            producto_existente = verificar_celular_existe(celular)
            if producto_existente:
                # Mostrar un mensaje si el celular ya está registrado, pero permitir la compra
                def mostrar_lista_compras(e):
                    productos_cliente = obtener_compras_cliente(celular)
                    lista_compras = ft.Column()
                    for producto in productos_cliente:
                        lista_compras.controls.append(ft.Text(f"Producto: {producto[0]}"))
                    lista_compras.controls.append(ft.Text(f"Datos del Cliente: {nombre_apellido} - Celular: {celular}"))
                    page.dialog = ft.AlertDialog(
                        title=ft.Text("Historial de Compras"),
                        content=lista_compras,
                        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())],
                    )
                    page.dialog.open = True
                    page.update()
               
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Advertencia"),
                    content=ft.Text(f"Este usuario ya compró: {producto_existente[0]}."),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: page.dialog.close()),
                        ft.TextButton("Lista", on_click=mostrar_lista_compras)
                    ],
                )
                page.dialog.open = True
                page.update()

            # Agregar el registro a la base de datos
            agregar_registro_db(nombre_apellido, producto, celular)
            # Limpiar los campos de entrada
            nombre_apellido_input.value = ""
            producto_input.value = ""
            celular_input.value = ""
            page.update()

    # Botón para agregar el registro
    agregar_button = ft.ElevatedButton(
        text="Agregar Registro",
        on_click=agregar_registro,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#ff6f91",  # Color rosado
            shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
        )
    )
   
    # Función para mostrar registros
    def mostrar_registros(e):
        registros = obtener_registros_db()
        registros_column = ft.Column()
       
        # Crear un contenedor con los registros
        for reg in registros:
            fecha_formateada = reg[3].strftime("%d/%m/%Y %H:%M:%S")
            registros_column.controls.append(
                ft.Text(f"{reg[0]} - {reg[1]} - {reg[2]} - {fecha_formateada}")
            )
       
        # Crear una nueva página con los registros
        page.dialog = ft.AlertDialog(
            title=ft.Text("Registros de Clientes"),
            content=registros_column,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())],
        )
        page.dialog.open = True
        page.update()

    # Botón para ver los registros
    mostrar_registros_button = ft.ElevatedButton(
        text="Ver Registros",
        on_click=mostrar_registros,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#ff6f91",  # Color rosado
            shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
        )
    )

    # Diseño de la página principal
    page.add(
        ft.Column(
            controls=[
                nombre_apellido_input,
                celular_input,  # Cambié el orden aquí
                producto_input,
                agregar_button,
                mostrar_registros_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )


    ft.Text(
                "Bienvenidos a la página oficial de la distribuidora Cobra",
                size=40,  # Tamaño del texto
                weight=ft.FontWeight.BOLD,  # Hacer el texto en negrita
                color=ft.colors.BLUE,  # Color del texto
            ),
# Ejecutar la aplicación
ft.app(target=main)
