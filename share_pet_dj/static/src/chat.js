const roomName = JSON.parse(document.getElementById('room-name').textContent);
const sender = JSON.parse(document.getElementById('sender').textContent);
const sendButton = document.querySelector('#send-button');
const textArea = document.querySelector('#id_text');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    let div = document.createElement('div');
    div.className = 'message';
    div.innerHTML = data.text + '<b>' + sender + '</b>';
    document.querySelector('.chat').appendChild(div);
};

textArea.focus();
textArea.onkeyup = function(e) {
    if (e.keyCode === 13) {
        sendButton.click();
    }
};

sendButton.onclick = function(e) {
    const message = textArea.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    textArea.value = '';
};
