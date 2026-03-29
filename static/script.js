function ask() {
    let question = document.getElementById("question").value;
    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "question=" + encodeURIComponent(question)
    }).then(res => res.json())
      .then(data => {
        let chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p><b>You:</b> "+question+"</p>";
        chatBox.innerHTML += "<p><b>AI:</b> "+data.answer+"</p>";
      });
}

function teach() {
    let q = document.getElementById("question").value;
    let a = document.getElementById("answer").value;
    fetch("/teach_submit", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "question=" + encodeURIComponent(q) + "&answer=" + encodeURIComponent(a)
    }).then(res => res.json())
      .then(data => alert(data.message));
}
