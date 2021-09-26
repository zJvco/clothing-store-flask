const edit_user = document.getElementById("edit-user")
const cancel = document.getElementById("cancel-edit")
const submit_field = document.getElementById("submit-field")

const inputs_form = document.querySelectorAll(".user-form form .inpt-field input")

function toggleEditInputAttributes(bool) {
    for (let i=0; i<inputs_form.length; i++) {
        inputs_form[i].toggleAttribute("readonly", bool)
        inputs_form[i].toggleAttribute("disabled", bool)
    }
}

edit_user.addEventListener("click", () => {
    edit_user.style.display = "none"
    submit_field.style.display = "initial"

    toggleEditInputAttributes(false)
})

cancel.addEventListener("click", () => {
    submit_field.style.display = "none"
    edit_user.style.display = "initial"

    toggleEditInputAttributes(true)
})