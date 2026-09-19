const menuTiles = document.querySelectorAll('.ember-tier');
const menuTarget = document.getElementById('menu-target');
const modalBadge = document.getElementById('ember-modal-badge');

const menu1 = {
    key: 'M1',
    name: '3 Course Menu',
    firstcourse: 'Shrimp suya arancini, smoked paprika sauce, scent leaf emulsion',
    secondcourse: 'Confit duck, over egusi puree, mashed sweet potatoes, uyayaka oil',
    thirdcourse: 'Zozo poached pear, whipped ginger cream, zobo gel, nutty gelato',
    price: '90,000 per guest'
};

const menu2 = {
    key: 'M2',
    name: '4 Course Menu',
    firstcourse: 'Deli beef suya crostini',
    secondcourse: 'Avocado mousse, cassava salad, palm vinaigrette, smoked ugba aioli',
    thirdcourse: 'Pan seared seabass, plantain gnocchi, creamy banga gravy',
    fourthcourse: 'Spiced dark chocolate mango tart, pistachio gelato',
    price: '140,000 per guest'
};

const menu3 = {
    key: 'M3',
    name: '5 Course Menu',
    firstcourse: 'Smoked black snapper pepper soup consommé, iru brioche',
    secondcourse: 'Charred prawn, jollof risotto, spicy flaky plantain tuile',
    thirdcourse: 'Braised ehuru tozo, smoked asaro mash, coriander emulsion, amoriri gravy',
    fourthcourse: 'Lemon avo sorbet',
    fifthcourse: 'Kuli crumb, zobo caramel, trio gelato, chocolate mousse, zobo tuile',
    price: '220,000 per guest'
};

const menus = { M1: menu1, M2: menu2, M3: menu3 };

const courseLabels = ['First Course', 'Second Course', 'Third Course', 'Fourth Course', 'Fifth Course'];
const courseKeys = ['firstcourse', 'secondcourse', 'thirdcourse', 'fourthcourse', 'fifthcourse'];

function courseRow(index, label, dish) {
    return `
        <div class="ember-course">
            <div class="ember-course__num">0${index + 1}</div>
            <div>
                <div class="ember-course__label">${label}</div>
                <div class="ember-course__dish">${dish}</div>
            </div>
        </div>
    `;
}

function renderMenu(menu) {
    let rows = '';
    courseKeys.forEach((key, index) => {
        if (menu[key]) {
            rows += courseRow(index, courseLabels[index], menu[key]);
        }
    });

    return `
        <div class="ember-card__head">
            <h2 class="ember-card__title">${menu.name}</h2>
            <div class="ember-card__badge">&#8358;${menu.price}</div>
        </div>
        <div class="ember-card__body">
            ${rows}
        </div>
    `;
}

const invoiceLink = document.getElementById('cmd');

function selectMenu(key) {
    const menu = menus[key];

    menuTiles.forEach((tile) => {
        tile.classList.toggle('active', tile.dataset.menu === key);
    });

    menuTarget.innerHTML = renderMenu(menu);
    document.getElementById('id_menu_type').value = key;
    modalBadge.innerHTML = `${menu.name} &middot; &#8358;${menu.price}`;
    invoiceLink.href = invoiceLink.href.replace(/menu=M\d/, `menu=${key}`);
}

menuTiles.forEach((tile) => {
    tile.addEventListener('click', () => selectMenu(tile.dataset.menu));
});

window.onload = () => {
    selectMenu('M1');
}
