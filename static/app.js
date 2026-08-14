document.querySelectorAll('.step-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const done = button.classList.toggle('done');
    button.setAttribute('aria-label', done ? 'Mark step incomplete' : `Mark step ${button.textContent.trim()} complete`);
  });
});


// Static catalogue filtering for the offline HTML export.
const filterForm = document.querySelector('.filters');
if (filterForm) {
  const cards = [...document.querySelectorAll('.recipe-card')];
  const resultLine = document.querySelector('.results-line');
  const params = new URLSearchParams(window.location.search);
  const queryInput = filterForm.querySelector('[name="q"]');
  const cuisineInput = filterForm.querySelector('[name="cuisine"]');
  const speedInput = filterForm.querySelector('[name="speed"]');
  if (params.get('q')) queryInput.value = params.get('q');

  const applyFilters = () => {
    const query = queryInput.value.trim().toLowerCase();
    const cuisine = cuisineInput.value.toLowerCase();
    const under30 = speedInput.value === 'under-30';
    let shown = 0;
    cards.forEach((card) => {
      const text = card.textContent.toLowerCase();
      const minutes = parseInt(card.querySelector('.card-image span').textContent, 10);
      const matches = (!query || text.includes(query)) &&
        (cuisine === 'all' || text.includes(cuisine + ' ·')) &&
        (!under30 || minutes <= 30);
      card.style.display = matches ? '' : 'none';
      if (matches) shown += 1;
    });
    resultLine.innerHTML = `<strong>${shown}</strong> recipes found`;
  };
  filterForm.addEventListener('submit', (event) => { event.preventDefault(); applyFilters(); });
  applyFilters();
}
