document.addEventListener("DOMContentLoaded", function () {
    let usuario = localStorage.getItem("currentUser")
    if(usuario || usuario != "") {
        usuario = JSON.parse(usuario)
        document.querySelector("#usuario").innerHTML = usuario.infousuario.RestauranteID;
        document.querySelector("#logout").addEventListener('click', logout)
    } else {
        document.innerHTML = ""
        if(confirm("No ha ingresado, necesita ingresar al sistema?")){
            window.location.replace("iniciar_sesion.html");
        } else {
            window.location.replace("/")
        }
    }
})
function logout() {
    if(confirm("Seguro que quieres cerrar Sesion?")){
        localStorage.setItem("currentUser", "")
        window.location.replace("/");
    }
}