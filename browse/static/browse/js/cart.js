// ************************************************
// cart.js
// Shopping Cart API
// ************************************************

var shoppingCart = (function () {
    // =============================
    // Private methods and propeties
    // =============================
    cart = [];

    // Constructor
    function Item(id, price, count, name, rest_id, buy_n, get_n) {
        this.id = id;
        this.price = price;
        this.count = count;
        this.name = name;
        this.rest_id = rest_id;
        this.buy_n = buy_n;
        this.get_n = get_n;
    }

    // Save cart
    function saveCart() {
        localStorage.setItem('shoppingCart', JSON.stringify(cart));
    }

    // Load cart
    function loadCart() {
        cart = JSON.parse(localStorage.getItem('shoppingCart'));
    }

    if (localStorage.getItem("shoppingCart") != null) {
        loadCart();
    }


    // =============================
    // Public methods and propeties
    // =============================
    var obj = {};

    // Add to cart
    obj.addItemToCart = function (id, price, count, name, rest_id, buy_n = 1, get_n = 0) {

        for (var item in cart) {
            if (cart[item].id === id) {
                cart[item].count++;
                saveCart();
                return;
            }
        }
        cart.push(new Item(id, price, count, name, rest_id, buy_n, get_n));
        saveCart();
        return true;
    };
    // Set count from item
    obj.setCountForItem = function (id, count) {
        for (var i in cart) {
            if (cart[i].id === id) {
                cart[i].count = count;
                break;
            }
        }
    };
    // Remove item from cart
    obj.removeItemFromCart = function (id) {
        for (let i = 0; i < cart.length; i++) {
            if (cart[i].id === id) {
                cart[i].count--;
                if (cart[i].count === 0) {
                    cart.splice(i, 1);
                }
                break;
            }
        }
        saveCart();
    };

    // Remove all items from cart
    obj.removeItemFromCartAll = function (id) {
        for (let i = 0; i < cart.length; i++) {
            if (cart[i].id === id) {
                cart.splice(i, 1);
                break;
            }
        }
        saveCart();
    };

    // Clear cart
    obj.clearCart = function () {
        cart = [];
        saveCart();
    };

    // Count cart
    obj.totalCount = function () {
        var totalCount = 0;
        for (var item in cart) {
            totalCount += cart[item].count;
        }
        return totalCount;
    };

    // Total cart
    obj.totalCart = function () {
        var totalCart = 0;
        for (var item in cart) {
            totalCart += cart[item].price * cart[item].count;
        }
        return Number(totalCart.toFixed(2));
    };

    // List cart
    obj.listCart = function () {
        var cartCopy = [];
        for (i in cart) {
            item = cart[i];
            itemCopy = {};
            for (p in item) {
                itemCopy[p] = item[p];

            }
            itemCopy.total = Number(item.price * item.count).toFixed(2);
            cartCopy.push(itemCopy)
        }
        return cartCopy;
    };

    obj.hasItems = function () {
        return cart.length > 0;
    };
    // cart : Array
    // Item : Object/Class
    // addItemToCart : Function
    // removeItemFromCart : Function
    // removeItemFromCartAll : Function
    // clearCart : Function
    // countCart : Function
    // totalCart : Function
    // listCart : Function
    // saveCart : Function
    // loadCart : Function
    return obj;
})();


