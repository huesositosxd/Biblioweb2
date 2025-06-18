const menu= document.getElementById('menu');
const sidebar = document.getElementById('sidebar');
const main = document.getElementById('main');

menu.addEventListener('click',()=>{
    sidebar.classList.toggle('menu-toggle')
    menu.classList.toggle('menu-toggle')
    main.classList.toggle('menu-toggle')
})

document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('input[name="discapacidad"]');
    const especificar = document.getElementById('discapacidad_es_container');

    radios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.value === 'si') {
                especificar.style.display = 'block';
            } else {
                especificar.style.display = 'none';
                document.getElementById('discapacidad_es').value = '';
            }
        });
    });
});