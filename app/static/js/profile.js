const edit_user = document.getElementById("edit-user")
const cancel = document.getElementById("cancel-edit")
const submit_field = document.getElementById("submit-field")

const inputs_form = document.querySelectorAll(".user-form form .inpt-field input")

edit_user.addEventListener("click", () => {
    edit_user.style.display = "none"
    submit_field.style.display = "initial"

    for (let i=0; i<inputs_form.length; i++) {
        if (inputs_form[i].id != "inputEmail") {
            inputs_form[i].toggleAttribute("readonly", false)
            inputs_form[i].toggleAttribute("disabled", false)
        }
    }
})

cancel.addEventListener("click", () => {
    document.location.reload()
})

const tab_link_profile = document.getElementById("tab-link-profile")
const tab_link_adresses = document.getElementById("tab-link-adresses")

const user_form = document.getElementById("user-form")
const address_form = document.getElementById("address-form")

tab_link_profile.addEventListener("click", (e) => {
    e.preventDefault()
    user_form.style.display = "initial"
    address_form.style.display = "none"

    tab_link_profile.classList.add("active")
    tab_link_adresses.classList.remove("active")
})

tab_link_adresses.addEventListener("click", (e) => {
    e.preventDefault()
    address_form.style.display = "initial"
    user_form.style.display = "none"

    tab_link_adresses.classList.add("active")
    tab_link_profile.classList.remove("active")
})