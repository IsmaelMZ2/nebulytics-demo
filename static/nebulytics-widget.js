(function() {
    const container = document.getElementById('ai-widget-container');
    
    // Inyectar HTML del chat moderno
    container.innerHTML = `
        <div id="chat-bubble" style="position:fixed; bottom:30px; right:30px; width:60px; height:60px; background:#22d3ee; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; z-index:1000; box-shadow: 0 0 20px rgba(34,211,238,0.5);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </div>
        <div id="chat-window" style="position:fixed; bottom:110px; right:30px; width:380px; height:500px; background:#111827; border:1px solid #374151; border-radius:24px; display:none; flex-direction:column; z-index:1000; overflow:hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
            <div style="padding:20px; background:#22d3ee; color:black; font-weight:bold;">Nebulytics Conversational AI</div>
            <div id="messages" style="flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:10px;">
                <div style="background:#1f2937; padding:12px; border-radius:15px; font-size:14px;">¡Hola Ismael! Soy el orquestador de Nebulytics. Pregúntame sobre tus ventas o inventario.</div>
            </div>
            <div style="padding:20px; border-top:1px solid #374151;">
                <input id="chat-input" type="text" placeholder="Escribe un comando..." style="width:100%; background:#000; border:1px solid #374151; color:white; padding:12px; border-radius:12px; outline:none;">
            </div>
        </div>
    `;

    const bubble = document.getElementById('chat-bubble');
    const win = document.getElementById('chat-window');
    const input = document.getElementById('chat-input');
    const msgBox = document.getElementById('messages');

    bubble.onclick = () => win.style.display = win.style.display === 'flex' ? 'none' : 'flex';

    input.onkeypress = async (e) => {
        if (e.key === 'Enter' && input.value !== "") {
            const userMsg = input.value;
            msgBox.innerHTML += `<div style="align-self:flex-end; background:#22d3ee; color:black; padding:10px; border-radius:15px; font-size:14px;">${userMsg}</div>`;
            input.value = "";

            // Llamada al backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: userMsg})
            });
            const data = await response.json();

            // Respuesta de la IA
            msgBox.innerHTML += `<div style="background:#1f2937; padding:12px; border-radius:15px; font-size:14px;">${data.reply}</div>`;
            
            // Acción dinámica: ¿Actualizar el dashboard?
            if (data.action === "UPDATE_CHART") {
                updateDashboard(data.payload);
            }
            
            msgBox.scrollTop = msgBox.scrollHeight;
        }
    };
})();
