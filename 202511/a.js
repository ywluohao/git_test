const ids = Array.from(document.querySelectorAll('div[data-node-id]'))
  .map(el => el.getAttribute('data-node-id'))
  .join('\n');

console.log(ids);