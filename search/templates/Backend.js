const btn = document.getElementById('btn');
const text = document.getElementById('text');
let x = 0;

btn.addEventListener('click', () => {
    text.textContent = Number(text.textContent) + 1;
});