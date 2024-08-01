const run = document.getElementById('run');
const output = document.getElementById('output');
const clear = document.getElementById('clear');
const theme = document.getElementById('theme');
const copy = document.getElementById('copy');
const themeStyle = document.getElementById('theme-style');
let chosenTheme = localStorage.getItem('theme') || 'default';

const socket = io({ autoConnect: false });

socket.connect();
socket.on('connect', () => {
  socket.emit('connection', { data: 'I\'m connected!' });
});

socket.on('connected', (data) => {
  console.log(data.data);
});

theme.value = chosenTheme;
setThemeStyleAttribute();
setTheOutputTheme();

theme.addEventListener('change', () => {
  chosenTheme = theme.value;
  localStorage.setItem('theme', chosenTheme);
  setThemeStyleAttribute();
  location.reload();
});

function setThemeStyleAttribute() {
  themeStyle.setAttribute(
    'href',
    `https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/${chosenTheme}.min.css`
  );
}

function setTheOutputTheme() {
  switch (chosenTheme) {
    case 'default':
      output.style.color = 'black';
      output.style.backgroundColor = 'white';
      break;
    case 'yeti':
      output.style.color = 'black';
      output.style.backgroundColor = '#eceae8';
      break;
    case 'xq-light':
      output.style.color = 'black';
      output.style.backgroundColor = 'white';
      break;
    case 'duotone-light':
      output.style.color = 'black';
      output.style.backgroundColor = '#faf8f5';
      break;
    case 'bespin':
      output.style.color = 'white';
      output.style.backgroundColor = '#28211c';
      break;
    case 'ambiance':
      output.style.color = 'white';
      output.style.backgroundColor = '#202020';
      break;
    case 'juejin':
      output.style.color = 'black';
      output.style.backgroundColor = '#f8f9fa';
      break;
    case 'material-palenight':
      output.style.color = 'white';
      output.style.backgroundColor = '#292d3e';
      break;
  }
}

let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
  lineNumbers: true,
  mode: "python",
  theme: chosenTheme,
});

run.addEventListener('click', () => {
  isRunning(true);
  output.value = '';

  const code = editor.getValue();
  socket.emit('code_submitted', { 'code': code });
});

function isRunning(loading) {
  if (loading) {
    run.innerHTML = '<span class="spinner"></span>';
  } else {
    run.innerHTML = 'Run';
  }
}

let startPosition = 0;
socket.on('get_input', () => {
  startPosition = output.value.length;
  output.focus();
});

output.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    const value = output.value;
    socket.emit('input_value', { 'value': value.slice(startPosition) });
  }
});

socket.on('code_output', (data) => {
  output.value += data.output;
});

socket.on('code_execution_complete', (data) => {
  isRunning(false);
  output.value += `\n === ${data.status} ===`;
});

clear.addEventListener('click', () => {
  output.value = "";
});

copy.addEventListener('click', () => {
  copyText();
});

function copyText() {
  const textToCopy = editor.getValue();
  navigator.clipboard.writeText(textToCopy).then(() => {
    showNotification();
  }).catch(err => {
    console.error('Could not copy text: ', err);
  });
}

function showNotification() {
  const notification = document.getElementById('copy-notification');

  const buttonRect = copy.getBoundingClientRect();

  notification.style.left = `${buttonRect.left - 13}px`;
  notification.style.top = `${buttonRect.top + 50}px`;

  notification.style.display = 'block';

  setTimeout(() => {
    notification.style.display = 'none';
  }, 2000);
}
