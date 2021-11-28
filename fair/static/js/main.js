const fairBtns = document.querySelectorAll('.btn_fair')

if (fairBtns.length) {
    fairBtns.forEach(function(element) {
        element.addEventListener('click', function (event) {
            const studentId = element.data['studnetId'];
        })
    })
}