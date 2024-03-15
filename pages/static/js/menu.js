const menuSelected = document.getElementById('menu-select');
const menuTarget = document.getElementById('menu-target');
const menuForm = document.getElementById('menu-form');

const menu1 = {
    name: 'Menu 1',
    menuNo: '3 Course Meal',
    firstcourse: 'Buffalo wings, seafood spring roll, spicy chicken wrap, grilled spicy prawn, Hot goat pepper soup, pepper sauce',
    secondcourse: 'Confit chicken, Linguine crème ata din din',
    thirdcourse: 'Red velvet cake, coffee chocolate mousse, hibiscus coulis, coffee gelato, agbalumo crack tuile',
    price: '600,000'
};

const menu2 = {
    name: 'Menu 2',
    menuNo: '3 Course Meal',
    firstcourse: 'Spicy butternut soup , kilichi  rice crisp  prawn ,leek sprout , garlic butter sourdough',
    secondcourse: 'Pan Seared croaker, Seafood jambalaya , smoked pepper sauce, kelewele, parsley emulsion',
    thirdcourse: 'Apple crumble , iru gelato ,butter kokoro crumbs ,white chocolate ganache',
    price: '600,000'
};

const menu3 = {
    name: 'Menu 3',
    menuNo: '4 COURSE MEAL',
    firstcourse: 'Smokey pepper soup croaker, chef seeded brioche',
    secondcourse: 'Confit duck, coriander butternut squash puree, Agor reduction, roasted mix vegetable',
    thirdcourse: 'Pan seared red snapper, carrot texture, leek truffle cream, parsley emulsion, mixed vegetable.',
    fourthcourse: 'Dark Elubo cake, Egusi mousse, vanilla gelato, garri tuile',
    price: '840,000'
};

const menu4 = {
    name: 'Menu 4',
    menuNo: '4 COURSE MEAL',
    firstcourse: 'Creamy seafood soup, gbegiri emulsion, charcoal croaker cut, chefs grissini',
    secondcourse: 'Confit chicken roulade, risotto ata din din',
    thirdcourse: 'Char grilled Brine steak, smoked potatoes mash, roasted carrot, base carrot texture, agor demi-glace',
    fourthcourse: 'Blueberries brownies slice, chocolate caramel drop, chili gelato, dudu crumbs, Odunku tuile',
    price: '840,000'
};

const menu5 = {
    name: 'Menu 5',
    menuNo: '4 COURSE MEAL',
    firstcourse: 'Spicy cream of mushroom soup, roasted quail, cheese roll',
    secondcourse: 'Sugarcane glazed halibut, bok choy, sake butter sauce, banga cream',
    thirdcourse: 'Odo Filet steak, duck fat potatoes, avocado liver mousse, demi-glace, smoke efo riro',
    fourthcourse: 'Deconstructed mango meringue parfait, gbegiri rosemary jelly, lemon cream, TTG crumbs',
    price: '1,200,000'
};

const menu6 = {
    name: 'Menu 6',
    menuNo: '4 COURSE MEAL',
    firstcourse: 'Seared scallop, char butter red snapper, cauliflower thyme puree, truffle cream, sprout',
    secondcourse: 'Chicken mushroom roulade, sweet potatoes mash, braised radicchio, leek cream, Supreme sauce',
    thirdcourse: 'Roast Lamb rack, rosemary jus, beans cream sauce, mixed roasted vegetables',
    fourthcourse: 'Black Deconstructed dankwa cheese cake, mango gelato, mixed berry compote, chili mango tuile',
    price: '1,020,000'
};


function MenuToForm(menu) {
    data = '';
    for (const [key, value] of Object.entries(menu)) {
        data += `<input type="hidden" name="${key}" value="${value}">`
    }
    console.log(data);
    return data;  
}

function htmlData3Course(menu) {
    return `
    <h2>${menu.name}</h2>
    <p>${menu.menuNo}</p>
    <table class="table table-striped">
        <tbody>
            <tr>
            <th scope="row">1</th>
            <td>First Course</td>
            <td>${menu.firstcourse}</td>
            </tr>
            <tr>
            <th scope="row">2</th>
            <td>Second Course</td>
            <td>${menu.secondcourse}</td>
            </tr>
            <tr>
            <th scope="row">3</th>
            <td>Third Course</td>
            <td>${menu.thirdcourse}</td>
            </tr>
            <tr>
            <th scope="row">Price</th>
            <td colspan="2">₦${menu.price}</td>
            </tr>
        </tbody>
        </table>
    `;
}

