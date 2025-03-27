const $name = document.getElementById('name');
const $form = document.getElementById('form');
const $edad = document.getElementById('edad');

$form.addEventListener('submit', function (e) {
    let nombre = String($name.value).trim();
    let edad = Number($edad.value); // Convertir la edad a número

    if (nombre.length === 0) {
        e.preventDefault();
        alert("El nombre no puede ir vacío");
    }

    if (edad < 0 || isNaN(edad)) { // Validar que la edad no sea negativa y que sea un número válido
        e.preventDefault();
        alert("El campo de edad no puede ser negativo");
    }
});