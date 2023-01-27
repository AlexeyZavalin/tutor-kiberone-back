"use strict";

function initModalBtns() {
    let btnsModal = document.querySelectorAll('.btn_modal');

    btnsModal.forEach(function (element) {
        element.addEventListener('click', function (event) {
            let modal = document.getElementById(element.dataset['modalId']);
            modal.style.display = "block";
        })
    })
}

initModalBtns();

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
        const info = createStudentForm.querySelector('#id_info').value
        const formData = {
            'name': name,
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

function initCheckboxes() {
    let studentCheckBoxes = document.querySelectorAll('.student-checkbox')
    let studentCheckAll = document.getElementById('student-check-all')
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
}

function handleCheckBox(checked, value, input) {
    if (checked) {
        studentIds.add(value)
    } else {
        studentIds.delete(value)
    }
    input.value = Array.from(studentIds).join(',')
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

function initCustomKiberonsBtns() {
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

function init() {
    initModalBtns();
    initCheckboxes();
    initFairBtns();
    initCustomKiberonsBtns();
}

init();

function initSorts() {
    const sorts = document.querySelectorAll('.sort_by');
    if (sorts) {
       sorts.forEach(function (element) {
            element.addEventListener('click', function (e) {
                const sortField = e.target.dataset.sortField;
                const sortOrder = e.target.dataset.sortOrder;
                const url = `${e.target.dataset['sortUrl']}?sort_by=${sortField}&sort_order=${sortOrder}`;
                let container = document.querySelector(e.target.dataset.sortContainer)
                const loadingContainer = document.querySelector(e.target.dataset.loadingContainer);
                const loader = loadingContainer.querySelector('.loading');
                loader.classList.add('loading_active');
                getData(url, {})
                .then(data => {
                    document.getElementById('student_list').innerHTML = data.markup
                    if (sortOrder === 'DESC') {
                        element.dataset.sortOrder = 'ASC';
                        element.classList.add('sort_by_asc');
                        element.classList.remove('sort_by_desc');
                        element.title = 'Сортировать по возрастанию';
                    } else {
                        element.dataset.sortOrder = 'DESC';
                        element.classList.remove('sort_by_asc');
                        element.classList.add('sort_by_desc');
                        element.title = 'Сортировать по убыванию';
                    }
                    init();
                    loader.classList.remove('loading_active');
                })
            })
        })
    }
}

initSorts();

function initFilterGroup() {
    const filters = document.querySelectorAll('.visited-filter__item');
    if (filters) {
       filters.forEach(function (element) {
            element.addEventListener('click', function (e) {
                const filterValue = e.target.dataset.visited;
                const url = `${e.target.dataset['sortUrl']}?visited_today=${filterValue}`;
                const loadingContainer = document.querySelector(e.target.dataset.loadingContainer);
                const loader = loadingContainer.querySelector('.loading');
                loader.classList.add('loading_active');
                getData(url, {})
                .then(data => {
                    document.getElementById('student_list').innerHTML = data.markup;
                    element.classList.add('visited-filter__item_active');
                    if (filterValue === '1') {
                        element.previousElementSibling.classList.remove('visited-filter__item_active');
                    } else {
                        element.nextElementSibling.classList.remove('visited-filter__item_active');
                    }
                    init();
                    loader.classList.remove('loading_active');
                })
            })
        })
    }
}

initFilterGroup()

// show password
const showPasswordBtn = document.querySelector('.show_password');
if (showPasswordBtn) {
    showPasswordBtn.addEventListener('click', function (e) {
        const passwordInput = showPasswordBtn.parentNode.querySelector('[name="password"]');
        const img = showPasswordBtn.querySelector('img')
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            showPasswordBtn.title = showPasswordBtn.dataset.hideText;
            img.src = showPasswordBtn.dataset.hidePath;
        } else {
            passwordInput.type = 'password';
            showPasswordBtn.title = showPasswordBtn.dataset.showText;
            img.src = showPasswordBtn.dataset.showPath;
        }
    })
}

// переключение темы
const themeSwitcher = document.getElementById('theme-switcher')

if (themeSwitcher) {
    themeSwitcher.addEventListener('click', function (e) {
        let theme = 'dark';
        const url = themeSwitcher.dataset['url'];
        if (themeSwitcher.classList.contains('theme-switcher_light')) {
            themeSwitcher.classList.remove('theme-switcher_light');
            themeSwitcher.classList.add('theme-switcher_dark');
        } else if (themeSwitcher.classList.contains('theme-switcher_dark')) {
            themeSwitcher.classList.add('theme-switcher_light');
            themeSwitcher.classList.remove('theme-switcher_dark');
            theme = 'light';
        }
        postData(url, {'theme': theme})
            .then((data) => {
                if (data['success']) {
                    window.location.reload();
                }
            });
    })
}