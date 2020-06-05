document.getElementById("modalbutton").addEventListener("click", function(){
        var modalBox=document.querySelector('.modal');
        document.querySelector(".modal-backdrop").classList.remove("modal-backdrop");
        modalBox.classList.remove("show");
        modalBox.style.display="none";
    })
