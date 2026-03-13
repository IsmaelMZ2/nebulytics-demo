(function() {
    // 1. Configuración de la URL de tu backend en Render
    const API_URL = "https://nebulytics-demo.onrender.com/api/v1/chatbot/ask";

    // 2. Crear los estilos del Widget (CSS)
    const style = document.createElement('style');
    style.innerHTML = `
        #nebulytics-bot-container {
            position: fixed; bottom: 20px; right: 20px; z-index: 1000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        #nebulytics-button {
            background-color: #007bff; color: white; width: 60px; height: 60px;
            border-radius: 50%; border: none; cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); font-size: 24px;
        }
        #nebulytics-chat-window {
            display: none; position: absolute; bottom: 80px; right: 0;
            width: 320px; height: 450px; background: white;
            border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            flex-direction: column; overflow: hidden; border: 1px solid #eee;
        }
        #chat-header { background: #007bff; color: white; padding: 15px; font-weight: bold; }
        #chat-messages { flex: 1; padding: 15px; overflow-y: auto; font-size: 14px; background: #f9f9f9; }
        #chat-input-area { display: flex; border-top: 1px solid #eee; padding: 10px; }
        #chat-input { flex: 1; border: 1px solid #ddd; border-radius: 4px; padding: 8px; outline: none; }
        #chat-send { background: #007bff; color: white; border: none; padding: 0 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; }
        .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 8px; max-width: 80%; }
        .user-msg { background: #007bff; color: white; align-self: flex-end; margin-left: auto; }
        .bot-msg { background: #e9ecef; color: #333; align-self: flex-start; }
    `;
    document.head.appendChild(style);

    // 3. Crear la estructura del Widget
    const container = document.createElement('div');
    container.id = 'nebulytics-bot-container';
    container.innerHTML = `
        <div id="nebulytics-chat-window">
            <div id="chat-header">Asistente Nebulytics</div>
            <div id="chat-messages" style="display: flex; flex-direction: column;">
                <div class="msg bot-msg">¡Hola! Soy tu asistente de inventario. ¿En qué puedo ayudarte hoy?</div>
            </div>
            <div id="chat-input-area">
                <input type="text" id="chat-input" placeholder="Escribe un mensaje...">
                <button id="chat-send">Enviar</button>
            </div>
        </div>
        <button id="nebulytics-button">🤖</button>
    `;
    document.body.appendChild(container);

    // 4. Lógica de Interacción
    const btn = document.getElementById('nebulytics-button');
    const window = document.getElementById('nebulytics-chat-window');
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send');
    const messages = document.getElementById('chat-messages');

    btn.onclick = () => window.style.display = window.style.display === 'none' ? 'flex' : 'none';

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Mostrar mensaje del usuario
        appendMessage('user-msg', text);
        input.value = '';

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, store_id: "demo_store" })
            });
            const data = await response.json();
            appendMessage('bot-msg', data.response);
        } catch (error) {
            appendMessage('bot-msg', "Lo siento, estoy sincronizando inventarios. Intenta de nuevo en un momento.");
        }
    }

    function appendMessage(className, text) {
        const div = document.createElement('div');
        div.className = `msg ${className}`;
        div.innerText = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    sendBtn.onclick = sendMessage;
    input.onkeypress = (e) => { if(e.key === 'Enter') sendMessage(); };
})();