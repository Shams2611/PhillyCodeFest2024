function sendRonald() {
    const msg = document.getElementById('chatInp').value;
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
            document.getElementById('chatResponse').textContent = result.response;
        })
        .catch(error => {
            console.error(error);
        });
}