const dropdown = document.querySelector('.dropdown')
const button_i = document.querySelector('#toggle-i')

document.querySelector('#toggle-dropdown').addEventListener('click', function(event) {
    if (dropdown.style.display == 'flex'){
        dropdown.style.display = 'None';
        button_i.classList.remove('bxs-down-arrow')
        button_i.classList.add('bxs-right-arrow')
    }
    else {
        dropdown.style.display = 'flex';
        button_i.classList.remove('bxs-right-arrow')
        button_i.classList.add('bxs-down-arrow')
    }  
});
