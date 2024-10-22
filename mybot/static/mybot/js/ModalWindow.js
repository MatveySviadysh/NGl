var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
    btn.innerHTML = "✖";
}

span.onclick = function() {
    modal.style.display = "none";
    btn.innerHTML = "📩";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        btn.innerHTML = "📩";
    }
}

document.getElementById("djangoBtn").onclick = function() {
    alert("Кнопка Django нажата!");
}
