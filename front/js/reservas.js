window.onload = function () {
    //aca, cambias la parte de abajo, creas un fetch y despues le pasas los datos de la respuesta json 
    //a la funcion crear vista mesas.
    datos = {
        "mesas": [
            {
                "Disponibilidad": 0,
                "MesaID": 21,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 22,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 23,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 24,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 25,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 26,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 27,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 28,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 29,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 30,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 31,
                "RestauranteID": "RestauranteDondePericos"
            },
            {
                "Disponibilidad": 0,
                "MesaID": 32,
                "RestauranteID": "RestauranteDondePericos"
            }
        ]
    }
    //Para acceder al id del Restaurante es así
    let usuario = localStorage.getItem("currentUser")
    //id = usuario.infousuario.RestauranteID
    // o en su caso, si es por ID de usuario
    //id = usuario.infousuario.UsuarioID
    //descomenta, dependiendo de lo que tu endpoint pide.
    crearVistaMesas(datos);
};
function crearVistaMesas(datos) {
    let string;
    $("#reservas").hide();
    string = `<div class="container text-center"> <div class="row row-cols-4">`;

    // Loop through mesa data and add to the string
    datos.mesas.forEach(mesa => {
        string += `<div class="col">
            
            <div class="card">
                <img src="assets/icon-mesa-consumidor.png" class="card-img-top" alt="...">
                <div class="card-body">
                    <h5 class="card-title">${"Mesa " + mesa.MesaID}</h5>
                    <p class="card-text">${mesa.Disponibilidad == 0 ? "Disponible" : "Ocupada"}</p>
                    <a href="#" onclick="cambiarDisponibilidad(${mesa.MesaID}, ${mesa.Disponibilidad});" class="btn btn-primary">Cambiar estado</a>
                </div>
            </div>
        </div>`; // Example: Displaying MesaID
    });

    string += `</div></div>`;

    // Append the string to the reservas element
    $("#reservas").append(string);
    $("#reservas").slideDown();
};
function cambiarDisponibilidad(mesa, Disponibilidad) {
    Swal.fire({
        title: 'Cambiar estado',
        input: 'select',
        inputOptions: {
            0: 'Disponible',
            1: 'Ocupado',
        },
        inputPlaceholder: 'Selecciona un estado',
        showCancelButton: false,
        confirmButtonText: "Cambiar estado",
        confirmButtonColor: '#4CAF50',
        inputValidator: (value) => {
            console.log(value)
            if(value =="") {
                Swal.fire("selecciona un valor")
            } else {
                let valor = parseInt(value)
                //aqui metes el fetch donde le envias los datos al servidor, en el json de respuesta, 
                //muestras el error o mensaje de exito al usuario, limpias el contenido de #reservas, con esto:
                document.querySelector("#reservas").innerHTML =""
                //mandas otro fetch (para acutalizar las mesas), y actualizas la pagina, como hice al principio 
            }
        }
    })
}
