const updateButtons = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function () {
        const product_id = this.dataset.product
        const action = this.dataset.action

        console.log('product_id:', product_id, 'action:', action)
        console.log('USER: ', user)

        if (user === 'AnonymousUser') {
            addCookieItem(product_id, action)
        } else {
            updateUserOrder(product_id, action)
        }
    })
}

function updateUserOrder(product_id, action) {
    console.log('User is authenticated, sending data...')

        const url = '/shop/update_item'

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'product_id': product_id, 'action': action})
        }).then((response) => {
            return response.json();
        }).then((data) => {
            location.reload()
        });
}

function addCookieItem(product_id, action) {
    console.log('User is not authenticated')

    if (action === 'add') {
        if (cart[product_id] === undefined) {
            cart[product_id] = {'quantity': 1}
        } else {
            cart[product_id]['quantity'] += 1
        }
    }

    if (action === 'remove') {
        cart[product_id]['quantity'] -= 1

        if (cart[product_id]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[product_id];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}
