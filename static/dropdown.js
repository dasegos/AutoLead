const buttons = document.querySelectorAll('.toggle-dropdown');
const dropdowns = document.querySelectorAll('.dropdown');
const toggle_i = document.querySelectorAll('.toggle-i');

buttons.forEach(n => n.addEventListener('click', onClick));

function onClick() {
    const index = Array.prototype.indexOf.call(buttons, this);
    if (dropdowns[index].classList.contains('hidden')) {
        dropdowns[index].classList.remove('hidden');
        toggle_i[index].classList.remove('bxs-down-arrow');
        toggle_i[index].classList.add('bxs-right-arrow');
    }
    else {
        dropdowns[index].classList.add('hidden');
        toggle_i[index].classList.remove('bxs-right-arrow');
        toggle_i[index].classList.add('bxs-down-arrow');
    }
}
