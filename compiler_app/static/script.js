const run = document.getElementById('run');
const input = document.getElementById('input');
const output = document.getElementById('output');

const socket = io({ autoConnect: false });

socket.connect();
socket.on('connect', () => {
  socket.emit('connection', { data: 'I\'m connected!' });
});

run.addEventListener('click', () => {
  output.innerText = '';

  const code = document.getElementById('code').value;
  socket.emit('code_submitted', code);
});

input.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    const value = input.value;

    input.value = '';
    input.style.display = 'none';
    output.innerText += ` ${value}\n`;

    socket.emit('input_value', value);
  }
});

socket.on('get_input', () => {
  input.style.display = 'block';
});

socket.on('code_output', (data) => {
  output.innerText += data.output;
});

socket.on('code_execution_complete', (data) => {
  output.innerText += `\n\n\n === ${data.status} ===`;
});
