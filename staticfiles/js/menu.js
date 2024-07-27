const menuIcon = document.getElementById('menu-icon');
const menu = document.getElementById('menu');


const changeIcon = () => {
    menuIcon.setAttribute('class', {
        'fas fa-stream': 'fa fa-times',
        'fa fa-times': 'fas fa-stream',
    }[menuIcon.getAttribute('class')]);
}

const toggleMenuVisibility = () => {
    menu.style.maxHeight = {
        '1000px': '0px',
        '0px': '1000px',
    }[menu.style.maxHeight]
 }


const executeMenuPrograms = () => {
    changeIcon();
    toggleMenuVisibility();
}
