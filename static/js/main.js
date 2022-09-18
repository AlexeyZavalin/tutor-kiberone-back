"use strict";

let btnsModal = document.querySelectorAll('.btn_modal');

btnsModal.forEach(function (element) {
    element.addEventListener('click', function (event) {
        let modal = document.getElementById(element.dataset['modalId']);
        modal.style.display = "block";
    })
})

let closeBtns = document.querySelectorAll('.close');

closeBtns.forEach(function (element) {
    element.addEventListener('click', function (event) {
        const modalId = element.dataset['closeModalId'];
        document.getElementById(modalId).style.display = "none";
    })
})

let modals = document.querySelectorAll('.modal');

window.onclick = function (event) {
    modals.forEach(function (element) {
        if (event.target === element) {
            element.style.display = "none";
        }
    })
}

// удаление группы
let removeGroupBtns = document.querySelectorAll('.btn_group_remove')
let removeFormGroupId = document.getElementById('id_group_id');

if (removeGroupBtns) {
    removeGroupBtns.forEach(function (element) {
        element.addEventListener('click', function (event) {
            const groupId = element.dataset['groupId'];
            removeFormGroupId.value = groupId;
        })
    })
}

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
        const time = createGroupForm.querySelector('#id_available_time').value
        const dayOfWeek = createGroupForm.querySelector('#id_day_of_week').value
        const location = createGroupForm.querySelector('#id_available_location').value
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
let removeFormStudentId = document.getElementById('id_remove_student_id');
let removeStudentBtns = document.querySelectorAll('.btn_student_remove')

if (removeStudentBtns) {
    removeStudentBtns.forEach(function (element) {
        element.addEventListener('click', function (event) {
            removeFormStudentId.value = element.dataset['studentId']
            console.log(removeFormStudentId)
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
        if (removeStudentForm.querySelector('.form_success')) {
            removeStudentForm.querySelector('.form_success').remove()
        }
        const url = removeStudentForm.dataset['action']
        const studentId = removeFormStudentId.value
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

if (studentCheckBoxes.length > 0) {
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


// фильтрация записей

let regStudentName = document.getElementById('reg-student-name')

function handleRemoveReg(btns) {
    btns.forEach(function (element) {
        element.addEventListener('click', function (event) {
            const regId = element.dataset['regId']
            const url = element.dataset['url']
            const formData = {
                'reg_id': regId
            }
            postData(url, formData)
                .then((data) => {
                    if (data['success']) {
                        document.getElementById('kiberon-reg-' + regId).remove()
                    }
                })
        })
    })
}

if (regStudentName !== null) {
    console.log('test')
    regStudentName.addEventListener('input', function (event) {
        let name = event.target.value
        let url = event.target.dataset['url'] + '?name=' + name
        getData(url, {'name': name})
            .then(data => {
                document.querySelector('.kiberon-log').innerHTML = data['markup']
                let btnsRemoveReg = document.querySelectorAll('.btn_remove-reg')
                handleRemoveReg(btnsRemoveReg)
            })
    })
}

// удаление записи из журнала

let btnsRemoveReg = document.querySelectorAll('.btn_remove-reg')

if (btnsRemoveReg) {
    handleRemoveReg(btnsRemoveReg)
}

// закрыть списки сообщений
let messagesClose = document.querySelectorAll('.messages__close')

if (messagesClose) {
    messagesClose.forEach(function (element) {
        element.addEventListener('click', function (event) {
            element.parentNode.remove()
        })
    })
}

// кастомное добавление киберонов
let studnetKiberonBtns = document.querySelectorAll('.btn_student_kiberon')

let createCustomRegForm = document.getElementById('customKiberonAdd');

if (createCustomRegForm) {
    if (studnetKiberonBtns) {
        studnetKiberonBtns.forEach(function (element) {
            element.addEventListener('click', function (event) {
                document.getElementById('id_add-student_id').value = element.dataset['studentId']
            })
        })
    }

    createCustomRegForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (createCustomRegForm.querySelector('.form_errors')) {
            createCustomRegForm.querySelector('.form_errors').remove()
        }
        const url = createCustomRegForm.dataset['action']
        const achievement = createCustomRegForm.querySelector('#id_add-achievement').value
        const kiberonAmount = createCustomRegForm.querySelector('#id_add-kiberons_amount').value
        const studentId = createCustomRegForm.querySelector('#id_add-student_id').value
        const formData = {
            'kiberon_amount': kiberonAmount,
            'student_id': studentId,
            'achievement': achievement
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
                    const btn = createCustomRegForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}

// кастомное удаление киберонов
let studnetKiberonRemoveBtns = document.querySelectorAll('.btn_student_kiberon_remove')

let removeCustomKiberonForm = document.getElementById('customKiberonRemove');

if (removeCustomKiberonForm) {
    if (studnetKiberonRemoveBtns) {
        studnetKiberonRemoveBtns.forEach(function (element) {
            element.addEventListener('click', function (event) {
                document.getElementById('id_remove-student_id').value = element.dataset['studentId']
            })
        })
    }

    removeCustomKiberonForm.addEventListener('submit', function (e) {
        e.preventDefault()
        if (removeCustomKiberonForm.querySelector('.form_errors')) {
            removeCustomKiberonForm.querySelector('.form_errors').remove()
        }
        const url = removeCustomKiberonForm.dataset['action']
        const kiberonAmount = removeCustomKiberonForm.querySelector('#id_remove-kiberons_amount').value
        const studentId = removeCustomKiberonForm.querySelector('#id_remove-student_id').value
        const formData = {
            'kiberon_amount': kiberonAmount,
            'student_id': studentId
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
                    const btn = removeCustomKiberonForm.querySelector('.btn')
                    const parent = btn.parentNode
                    parent.insertBefore(errorSpan, btn)
                }
            });
    })
}

// удаляем лишние пустые списки с сообщениями
const messagesLists = document.querySelectorAll('ul.messages')

if (messagesLists.length) {
    messagesLists.forEach(function (element) {
        const messagesItems = element.querySelectorAll('li.messages__message')
        if (messagesItems.length === 0) {
            element.remove()
        }
    })
}