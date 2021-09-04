const csrftoken = getCookie('csrftoken')

async function postData(url = '', data = {}) {
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

async function getData(url = '', data = {}) {
    const response = await fetch(url, {
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data
    });
    return await response.json();
}