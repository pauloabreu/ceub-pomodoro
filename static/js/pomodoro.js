let workMinInput = document.getElementById('work-min');
let breakMinInput = document.getElementById('break-min');
let timeDisplay = document.getElementById('time-display');
let startBtn = document.getElementById('start');
let pauseBtn = document.getElementById('pause');
let resetBtn = document.getElementById('reset');
let cyclesCountEl = document.getElementById('cycles-count');

let timer = null;
let remaining = 0; // seconds
let mode = 'work';
let cycles = 0;

function formatTime(s) {
  let m = Math.floor(s/60).toString().padStart(2,'0');
  let sec = (s%60).toString().padStart(2,'0');
  return `${m}:${sec}`;
}

function updateDisplay() {
  timeDisplay.textContent = formatTime(remaining);
}

function notify(title, body) {
  if (!('Notification' in window)) return;
  if (Notification.permission === 'granted') {
    new Notification(title, { body });
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then(p => {
      if (p === 'granted') new Notification(title, { body });
    });
  }
}

function startTimer() {
  if (timer) return;
  if (remaining <= 0) {
    remaining = (mode === 'work' ? parseInt(workMinInput.value) : parseInt(breakMinInput.value)) * 60;
  }
  timer = setInterval(() => {
    remaining -= 1;
    updateDisplay();
    if (remaining <= 0) {
      clearInterval(timer); timer = null;
      if (mode === 'work') {
        cycles += 1; cyclesCountEl.textContent = cycles;
        notify('Pomodoro', 'Período de trabalho finalizado! Hora de pausar.');
        mode = 'break';
      } else {
        notify('Pomodoro', 'Pausa finalizada! De volta ao trabalho.');
        mode = 'work';
      }
      remaining = (mode === 'work' ? parseInt(workMinInput.value) : parseInt(breakMinInput.value)) * 60;
      updateDisplay();
    }
  }, 1000);
}

startBtn.addEventListener('click', startTimer);
pauseBtn.addEventListener('click', () => { if (timer) { clearInterval(timer); timer = null; } });
resetBtn.addEventListener('click', () => { if (timer) { clearInterval(timer); timer = null; } mode = 'work'; remaining = parseInt(workMinInput.value) * 60; updateDisplay(); });

remaining = parseInt(workMinInput.value) * 60;
updateDisplay();
