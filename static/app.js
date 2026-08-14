document.querySelectorAll('.step-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const done = button.classList.toggle('done');
    button.setAttribute('aria-label', done ? 'Mark step incomplete' : `Mark step ${button.textContent.trim()} complete`);
  });
});
