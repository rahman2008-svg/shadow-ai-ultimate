async function sendMessage() {
    const input = document.getElementById("user-input");
    const question = input.value;
    if(!question) return;
    appendMessage(question, 'user-msg');
    input.value = '';

    // Typing animation
    const typingId = appendMessage("Typing...", 'ai-msg', true);

    const res = await fetch("/ask", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({question})
    });
    const data = await res.json();

    // Replace typing animation with answer
    replaceMessage(typingId, data.answer);
}

async function teachAI() {
    const q = document.getElementById("teach-question").value;
    const a = document.getElementById("teach-answer").value;
    if(!q || !a) return alert("Both question and answer required!");
    const res = await fetch("/teach", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({question:q, answer:a})
    });
    const data = await res.json();
    alert(data.message);
    document.getElementById("teach-question").value="";
    document.getElementById("teach-answer").value="";
}

function appendMessage(msg, cls, isTemp=false){
    const box = document.getElementById("chat-box");
    const p = document.createElement("p");
    p.className = cls;
    p.innerText = msg;
    if(isTemp) p.dataset.temp = "true";
    box.appendChild(p);
    box.scrollTop = box.scrollHeight;
    return p;
}

function replaceMessage(elem, msg){
    elem.innerText = msg;
    delete elem.dataset.temp;
}
