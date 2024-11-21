let menubtn = document.getElementById('bar')
let bar = document.getElementById('bar-user')
let file_input = document.getElementById('smeta')
let file_name_div = document.getElementById('file-name')
let error_list = document.getElementById('error_list')
let error_list_two = document.getElementById('error_list_two')
let form_reg_part_one = document.getElementById('form-register')
let form_reg_par_two = document.getElementById('form-register-two')
if (file_input) {
    file_input.addEventListener('change', (event) => {
        const file = event.target.files
        let name_file = file[0].name
        file_name_div.textContent = 'Выбран файл: ' + 'name_file'
        file_name_div.classList.toggle('green')
        console.log('Выбран файл')
    })

}

document.addEventListener('click', function () {
    bar.classList.remove('show-bar')

})
menubtn.addEventListener('click', function () {
    bar.classList.toggle('show-bar')
    console.log("Nice")
    event.stopPropagation()
})

bar.addEventListener('click', function () {
    event.stopPropagation()
})

let token = document.querySelector("input[name='csrfmiddlewaretoken']").value;
$(document).ready(function () {
    $('#form-register').on('submit', function (event) {
        event.preventDefault();

        fetch(submit_url, {
            method: 'POST',
            headers: {
                "Content-Type": 'application/json;charset=utf-8',
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                username: $('#id_username').val(),
                password1: $('#id_password1').val(),
                email: $('#id_email').val(),
                password2: $('#id_password2').val(),
            })
        })
            .then(function (response) {
                error_list.textContent = ''
                if (response.ok) {
                    form_reg_part_one.classList.add('display-none')
                    form_reg_par_two.removeAttribute('hidden')
                } else {
                    response.json().then(data => {
                        for (let error_item in data.errors) {
                            let child_error = document.createElement('p');
                            child_error.textContent = data.errors[error_item];
                            error_list.appendChild(child_error)
                        }
                    })

                }
            })
    })
})
$(document).ready(function () {
    $('#form-register-two').on('submit', function (event) {
        event.preventDefault();

        fetch(code_url, {
            method: 'POST',
            headers: {
                "Content-Type": 'application/json;charset=utf-8',
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                code: $('#id_code').val(),
                username: $('#id_username').val(),
                email: $('#id_email').val(),
            })
        })
            .then(function (response) {
                error_list_two.textContent = ''
                if (response.ok) {
                    window.location.href = login_url
                } else {
                    response.json().then(data => {
                        for (let error_item in data.errors) {
                            let child_error = document.createElement('p');
                            child_error.textContent = data.errors[error_item];
                            error_list_two.appendChild(child_error)
                        }
                    })

                }
            })
    })
})


