"use strict";

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
let removeFormGroupId = document.getElementById('id_group_id');
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

// добавление студента в группу
let createStudentForm = document.getElementById('createStudentForm');

if (createStudentForm) {
    createStudentForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (createStudentForm.querySelector('.form_errors')) {
            createStudentForm.querySelector('.form_errors').remove()
        }
        const url = createStudentForm.dataset['action']
        const name = createStudentForm.querySelector('#id_name').value
        const kiberonAmount = createStudentForm.querySelector('#id_kiberon_amount').value
        const info = createStudentForm.querySelector('#id_info').value
        const formData = {
            'name': name,
            'kiberon_amount': kiberonAmount,
            'info': info
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
                    const btn = createStudentForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}

// удаление студента
let removeFormStudentId = document.getElementById('id_student_id');
let removeStudentBtns = document.querySelectorAll('.btn_student_remove')

if (removeStudentBtns) {
    removeStudentBtns.forEach(function (element) {
        element.addEventListener('click', function (event) {
            removeFormStudentId.value = element.dataset['studentId']
        })
    })
}
let removeStudentForm = document.getElementById('removeStudentForm')

if (removeStudentForm) {
    removeStudentForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (removeStudentForm.querySelector('.form_errors')) {
            removeStudentForm.querySelector('.form_errors').remove()
        }
        const url = removeStudentForm.dataset['action']
        const studentId = removeStudentForm.querySelector('#id_student_id').value
        const password = removeStudentForm.querySelector('#id_password').value
        postData(url, {'student_id': studentId, 'password': password})
            .then((data) => {
                if (data['success']) {
                    document.querySelector('#student-row-' + studentId).remove();
                    let successSpan = document.createElement('div')
                    successSpan.textContent = data['message']
                    successSpan.classList.add('form_success')
                    const btn = removeStudentForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(successSpan, btn)
                } else {
                    let errorSpan = document.createElement('div')
                    errorSpan.textContent = data['message']
                    errorSpan.classList.add('form_errors')
                    const btn = removeStudentForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}

// массовое выделение
let studentIds = new Set()

let studentCheckBoxes = document.querySelectorAll('.student-checkbox')
let studentCheckAll = document.getElementById('student-check-all')

function handleCheckBox(checked, value, input) {
    if (checked) {
        studentIds.add(value)
    } else {
        studentIds.delete(value)
    }
    input.value = Array.from(studentIds).join(',')
}

if (studentCheckBoxes) {
    let studentIdsInput = document.getElementById('id_student_ids')
    studentCheckAll.addEventListener('click', function (event) {
        studentCheckBoxes.forEach(function (element) {
            element.checked = studentCheckAll.checked
            handleCheckBox(element.checked, element.dataset['studentId'], studentIdsInput)
        })
    })
    studentCheckBoxes.forEach(function (element) {
        element.addEventListener('change', function (event) {
            handleCheckBox(element.checked, element.dataset['studentId'], studentIdsInput)
            if (!element.checked) {
                studentCheckAll.checked = false
            }
        })
    })
}