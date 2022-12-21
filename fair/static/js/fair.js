let products = new Set();

let container = document.querySelector('.fair__souvenirs');

class Order {
    constructor(studentId, balance) {
        this.studentId = studentId;
        this.balance = balance;
        this.cart = new Cart();
    }

    addProductToOrder(item) {
        if (this.canAdd(item.price)) {
            item.in_cart = true;
            this.balance -= item.price;
            products.delete(item);
            this.cart.addProduct(item);
            this.cart.renderCart('.fair__cart');
        }
    }

    removeProductFromOrder(item) {
        item.in_cart = false;
        this.balance += item.price;
        products.add(item);
        this.cart.removeProduct(item);
        this.cart.renderCart('.fair__cart');
    }

    canAdd(price) {
        return this.balance - price >= 0;
    }


}

class Item {
    constructor(id, price, name, img) {
        this.id = id;
        this.price = price;
        this.name = name;
        this.img = img;
        this.in_cart = false;
    }

    createItemMarkup() {
        const itemMarkup = document.createElement('div');
        let classes = ['souvenir'];
        if (this.in_cart) classes.push('souvenir_in-cart');
        itemMarkup.classList.add(...classes);
        itemMarkup.id = `souvenir-${this.id}`;
        const imgWrapper = document.createElement('div');
        imgWrapper.classList.add('souvenir__img-wrapper');
        const img = document.createElement('img');
        img.classList.add('souvenir__img');
        img.src = this.img;
        img.alt = this.name;
        imgWrapper.appendChild(img);
        const name = document.createElement('div');
        name.classList.add('souvenir__name');
        name.innerText = this.name;
        const price = document.createElement('div');
        price.classList.add('souvenir__price');
        price.innerText = `${this.price}к`;
        let btn = this.createBtn(this.in_cart);
        itemMarkup.append(imgWrapper, name, price, btn);
        btn.addEventListener('click', () => {
            this.clickHandler(this);
            renderProducts(products, container);
        })
        return itemMarkup;
    }

    createBtn(in_cart = false) {
        const btn = document.createElement('button');
        let classes = ['btn'];
        if (in_cart) {
            classes.push('btn_red', 'remove_from_cart');
            btn.innerText = 'Удалить';
        } else {
            classes.push('btn_blue', 'add_to_cart');
            btn.innerText = 'Добавить';
        }
        btn.classList.add(...classes);
        return btn;
    }

    clickHandler(product) {
        if (!product.in_cart) {
            order.addProductToOrder(product);
        } else {
            order.removeProductFromOrder(product);
        }
    }
}

class Cart {
    constructor() {
        this.items = new Set();
        this.total = 0;
    }

    addProduct(item) {
        this.items.add(item);
        this.total += item.price;
    }

    removeProduct(item) {
        this.items.delete(item);
        this.total -= item.price;
    }

    renderCart(selector) {
        let container = document.querySelector(selector);
        container.innerHTML = '';
        const list = document.createElement('div');
        list.classList.add('souvenirs');
        for (let item of this.items) {
            list.appendChild(item.createItemMarkup());
        }
        container.appendChild(list);
        if (this.items.size > 0) {
            const confirmBtn = this.confirmBtn();
            container.appendChild(confirmBtn);
            confirmBtn.addEventListener('click', this.confirm)
        }
    }

    confirmBtn() {
        const btn = document.createElement('button');
        btn.classList.add('btn', 'btn_yellow', 'btn_big', 'btn_confirm_order');
        btn.innerText = 'Оформить';
        return btn;
    }

    confirm(e) {
        const confirmUrl = window.fairCreateUrl;
        let orderData = order
        orderData.items = Array.from(order.cart.items)
        postData(confirmUrl, orderData)
            .then((data) => {
                if (data['success']) {
                    if (data['redirect']) {
                        window.location = data['redirect']
                    }
                }
            });
    }
}

let cart = new Cart();
let order = new Order();

function initFairBtns() {
    products = new Set();
    let fairBtns = document.querySelectorAll('.btn_fair')
    order = new Order();
    if (fairBtns.length) {
        const cartContainer = document.querySelector('.fair__cart');
        fairBtns.forEach(function (element) {
            element.addEventListener('click', function (event) {
                products = new Set();
                document.querySelector('.fair__title').textContent = element.dataset['studentName'];
                document.querySelector('.fair__subtitle').textContent = element.dataset['kiberons'] + 'к';
                cartContainer.innerHTML = '';
                const url = element.dataset['url'] + '?id=' + element.dataset['studentId'];
                getData(url).then(data => {
                    let items = JSON.parse(data);
                    for (const item of items) {
                        products.add(new Item(Number(item.pk), Number(item.fields.price), item.fields.name, item.fields.image))
                    }
                    renderProducts(products, container);
                    cart = new Cart();
                    order = new Order(Number(element.dataset['studentId']), Number(element.dataset['kiberons']));
                });
            })
        })
    }
}

initFairBtns()

function renderProducts(list, container) {
    container.innerHTML = '';
    let listItems = document.createElement('div');
    listItems.classList.add('souvenirs');
    for (let item of list) {
        listItems.appendChild(item.createItemMarkup());
    }
    if (list.size === 0) {
        listItems.innerText = 'Не хватает киберонов или товары закончились';
    }
    container.appendChild(listItems);
}