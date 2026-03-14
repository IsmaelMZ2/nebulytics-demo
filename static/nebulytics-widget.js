(function() {
    // 1. Crear el contenedor principal
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'nebulytics-ai-widget';
    document.body.appendChild(widgetContainer);

    // 2. Estilos del Widget (Inyectados directamente)
    const style = document.createElement('style');
    style.innerHTML = `
        #nebulytics-button {
            position: fixed; bottom: 20px; right: 20px;
            width: 60px; height: 60px;
            background: #22d3ee; border-radius: 50%;
            box-shadow: 0 4px 15px rgba(34, 211, 238, 0.4);
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            z-index: 9999; transition: all 0.3s ease;
        }
        #nebulytics-button:hover { transform: scale(1.1); background: #06b6d4; }
        
        #nebulytics-window {
            position: fixed; bottom: 90px; right: 20px;
            width: 350px; height: 450px;
            background: #1a1d27; border: 1px solid #2d3343;
            border-radius: 16px; display: none; flex-direction: column;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 9999; overflow: hidden;
            font-family: sans-serif;
        }
        .chat-header { background: #22d3ee; color: #0f1117; padding: 15px; font-weight: bold; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; color: #e2e8f0; font-size: 14px; }
        .chat-input { padding: 15px; border-top: 1px solid #2d3343; display: flex; }
        .chat-input input { 
            flex: 1; background: #0f1117; border: 1px solid #2d3343; 
            color: white; padding: 8px; border-radius: 8px; outline: none;
        }
        .bot-msg { background: #2d3343; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    `;
    document.head.appendChild(style);

    // 3. HTML del Widget
    widgetContainer.innerHTML = `
        <div id="nebulytics-button">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
        </div>
        <div id="nebulytics-window">
            <div class="chat-header">Nebulytics IA Assistant</div>
            <div class="chat-messages" id="chat-box">
                <div class="bot-msg">¡Hola! Soy tu asistente IA de Nebulytics. ¿En qué puedo ayudarte hoy con tu tienda?</div>
            </div>
            <div class="chat-input">
                <input type="text" placeholder="Pregunta sobre tu negocio..." id="user-input">
            </div>
        </div>
    `;

    // 4. Lógica de apertura/cierre
    const btn = document.getElementById('nebulytics-button');
    const win = document.getElementById('nebulytics-window');
    
    btn.onclick = () => {
        win.style.display = win.style.display === 'flex' ? 'none' : 'flex';
    };

    // 5. Lógica básica de envío (Simulación IA)
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && input.value.trim() !== "") {
            const userText = input.value;
            chatBox.innerHTML += `<div style="text-align:right; margin-bottom:10px; color:#22d3ee;">${userText}</div>`;
            input.value = "";
            
            // Simular respuesta de IA
            setTimeout(() => {
                chatBox.innerHTML += `<div class="bot-msg">Analizando datos... Según mi predicción, tus ventas de Zapatillas subirán un 15% la próxima semana.</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
        }
    });
})();
