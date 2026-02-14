document.addEventListener('click', function (e) {
    const item = e.target.closest('.chat-item')
    if (!item) return

    document.querySelectorAll('.chat-item.active')
        .forEach(el => el.classList.remove('active'))

    item.classList.add('active')
})

document.addEventListener("htmx:wsAfterMessage", handleResponseFromDjangoChannel)
function handleResponseFromDjangoChannel(event) {
    const message = event.detail.message
    let data
    try {
        data = JSON.parse(message)
  } catch (err) {
        console.warn("Invalid JSON:", err)
        return
    }

    if (data.type === "user_message") {
        const chat = document.getElementById('chat-log')
        chat.insertAdjacentHTML("beforeend", data.html_content)
        return
    }

    if (data.type ==="done") {
        const container = document.getElementById(`ai-stream-${data.message_id}`)
        delete container.dataset.buffer
        return
    }

    if (data.type === "ai_chunk") {
        const container = document.getElementById(`ai-stream-${data.message_id}`)
        if (!container) {
            console.warn(`Container with id ${data.message_id} is not found`)
            return
        }
        if (!container.dataset.buffer) container.dataset.buffer = ""
        container.dataset.buffer += data.chunk
        tryRender(container)
    }
}

function tryRender(container) {
    const buffer = container.dataset.buffer
    if (!buffer) return

    const parser = new DOMParser()
    const doc = parser.parseFromString(buffer, "text/html")

    if(doc.querySelector("parsererror")) return

    container.innerHTML = doc.body.innerHTML
    container.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block)
    })

}