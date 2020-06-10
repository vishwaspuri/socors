document.getElementById("modalbutton").addEventListener("click", function(){
    var modalBox=document.querySelector('.mod');
    document.querySelector(".modal-backdrop").classList.remove("modal-backdrop");
    modalBox.classList.remove("show");
    modalBox.style.display="none";
})
