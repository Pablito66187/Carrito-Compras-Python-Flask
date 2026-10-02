import uuid
from flask import session
from db import query


def get_or_create_cart_id():
    """Obtiene el carrito ligado a la sesión del navegador, o crea uno nuevo."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]

    carrito = query(
        "SELECT id FROM carritos WHERE session_id = %s", (session_id,), fetchone=True
    )
    if carrito:
        return carrito["id"]

    nuevo_id = query(
        "INSERT INTO carritos (session_id) VALUES (%s)", (session_id,)
    )
    return nuevo_id


def add_item(producto_id, cantidad=1):
    carrito_id = get_or_create_cart_id()
    existente = query(
        "SELECT id, cantidad FROM carrito_items WHERE carrito_id=%s AND producto_id=%s",
        (carrito_id, producto_id),
        fetchone=True,
    )
    if existente:
        query(
            "UPDATE carrito_items SET cantidad = cantidad + %s WHERE id=%s",
            (cantidad, existente["id"]),
        )
    else:
        query(
            "INSERT INTO carrito_items (carrito_id, producto_id, cantidad) VALUES (%s, %s, %s)",
            (carrito_id, producto_id, cantidad),
        )


def update_item(producto_id, cantidad):
    carrito_id = get_or_create_cart_id()
    if cantidad <= 0:
        remove_item(producto_id)
        return
    query(
        "UPDATE carrito_items SET cantidad=%s WHERE carrito_id=%s AND producto_id=%s",
        (cantidad, carrito_id, producto_id),
    )


def remove_item(producto_id):
    carrito_id = get_or_create_cart_id()
    query(
        "DELETE FROM carrito_items WHERE carrito_id=%s AND producto_id=%s",
        (carrito_id, producto_id),
    )


def get_items():
    carrito_id = get_or_create_cart_id()
    return query(
        """
        SELECT ci.producto_id, ci.cantidad, p.nombre, p.precio, p.imagen, p.stock,
               (ci.cantidad * p.precio) AS subtotal
        FROM carrito_items ci
        JOIN productos p ON p.id = ci.producto_id
        WHERE ci.carrito_id = %s
        ORDER BY ci.id
        """,
        (carrito_id,),
    )


def get_total_and_count():
    items = get_items()
    total = sum(float(i["subtotal"]) for i in items)
    count = sum(i["cantidad"] for i in items)
    return total, count


def clear_cart():
    carrito_id = get_or_create_cart_id()
    query("DELETE FROM carrito_items WHERE carrito_id=%s", (carrito_id,))
