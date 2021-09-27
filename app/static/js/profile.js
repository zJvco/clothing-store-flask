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