function htmlData4Course(menu) {
    return `
        <h2>${menu.name}</h2>
        <p>${menu.menuNo}</p>
        <table class="table table-striped">
            <tbody>
                <tr>
                    <th scope="row">1</th>
                    <td>First Course</td>
                    <td>${menu.firstcourse}</td>
                </tr>
                <tr>
                    <th scope="row">2</th>
                    <td>Second Course</td>
                    <td>${menu.secondcourse}</td>
                </tr>
                <tr>
                    <th scope="row">3</th>
                    <td>Third Course</td>
                    <td>${menu.thirdcourse}</td>
                </tr>
                <tr>
                    <th scope="row">4</th>
                    <td>Fourth Course</td>
                    <td>${menu.fourthcourse}</td>
                </tr>
                <tr>
                    <th scope="row">Price</th>
                    <td colspan="2">₦${menu.price}</td>
                </tr>
            </tbody>
            </table>
    `;
}


menuSelected.addEventListener('change', (e) => {
    const selected = e.target.value;

    if (selected.endsWith('1')) {
        menuTarget.innerHTML = htmlData3Course(menu1);
    } else if (selected.endsWith('2')) {
        menuTarget.innerHTML = htmlData3Course(menu2);
    } else if (selected.endsWith('3')) {
        menuTarget.innerHTML = htmlData4Course(menu3);
    } else if (selected.endsWith('4')) {
        menuTarget.innerHTML = htmlData4Course(menu4);
    } else if (selected.endsWith('5')) {
        menuTarget.innerHTML = htmlData4Course(menu5);
    } else if (selected.endsWith('6')) {
        menuTarget.innerHTML = htmlData4Course(menu6)
    } else if (selected.endsWith('7')) {
        menuTarget.innerHTML = `
        <h2>Menu 7</h2>
        <p>5 COURSE MEAL</p>
        <table class="table table-striped">
            <tbody>
                <tr>
                    <th scope="row">1</th>
                    <td>First Course</td>
                    <td>Smoked Prawn Avocado mold, scent raspberry vinaigrette, watercress, avocado aioli</td>
                </tr>
                <tr>
                    <th scope="row">2</th>
                    <td>Second Course</td>
                    <td>Pan Seared grouper, leek truffle cream, charred asparagus, seaweed dust, and scent leaves oil</td>
                </tr>
                <tr>
                    <th scope="row">3</th>
                    <td>Third Course</td>
                    <td>Roasted chicken, quail breast, carrot emulsion, roasted red cabbage, leek veloute</td>
                </tr>
                <tr>
                    <th scope="row">4</th>
                    <td>Fourth Course</td>
                    <td>Odo steak roast, butternut cream texture , squash terrine, date demi-glace, potatoes fondant</td>
                </tr>
                <tr>
                    <th scope="row">5</th>
                    <td>Fifth Course</td>
                    <td>Coconut panna cotta, white chocolate custard cream, ugba dark soil, coconut gelato white chocolate mousse</td>
                </tr>
                <tr>
                    <th scope="row">Price</th>
                    <td colspan="2">₦1,440,000</td>
                </tr>
            </tbody>
            </table>
        `
    }
    else {
        menuTarget.innerHTML = '';
    }

});


const header = `
    <div class="row" >
        <div class="col">
            <div>
                <img src="https://i.ibb.co/Kxcr0bY/black-logo.png" alt="Ose Logo" width="120px" style="{margin: 5px;}" class="logo text-center">
                <ul class="list-unstyled">
                    <li style="font-size: 20px; "><b>Contact:</b></li>
                    <li>booking@osedining.com</li>
                    <li>+234 816 747 6771</li>
                </ul>
            </div>

            <div class="text-center">
            <h3>Fine Dining</h3>
            <p>Menu is designed for a minimum of 10 (ten) guests</p>
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