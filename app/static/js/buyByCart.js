async function buyByCart() {
    const cartStorage = JSON.parse(localStorage.getItem("cartStorage"));
    const cartStorageObj = Object.keys(cartStorage);

    let temp = []
    for (let i = 0; i < cartStorageObj.length; i++) {
        temp.push(cartStorage[cartStorageObj[i]]);
    }

    const config = {
        method: "POST",
        body: JSON.stringify(temp)
    }

    res = await fetch(`/buy/`, config);

    if (res) {
        window.location.reload();
    }
}