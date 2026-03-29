function askAI() {
    let q = document.getElementById("ask_input").value;
    fetch("/ask", {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `question=${encodeURIComponent(q)}`
    }).then(res=>res.json()).then(data=>{
        let out = document.getElementById("chat_output");
        out.innerHTML += `<p><b>You:</b> ${q}</p><p><b>AI:</b> ${data.answer}</p>`;
    });
}

function teachAI() {
    let q = document.getElementById("teach_q").value;
    let a = document.getElementById("teach_a").value;
    fetch("/teach", {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `question=${encodeURIComponent(q)}&answer=${encodeURIComponent(a)}`
    }).then(res=>res.json()).then(data=>{
        let out = document.getElementById("teach_output");
        out.innerHTML += `<p>${data.message}</p>`;
    });
}
