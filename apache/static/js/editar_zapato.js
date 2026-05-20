import { getHeaders } from './headers.js';

// Inicializamos los headers y pedimos el token CSRF pasando true
const myHeaders = getHeaders(true);

// Extraer el ID del zapato desde los parámetros de la URL (?id=...)
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const id = urlParams.get('id');

// Escuchador único para cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // 1. Si hay un ID en la URL, recuperamos los datos del zapato para rellenar el formulario
    if (id) {
        obtenerDatosZapato(id);
    } else {
        alert("No se ha proporcionado un ID de zapato válido.");
        location.href = "zapatos.html";
    }

    // 2. Asociamos el evento click al botón de guardar cambios
    const btnGuardar = document.getElementById('btn-guardar');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', guardar);
    }

    // 3. Funcionalidad del menú hamburguesa (Navbar de Bulma)
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {
            const target = el.dataset.target;
            const $target = document.getElementById(target);
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    });

    // 4. Extra: Actualizar la vista previa de la foto en tiempo real si el usuario cambia la URL
    const fotoUrlInput = document.getElementById("foto_url");
    if (fotoUrlInput) {
        fotoUrlInput.addEventListener('input', (e) => {
            document.getElementById("foto_preview").src = e.target.value || '#';
        });
    }
});

function obtenerDatosZapato(id) {
    const requestOptions = {
        method: 'GET',
        headers: myHeaders
    };

    fetch("/api/zapatos/" + id, requestOptions)
        .then(response => response.json())
        .then(result => pintarZapato(result))
        .catch(error => {
            console.error('Error:', error);
            alert("Ha habido un error al recuperar los datos del zapato");
            location.href = "zapatos.html";
        });
}

function pintarZapato(zapato) {
    console.log("Datos del zapato recuperados:", zapato);

    document.getElementById("nombre").value = zapato.nombre;
    document.getElementById("descripcion").value = zapato.descripcion;
    document.getElementById("marca").value = zapato.marca;
    document.getElementById("precio").value = zapato.precio;
    document.getElementById("foto_url").value = zapato.foto;
    document.getElementById("foto_preview").src = zapato.foto || '#';
}

function guardar() {
    let nombre = document.getElementById("nombre").value;
    let descripcion = document.getElementById("descripcion").value;
    let marca = document.getElementById("marca").value;
    let precio = document.getElementById("precio").value;
    let foto = document.getElementById("foto_url").value;

    // Validación básica en el frontend
    if (!nombre || !descripcion || !marca || !precio) {
        alert("Todos los campos excepto la foto son requeridos");
        return;
    }

    // Preparamos el JSON que espera tu API de Python en el método PUT
    let datos = JSON.stringify({
        "id": id,
        "nombre": nombre,
        "descripcion": descripcion,
        "marca": marca,
        "precio": precio,
        "foto": foto
    });

    const requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: datos
    };

    console.log("Enviando actualización:", requestOptions);

    fetch("/api/zapatos/", requestOptions)
        .then(response => response.json())
        .then(result => {
            if (result.status === "OK") {
                alert("Zapato modificado correctamente");
                location.href = "zapatos.html";
            } else {
                alert("El zapato no ha podido ser modificado: " + (result.mensaje || "Error desconocido"));
            }
        })
        .catch(error => {
            console.error('Error en el PUT:', error);
            alert("Se ha producido un error y el zapato no ha podido ser modificado: " + error.message);
        });
}