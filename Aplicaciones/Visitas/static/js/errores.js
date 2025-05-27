(function() {
  
    const $name = document.getElementById('name');
    const $form = document.getElementById('form');
    const $edad = document.getElementById('edad');
    
    $form.addEventListener('submit', function (e) {
        let nombre = String($name.value).trim();
    
        if (nombre.length === 0) {
            e.preventDefault();
            alert("El nombre no puede ir vacío");
        }
        
    });
})();