// *****************************************
// Triggers / Events
// *****************************************
// Add item
$('.add-to-cart').click(function (event) {

    event.preventDefault();
    console.log('add-to-cart');
    var rest_id = $(this).data('restaurant-id');
    var id = $(this).data('id');
    var name = $(this).data('name');
    var price = Number($(this).data('price'));
    var buy_n = Number($(this).data('offer-buy-n'));
    var get_n = Number($(this).data('offer-get-n'));
    var locInput = document.getElementById('delivery_area_srch').value;
    if (locInput == '') {
        $('#delivery_area_alert').modal();
    } else if (shoppingCart.listCart().length && shoppingCart.listCart()[0].rest_id !== rest_id) {
        $.confirm({
            title: 'Confirm!',
            content: 'You Have Items in Cart from Other Restaurant.\nREMOVE those to add current one to cart ?',
            buttons: {
                confirm: {
                    text: 'Clear',
                    btnClass: 'btn-red',
                    action: function () {
                        shoppingCart.clearCart();
                        shoppingCart.addItemToCart(id, price, 1, name, rest_id, buy_n, get_n);
                        displayCart();
                        this.close();
                        showSuccessNotification(name + " has been added to your cart.");
                    }
                },
                cancel: {
                    text: 'Cancel',
                    // btnClass: 'btn-red',
                    action: function () {
                        showWarningNotification(name + " has not been added to your cart.");
                        this.close();
                    }
                },
            }
        });
    } else {
        shoppingCart.addItemToCart(id, price, 1, name, rest_id, buy_n, get_n);
        displayCart();
        showSuccessNotification(name + " has been added to your cart.");
    }

});

// Clear items
$('.clear-cart').click(function () {
    shoppingCart.clearCart();
    displayCart();
});


function itemListJSON() {
    var arr = [];
    for (const item of shoppingCart.listCart()) {
        // arr.push({'id': item.id, 'quantity': item.count, 'price': item.price});
        arr.push({
            'id': item.id,
            'quantity': item.count + (Math.floor(item.count / item.buy_n) * item.get_n),
            'price': item.price * item.count
        });
    }
    return JSON.stringify({'pkg-list': arr});
}

function displayCart() {
    var cartArray = shoppingCart.listCart();
    var output = "";
    if (shoppingCart.totalCount() === 0) {
        output = "<h3>" + "Your Shopping cart is empty" + "<h3>";
        document.getElementById("cart-checkout-button").disabled = true;
        document.getElementById("cart-clear-button").disabled = true;
    } else {
        document.getElementById('rest-id').value = cartArray[0].rest_id;
        document.getElementById("cart-checkout-button").disabled = false;
        document.getElementById("cart-clear-button").disabled = false;
        for (var i in cartArray) {
            // console.log(cartArray[i]);
            const nfree = Math.floor(cartArray[i].count / cartArray[i].buy_n) * cartArray[i].get_n
            output += "<tr>"
                + "<td>" + cartArray[i].name + "</td>"
                + "<td>" + "( + " + nfree + " Extra)" + "</td>"
                + "<td width=150px><div class='input-group'><button class='minus-item input-group-addon btn btn-primary' data-id=" + cartArray[i].id + ">-</button>"
                + "<input type='number' class='item-count form-control' data-id='" + cartArray[i].id + "' value='" + cartArray[i].count + "'>"
                + "<button class='plus-item btn btn-primary input-group-addon' data-id=" + cartArray[i].id + ">+</button></div></td>"
                + "<td><button class='delete-item btn btn-danger' data-id=" + cartArray[i].id + ">X</button></td>"
                + "<td>(" + cartArray[i].count + "x" + cartArray[i].price + ")</td>"
                + " = "
                + "<td>" + cartArray[i].total + "</td>"
                + "</tr>";
        }
    }
    $('.show-cart').html(output);
    $('.total-cart').html(shoppingCart.totalCart());
    $('.total-count').html(shoppingCart.totalCount());
}

// Delete item button

$('.show-cart').on("click", ".delete-item", function (event) {
    var id = $(this).data('id');
    shoppingCart.removeItemFromCartAll(id);
    displayCart();
});


// -1
$('.show-cart').on("click", ".minus-item", function (event) {
    var id = $(this).data('id');
    shoppingCart.removeItemFromCart(id);
    displayCart();
});
// +1
$('.show-cart').on("click", ".plus-item", function (event) {
    var id = $(this).data('id');
    shoppingCart.addItemToCart(id);
    displayCart();
});

// Item count input
$('.show-cart').on("change", ".item-count", function (event) {
    var id = $(this).data('id');
    var count = Number($(this).val());
    shoppingCart.setCountForItem(id, count);
    displayCart();
});

displayCart();
