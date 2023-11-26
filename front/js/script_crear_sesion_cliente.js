function enviarDatos() {
    var nombre = document.getElementById("name").value;
    var apellido = document.getElementById("apellido").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("Las contraseñas no coinciden. Por favor, vuelve a ingresarlas.");
        return;
    }

    if (!nombre || !apellido || !email || !phone || !username || !password || !confirmPassword) {
        alert("Todos los campos son obligatorios. Por favor, llénelos todos.");
        return;
    }

    var datosJSON = {
        Usuario: username,
        Contrasena: password,
        TipoUsuario: "Cliente",
        DatosCliente: {
            Nombre: nombre,
            Apellido: apellido,
            Correo: email,
            Telefono: phone
        }
    };

    fetch('tu_backend_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosJSON)
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
