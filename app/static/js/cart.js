async function addToCart(productId) {
    const config = {
        method: "POST",
        body: JSON.stringify({id: productId})
    }

    const item = JSON.parse(await (await fetch(`/cart/${productId}/`, config)).text());

    let cartStorage = JSON.parse(localStorage.getItem("cartStorage"));
    if (cartStorage != null) {
        if (cartStorage[item.id] == undefined) {
            cartStorage = {
                ...cartStorage,
                [item.id]: item   
            }
            cartStorage[item.id].quantity = 1;
        }
    }
    else {
        item.quantity = 1;
        cartStorage = {
            [item.id]: item
        }
    }

    localStorage.setItem("cartStorage", JSON.stringify(cartStorage));
    displayItemsNumber();
}

function countCartItems() {
    const cartStorage = JSON.parse(localStorage.getItem("cartStorage"));
    if (cartStorage) return Object.keys(cartStorage).length;
    else return 0;
}

function displayItemsNumber() {
    let count = countCartItems();
    const cartTag = document.querySelector(".cart-amount");
    cartTag.innerHTML = count;
}

document.addEventListener("DOMContentLoaded", () => {
    displayItemsNumber();
});