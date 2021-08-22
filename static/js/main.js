"use strict";

let removeFormGroupId = document.getElementById('id_group_id');

let btnsModal = document.querySelectorAll('.btn_modal');

btnsModal.forEach(function (element) {
    element.addEventListener('click', function (event) {
        const groupId = element.dataset['groupId'];
        let removeModal = document.getElementById(element.dataset['modalId']);
        removeModal.style.display = "block";
        removeFormGroupId.value = groupId;
    })
})

let closeBtns = document.querySelectorAll('.close');

closeBtns.forEach(function (element) {
    element.addEventListener('click', function (event) {
        const modalId = element.dataset['closeModalId'];
        document.getElementById(modalId).style.display = "none";
        removeFormGroupId.value = null;
    })
})

let modals = document.querySelectorAll('.modal');

window.onclick = function (event) {
    modals.forEach(function (element) {
        if (event.target === element) {
            element.style.display = "none";
            removeFormGroupId.value = null;
        }
    })
}

async function postData(url = '', data = {}) {
    const csrftoken = getCookie('csrftoken')
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

// удаление группы
let removeGroupForm = document.getElementById('removeGroupForm');

if (removeGroupForm) {
    removeGroupForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (removeGroupForm.querySelector('.form_errors')) {
            removeGroupForm.querySelector('.form_errors').remove()
        }
        const url = removeGroupForm.dataset['action']
        const groupId = removeGroupForm.querySelector('#id_group_id').value
        const password = removeGroupForm.querySelector('#id_password').value
        postData(url, {'group_id': groupId, 'password': password})
            .then((data) => {
                if (data['success']) {
                    document.querySelector('#group-row-' + groupId).remove();
                } else {
                    let errorSpan = document.createElement('div')
                    errorSpan.textContent = data['message']
                    errorSpan.classList.add('form_errors')
                    const btn = removeGroupForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}

// создание группы
let createGroupForm = document.getElementById('createGroupForm');

if (createGroupForm) {
    createGroupForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (createGroupForm.querySelector('.form_errors')) {
            createGroupForm.querySelector('.form_errors').remove()
        }
        const url = createGroupForm.dataset['action']
        const time = createGroupForm.querySelector('#id_time').value
        const dayOfWeek = createGroupForm.querySelector('#id_day_of_week').value
        const location = createGroupForm.querySelector('#id_location').value
        const formData = {
            'location': location,
            'time': time,
            'day_of_week': dayOfWeek
        }
        postData(url, formData)
            .then((data) => {
                if (data['success']) {
                    if (data['redirect']) {
                        window.location = data['redirect']
                    }
                } else {
                    let errorSpan = document.createElement('div')
                    errorSpan.textContent = data['message']
                    errorSpan.classList.add('form_errors')
                    const btn = createGroupForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}