(function() {
  /*Mostrar y oculatar*/ 
  document.getElementById("Button").addEventListener("click", function () {
    document.getElementById("datos_g").style.display = "none";
    document.getElementById("datos_u").style.display = "block";
  });
  document.getElementById("Button2").addEventListener("click", function () {
    document.getElementById("datos_g").style.display = "block";
    document.getElementById("datos_u").style.display = "none";
  });

  /* Campos vacios*/
  const $form = document.getElementById('form');
  const $Edad = document.getElementById('edad');
  const $name = document.getElementById('name');
  const $Colonia = document.getElementById('soValue');
  const $Fecha_nacimiento = document.getElementById('fecha_nacimiento');
  const $curp = document.getElementById('CURP');
  const $Contraseña = document.getElementById('password');
  const $Contraseña2 = document.getElementById('password2');

  $form.addEventListener('submit', function (e) {
    
    const $Sexo = document.querySelector('input[name="sexo"]:checked');
    let edad = $Edad.value;
    let nombre = String($name.value).trim();
    let colonia = String($Colonia.value).trim();
    let fecha_nacimiento = String($Fecha_nacimiento.value).trim();
    let CURP = String($curp.value).trim();
    let contraseña = String($Contraseña.value).trim();
    let contraseña2 = String($Contraseña2.value).trim();


      if (nombre.length === 0 || colonia.length === 0 || edad === "" || !$Sexo ||fecha_nacimiento === '' ) {
          e.preventDefault();
          document.getElementById("datos_u").style.display = "none";
          document.getElementById("datos_g").style.display = "block";
          alert("No puede haber campos vacíos, por favor llene todos los campos");
      }
      else if (CURP.length > 18 || CURP.length < 18) {
        e.preventDefault();
        document.getElementById("datos_u").style.display = "none";
        document.getElementById("datos_g").style.display = "block";
        alert("La CURP debe tener 18 caracteres");
      }
      else if (contraseña != contraseña2){
        e.preventDefault();
        alert("Las contraseñas no son iguales");
      }
  });
})();

document.addEventListener("DOMContentLoaded", function () {
  const fechaInput = document.getElementById("fecha_nacimiento");
  const edadInput = document.getElementById("edad");

  fechaInput.addEventListener("change", function () {
    const inputFecha = fechaInput.value;
    if (!inputFecha) return;

    const fechaNac = new Date(inputFecha);
    const hoy = new Date();

    if (fechaNac > hoy) {
      alert("La fecha no puede ser futura");
      edadInput.style.display = "none";
      edadInput.value = '';
      return;
    }

    let edad = hoy.getFullYear() - fechaNac.getFullYear();
    const mes = hoy.getMonth() - fechaNac.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
      edad--;
    }

    edadInput.value = edad;
  });
});