async function buy(id) {
    const quantity = document.getElementById("quantity").value;

    const config = {
        method: "POST",
        body: JSON.stringify([{id: id, quantity: quantity}])
    }

    res = await fetch(`/buy/`, config);
}