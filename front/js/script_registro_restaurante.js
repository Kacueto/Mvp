function enviarDatosRestaurante() {
    var usuarioRestaurante = document.getElementById("usuario").value;
    var contrasenaRestaurante = document.getElementById("contrasena").value;
    var verificarContrasenaRestaurante = document.getElementById("verificarContrasena").value;
    var nombreRestaurante = document.getElementById("nombre").value;
    var direccionRestaurante = document.getElementById("direccion").value;
    var telefonoRestaurante = document.getElementById("telefono").value;
    var mesasRestaurante = document.getElementById("mesas").value;

    // Verificar que todos los campos estén llenos
    if (!usuarioRestaurante || !contrasenaRestaurante || !verificarContrasenaRestaurante || !nombreRestaurante || !direccionRestaurante || !telefonoRestaurante || !mesasRestaurante) {
        alert("Todos los campos son obligatorios. Por favor, llénelos todos.");
        return;
    }

    // Verificar que las contraseñas coincidan
    if (contrasenaRestaurante !== verificarContrasenaRestaurante) {
        alert("Las contraseñas no coinciden. Por favor, vuelve a ingresarlas.");
        return;
    }

    var datosJSONRestaurante = {
        Usuario: usuarioRestaurante,
        Contrasena: contrasenaRestaurante,
        TipoUsuario: "Restaurante",
        DatosRestaurante: {
            RestauranteId: nombreRestaurante,
            Direccion: direccionRestaurante,
            Telefono: telefonoRestaurante,
            CantidadDeMesas: parseInt(mesasRestaurante) // Convertir a entero
        }
    };

    fetch('http://reservalo.duckdns.org:5000/agregar_usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosJSONRestaurante)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        // Puedes agregar aquí cualquier lógica adicional que desees después de recibir la respuesta del servidor
    })
    .catch(error => {
        console.error('Error al enviar los datos al backend:', error);
    });
}