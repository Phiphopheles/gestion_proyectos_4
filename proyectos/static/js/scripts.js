document.addEventListener("DOMContentLoaded", function () {
    let alertas = document.querySelectorAll(".alert");
    alertas.forEach((alerta) => {
        setTimeout(() => {
            alerta.style.display = "none";
        }, 3000); // Oculta las alertas después de 3 segundos
    });
});
