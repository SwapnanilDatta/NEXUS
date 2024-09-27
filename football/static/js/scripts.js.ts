// Modal logic
function openModal(playerId) {
    var modal = document.getElementById('modal-' + playerId);
    modal.style.display = 'block';
}

function closeModal(playerId) {
    var modal = document.getElementById('modal-' + playerId);
    modal.style.display = 'none';
}

// Close modal if clicked outside the content
window.onclick = function(event) {
    var modals = document.getElementsByClassName("modal");
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}
