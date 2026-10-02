from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from config import Config
import db
import cart

app = Flask(__name__)
app.config.from_object(Config)

db.init_pool(app)
app.teardown_appcontext(db.close_db)


@app.context_processor
def inject_cart_count():
    try:
        _, count = cart.get_total_and_count()
    except Exception:
        count = 0
    return {"cart_count": count}


@app.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)
    if categoria_id:
        productos = db.query(
            "SELECT * FROM productos WHERE categoria_id=%s ORDER BY nombre",
            (categoria_id,),
        )
    else:
        productos = db.query("SELECT * FROM productos ORDER BY nombre")
    categorias = db.query("SELECT * FROM categorias ORDER BY nombre")
    return render_template(
        "index.html", productos=productos, categorias=categorias,
        categoria_activa=categoria_id
    )


@app.route("/producto/<int:producto_id>")
def producto_detalle(producto_id):
    producto = db.query(
        "SELECT * FROM productos WHERE id=%s", (producto_id,), fetchone=True
    )
    if not producto:
        flash("El producto no existe.", "error")
        return redirect(url_for("index"))
    return render_template("product_detail.html", producto=producto)


@app.route("/carrito")
def ver_carrito():
    items = cart.get_items()
    total, _ = cart.get_total_and_count()
    return render_template("cart.html", items=items, total=total)


# ---------- Endpoints AJAX (usados por static/js/cart.js) ----------

@app.route("/api/carrito/agregar", methods=["POST"])
def api_agregar():
    data = request.get_json(force=True)
    producto_id = int(data.get("producto_id"))
    cantidad = int(data.get("cantidad", 1))

    producto = db.query(
        "SELECT stock FROM productos WHERE id=%s", (producto_id,), fetchone=True
    )
    if not producto:
        return jsonify({"ok": False, "error": "Producto no encontrado"}), 404
    if cantidad < 1 or cantidad > producto["stock"]:
        return jsonify({"ok": False, "error": "Cantidad no disponible en stock"}), 400

    cart.add_item(producto_id, cantidad)
    total, count = cart.get_total_and_count()
    return jsonify({"ok": True, "total": total, "count": count})


@app.route("/api/carrito/actualizar", methods=["POST"])
def api_actualizar():
    data = request.get_json(force=True)
    producto_id = int(data.get("producto_id"))
    cantidad = int(data.get("cantidad"))
    cart.update_item(producto_id, cantidad)
    total, count = cart.get_total_and_count()
    return jsonify({"ok": True, "total": total, "count": count})


@app.route("/api/carrito/eliminar", methods=["POST"])
def api_eliminar():
    data = request.get_json(force=True)
    producto_id = int(data.get("producto_id"))
    cart.remove_item(producto_id)
    total, count = cart.get_total_and_count()
    return jsonify({"ok": True, "total": total, "count": count})


@app.route("/checkout", methods=["POST"])
def checkout():
    items = cart.get_items()
    if not items:
        flash("Tu carrito está vacío.", "error")
        return redirect(url_for("ver_carrito"))

    total, _ = cart.get_total_and_count()
    session_id = cart.get_or_create_cart_id()

    pedido_id = db.query(
        "INSERT INTO pedidos (session_id, total, estado) VALUES (%s, %s, 'pendiente')",
        (str(session_id), total),
    )
    for item in items:
        db.query(
            "INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario) "
            "VALUES (%s, %s, %s, %s)",
            (pedido_id, item["producto_id"], item["cantidad"], item["precio"]),
        )
        db.query(
            "UPDATE productos SET stock = stock - %s WHERE id=%s",
            (item["cantidad"], item["producto_id"]),
        )

    cart.clear_cart()
    flash(f"¡Pedido #{pedido_id} confirmado! Total: ${total:.2f}", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
