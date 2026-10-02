// Lógica del carrito: comunica con los endpoints /api/carrito/* de Flask

function actualizarBadge(count) {
    const badge = document.getElementById("cart-badge");
    if (badge) badge.textContent = count;
}

async function llamarApi(url, payload) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ error: "Error inesperado" }));
        alert(err.error || "Ocurrió un error");
        return null;
    }
    return res.json();
}

// Botones "Agregar al carrito" (catálogo y detalle de producto)
document.querySelectorAll(".btn-add[data-producto-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
        const productoId = btn.dataset.productoId;
        let cantidad = 1;
        if (btn.dataset.cantidadInput) {
            const input = document.getElementById(btn.dataset.cantidadInput);
            cantidad = parseInt(input.value, 10) || 1;
        }

        const original = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Agregando...";

        const data = await llamarApi("/api/carrito/agregar", {
            producto_id: productoId,
            cantidad: cantidad,
        });

        btn.disabled = false;
        btn.textContent = original;

        if (data && data.ok) {
            actualizarBadge(data.count);
            btn.textContent = "¡Agregado!";
            setTimeout(() => (btn.textContent = original), 1200);
        }
    });
});

// Página del carrito: cambiar cantidad y eliminar ítems
const cartBody = document.getElementById("cart-body");
if (cartBody) {
    cartBody.addEventListener("change", async (e) => {
        if (!e.target.classList.contains("cantidad-input")) return;
        const fila = e.target.closest("tr");
        const productoId = fila.dataset.productoId;
        const cantidad = parseInt(e.target.value, 10);

        const data = await llamarApi("/api/carrito/actualizar", {
            producto_id: productoId,
            cantidad: cantidad,
        });
        if (data && data.ok) {
            const precio = parseFloat(fila.querySelector(".precio-unitario").textContent.replace("$", ""));
            fila.querySelector(".subtotal").textContent = "$" + (precio * cantidad).toFixed(2);
            document.getElementById("cart-total").textContent = "$" + data.total.toFixed(2);
            actualizarBadge(data.count);
        }
    });

    cartBody.addEventListener("click", async (e) => {
        if (!e.target.classList.contains("btn-remove")) return;
        const fila = e.target.closest("tr");
        const productoId = fila.dataset.productoId;

        const data = await llamarApi("/api/carrito/eliminar", { producto_id: productoId });
        if (data && data.ok) {
            fila.remove();
            document.getElementById("cart-total").textContent = "$" + data.total.toFixed(2);
            actualizarBadge(data.count);
            if (data.count === 0) location.reload();
        }
    });
}
