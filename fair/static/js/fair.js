let fairBtns = document.querySelectorAll('.btn_fair')

if (fairBtns.length) {
    const container = document.querySelector('.fair__souvenirs');
    const cartContainer = document.querySelector('.fair__cart .souvenirs');
    fairBtns.forEach(function(element) {
        element.addEventListener('click', function (event) {
            document.querySelector('.fair__title').textContent = element.dataset['studentName'];
            document.querySelector('.fair__subtitle').textContent = element.dataset['kiberons'] + 'к';
            if (document.querySelector('.btn_confirm_order')) {
                document.querySelector('.btn_confirm_order').remove();
            }
            cartContainer.innerHTML = '';
            const url = element.dataset['url'] + '?id=' + element.dataset['studentId'];
            getData(url)
            .then(data => {
                if (data['markup']) {
                    container.innerHTML = data['markup'];
                    let order = new Order(element.dataset['studentId'], Number(element.dataset['kiberons']));
                    let addBtns = document.querySelectorAll('.add_to_cart');
                    let confirmBtn = document.createElement('button');
                        confirmBtn.classList.add('btn', 'btn_yellow', 'btn_big', 'btn_confirm_order');
                        confirmBtn.innerText = 'Оформить';
                        confirmBtn.disabled = true;
                        document.querySelector('.fair__cart').appendChild(confirmBtn);
                    if (addBtns.length) {
                        addBtns.forEach(function(btn) {
                            btn.addEventListener('click', function(e) {
                                if (order.canAdd(btn.dataset['kiberons'])) {
                                    const souvenir = document.getElementById('souvenir-' + btn.dataset['id']);
                                    let souvenirClone = souvenir.cloneNode(true);
                                    souvenir.remove();
                                    let souvenirInCart = souvenirClone.cloneNode(true);
                                    souvenirInCart.querySelector('.add_to_cart').remove();
                                    souvenirInCart.classList.add('souvenir_in-cart');
                                    const removeBtn = document.createElement('button');
                                    removeBtn.classList.add('btn', 'btn_red', 'remove_from_cart');
                                    removeBtn.innerText = 'Удалить';
                                    // souvenirInCart.appendChild(removeBtn);
                                    cartContainer.append(souvenirInCart);
                                    order.addProductToOrder(Number(btn.dataset['id']), Number(btn.dataset['kiberons']));
                                    document.querySelector('.fair__subtitle').textContent = order.balance + 'к';
                                    confirmBtn.disabled = false;
                                }
                            })
                        })
                    }
                    confirmBtn.addEventListener('click', function(e) {
                        const confirmUrl = window.fairCreateUrl;
                        let orderData = order
                        orderData.items = Array.from(order.cart.items)
                        if (order.cart.items.size > 0) {
                            postData(confirmUrl, orderData)
                                .then((data) => {
                                    if (data['success']) {
                                        if (data['redirect']) {
                                            window.location = data['redirect']
                                        }
                                    }
                                });
                        }
                    })
                }
            })
        })
    })
}

function addToCartHandler(order, btn, container) {
    if (order.canAdd(btn.dataset['kiberons'])) {
        const souvenir = document.getElementById('souvenir-' + btn.dataset['id']);
        let souvenirClone = souvenir.cloneNode(true);
        souvenir.remove();
        let souvenirInCart = souvenirClone.cloneNode(true);
        souvenirInCart.querySelector('.add_to_cart').remove();
        souvenirInCart.classList.add('souvenir_in-cart');
        const btn = document.createElement('button');
        btn.classList.add('btn', 'btn_red', 'remove_from_cart');
        btn.innerText = 'Удалить';
        souvenirInCart.appendChild(btn);
        container.append(souvenirInCart);
        order.addProductToOrder(Number(btn.dataset['id']), Number(btn.dataset['kiberons']));
        document.querySelector('.fair__subtitle').textContent = order.balance + 'к';
   }
}

function removeFromCartHandler(order, btn, container) {
    order.removeProductFromOrder(Number(btn.dataset['id']), Number(btn.dataset['kiberons']));
    const souvenir = document.getElementById('souvenir-' + btn.dataset['id']);
    let souvenirClone = souvenir.cloneNode(true);
    souvenir.remove();
    let souvenirToAdd = souvenirClone.cloneNode(true);
    container.append(souvenirToAdd);
}

class Order {
    constructor(studentId, balance) {
        this.studentId = studentId;
        this.balance = balance;
        this.cart = new Cart();
    }
    addProductToOrder(id, price) {
        if (this.canAdd(price)) {
            this.balance -= price;
            this.cart.addProduct(id, price);
        }
    }
    removeProductFromOrder(id, price) {
        this.balance += price;
        this.cart.removeProduct(id, price);
    }
    canAdd(price) {
        return this.balance - price > 0;
    }
}

class Cart {
    constructor() {
        this.items = new Set();
        this.total = 0;
    }
    addProduct(id, price) {
        this.items.add(id);
        this.total += price;
    }
    removeProduct(id, price) {
        this.items.delete(id);
        this.total -= price;
    }
}