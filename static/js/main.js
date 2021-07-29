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