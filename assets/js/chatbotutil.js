function sendChat(event) {
    const msg = document.getElementById('user_input').value;
    const data = {
        input: msg
    };

    fetch('/testchat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            document.getElementById('res_concat').textContent += result.response;
        })
        .catch(error => {
            console.error(error);
        });
}