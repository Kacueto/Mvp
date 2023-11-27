document.addEventListener("DOMContentLoaded", function () {
    // Obtén el formulario por su ID
    var formulario = document.querySelector("#login-form");

    formulario.addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar que el formulario se envíe normalmente

        var usuario = document.getElementById("username").value;
        var contrasena = document.getElementById("password").value;
        pedirDatos(usuario,contrasena)
        //, alla solo toca cambiar a direcciones de tu backend. 
        // la funcion pedirdatos solo le pasas user y pass.
        
    });
});
function redirUsuario(datos) {
    // crea una sesion con el usuario actual.
    localStorage.setItem('currentUser', JSON.stringify(datos))
    console.log(localStorage.getItem('currentUser'))
    let linkIngreso = datos.tipo == "restaurante"?"logueado.html":"logincliente.html"
    Swal.fire({
        title: `Bienvenido al panel! <br>`,
        html: `<a href='${linkIngreso}' class="btn btn-primary">Ir al panel</a>`,
        showCancelButton: false, 
        showConfirmButton: false,
        allowOutsideClick: false
      });
      
}
function pedirDatos(usuario, contrasena){
            // Verifica que ambos campos estén llenos
            if (!usuario || !contrasena) {
                alert("Ambos campos son obligatorios. Por favor, llénelos todos.");
                return;
            }
    
            var datosJSON = {
                Usuario: usuario,
                Contrasena: contrasena
            };
    
            // Ejemplo de cómo mostrar los datos en la consola
            console.log("Datos a enviar al backend:", datosJSON);
    
            // Envía los datos al backend
            fetch('http://localhost:5000/verificar_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datosJSON)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                redirUsuario(data)
            })
            .catch(error => {
                console.error('Error al enviar los datos al backend:', error);
                
            });
}
