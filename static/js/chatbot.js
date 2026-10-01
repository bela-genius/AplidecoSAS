function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("chatbot-toggle");
    const win = document.getElementById("chatbot-window");
    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");

    toggle.addEventListener("click", () => win.classList.toggle("hidden"));

    function appendMessage(text, sender) {
        const bubble = document.createElement("div");
        bubble.className = sender === "user"
            ? "ml-auto bg-rojo text-crema-100 rounded-xl px-3 py-2 max-w-[80%]"
            : "mr-auto bg-crema-200 text-carbon rounded-xl px-3 py-2 max-w-[80%]";
        bubble.textContent = text;
        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        appendMessage(text, "user");
        input.value = "";

        try {
            const response = await fetch("/api/chatbot/message/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ message: text }),
            });
            const data = await response.json();
            appendMessage(data.reply || "Ocurrió un error, intenta de nuevo.", "bot");
        } catch (error) {
            appendMessage("No pude conectarme. Intenta más tarde.", "bot");
        }
    });
});
