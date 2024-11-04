const menuSelected = document.getElementById('menu-select');
const menuTarget = document.getElementById('menu-target');
const menuForm = document.getElementById('menu-form');


menuSelected.addEventListener('change', (e) => {
    const selected = e.target.value;
    document.getElementById('id_menu_type').value = selected;
    if (selected.endsWith('1')) {
        menuTarget.innerHTML = htmlData4Menu(menu1);
    } else if (selected.endsWith('2')) {
        menuTarget.innerHTML = htmlData4Menu(menu2);
    }
});


const menu1 = {
    menuNo: 'Menu 1',
    smackAndDip: [
        'Chicken skewer: Chicken on skewer crusted with herbs and cashew, served with oyster & basil mayo.',
    'Tacos platter: De-constructed tacos platter, masala kebab, crispy shrimp, spicy beef wrap, fish bite tempura, pilaf, meaty black sauce, cherry, cucumber, efiri emulsion and avocado'],
    soup: ['Smoked Croaker fish pepper soup', 'Chicken corn soup'],
    appetizer: ['Fish Tempura: Spicy fresh catch fish of the day fried in a light & crispy batter served with chef sauce',
    'Sticky Bourbon Chicken Taco: Sticky charcoal grilled chicken, avocado, stuffed in taco bread served with coriander and chili dip.'],
    salad: 'Loaded Prawns Kilishi Caesar Salad: Eggs, baby cos lettuce, prawn, anchovy, kilishi,  pancetta focaccia , parsley, parmesan Caesar dressing',
    main: ['Coconut grilled chicken roulade: 48 hours marinate chicken, spinach mushroom, chili mushroom sauce, coriander emulsion, coconut syrup.',
    'Braised Lamb shank: Braised lamb shank, red wine gravy, leek rosemary puree, Beef short ribs, carrot texture, rosemary jus'],
    desert: ['Coffee Caramel dark chocolate tart',
    'Creamy dark chocolate ganache', 'Nutty ice cream', 'Plantain Crumbs'],
    bread: ['Focaccia', 'Sourdough', 'Garlic bread', 'Challah'],
    sides: ['Buttering mashed potatoes', 'Cheesy garlic roasted butter potatoes',
    'Potatoes fondant', 'Creamy baby potatoes', 'OSE special fried rice', 'Spaghetti stir fry', 
    'Coriander jasmine', 'Smoked asun jollof'],
    vegetable: ['Roasted carrot ', 'Broccoli tempura', 'Sautéed mushroom', 
    'Pickled onion', 'Mixed bell pepper', 'Sautéed spinach', 'Assorted bread'],
    price: '1,500,000'

}

const menu2 = {
    menuNo: 'Menu 2',
    smackAndDip: [
        'Lamb kebab: Diced Lamb on skewer crusted with herbs cheese and pine nut, served with smoked oyster & basil mayo.',
    'Chefs platter: De-constructed tacos platter, masala kebab, crispy shrimp, spicy beef wrap, fish bite tempura, pilaf, meaty black sauce, cherry, cucumber, efiri emulsion and avocado.'],
    soup: ['Charcoal Goat meat pepper soup', 'Seafood butternut sqaush soup'],
    appetizer: ['Prawn Crispy: Spicy garri crispy PRAWN butterball coated & deep fry prawn & crunchy onion served with hoi sin mayo paprika sauce',
    'Beef Sliders: Classic version of OSE masterpiece mini burger, caramelized onion, goat cheese, roasted parmesan cream served with assorted fries, two dip'],
    salad: 'Char Grilled Chicken Salad: Chicken fillet, avocado, quail egg, cherry, Smokey ham, onion, goat cheese, cranberry dressing.',
    main: ['Char Grilled Red Snapper: Grilled full red snapper, celeriac truffle sauce, ugba salsa Verde, OSE pepper sauce',
    'Ose char chicken roast: Five spice char chicken with OSE BBQ sauce served coconut curry sauce',
    'Beef Goulash: Beef, potatoes, vegetable'],
    desert: ['Hibiscus cheesecake, Hibiscus custard, Smoked strawberry oat dust, Tuile, Homemade uyayak gelato', 'A 200ml bowl of gelato', 'Zobo syrup'],
    bread: ['Focaccia', 'Sourdough', 'Garlic bread', 'Challah'],
    sides: ['Buttering mashed potatoes', 'Cheesy garlic roasted butter potatoes',
    'Potatoes fondant', 'Creamy baby potatoes', 'OSE special fried rice', 'Spaghetti stir fry', 
    'Coriander jasmine', 'Smoked asun jollof'],
    vegetable: ['Roasted carrot ', 'Broccoli tempura', 'Sautéed mushroom', 
    'Pickled onion', 'Mixed bell pepper', 'Sautéed spinach', 'Assorted bread'],
    price: '2,100,000'

}

// Display menu
function htmlData4Menu(menu) {
    let data = `
    <h2>${menu.menuNo}</h2>
    <p class="fw-bold">Smack and Dip</p>
    <ul>
    `;
    menu.smackAndDip.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">Soup</p>
    <ul>
    `;
    menu.soup.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>`;
    data += `<p class="fw-bold">Appetizer</p>
    <ul>
    `;
    menu.appetizer.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">Salad</p>
    <ul>
    <li>${menu.salad}</li>
    </ul>
    <p class="fw-bold">Main</p>
    <ul>
    `;
    menu.main.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">DESSERT (PLATED)</p>
    <ul>`;
    menu.desert.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">Bread</p>
    <p class="text-muted">Pick choice of bread.</p>
    <ul>`;
    menu.bread.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">Sides</p>
    <p class="text-muted">Pick choice two of sides.</p>
    <ul>`;
    menu.sides.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p class="fw-bold">Vegetable And Others</p>
    <p class="text-muted">FOOD SERVING portion Pick choice of two.</p>`;
    data += `<ul>`;
    menu.vegetable.forEach(item => {
        data += `<li>${item}</li>`;
    });
    data += `</ul>
    <p><span class="fw-bold">Price:</span> ₦${menu.price}</p>
    <p><span class="fw-bold">20% Service Charge</p>
    `;

    return data;
}

window.onload = () => {
    menuTarget.innerHTML = htmlData4Menu(menu1);
}


const header = `
    <div class="row" >
        <div class="col">
            <div>
                <img src="https://i.ibb.co/Kxcr0bY/black-logo.png" alt="Ose Logo" width="120px" style="{margin: 5px;}" class="logo text-center">
                <ul class="list-unstyled">
                    <li style="font-size: 20px; "><b>Contact:</b></li>
                    <li>bookings@osedining.com.ng</li>
                    <li>+234 816 747 6771</li>
                </ul>
            </div>

            <div class="text-center">
            <h3>Casual Dining</h3>
            <p>Menu is designed for a minimum of 8 (eight) guests</p>
            </div>
        </div>
    </div>
`

const footer = `
<br><br>
<p>All payment should be made in favour of:</p>
<ul class="list-unstyled">
    <li>Account Name:</li>
    <li style="font-size: 20px; "><b>Ehis Foods</b></li>
    <li>Account Number:</li>
    <li style="font-size: 20px; "><b>0122941028</b></li>
</ul>
<p>Thanks for your patronage</p>
`

const cmd = document.getElementById('cmd');
// const agree = document.getElementById('agreement').innerHTML;
cmd.addEventListener('click', (e) => {
    const data = document.getElementById('menu-target').innerHTML;
    document.body.innerHTML = header + data + footer;
    // document.body.innerHTML = data;
    window.print();
})