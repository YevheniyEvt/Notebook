document.body.addEventListener('htmx:afterSwap', function(event) {
    // знайти всі нові blocks
    event.target.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
});