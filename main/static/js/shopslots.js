var open=false;
var h1Margin=$("h1").css("marginTop");
var timeButtons=document.querySelectorAll(".bt");
$(document).ready(function(){

        $(".navbar-toggler, .overlay").on("click",function(){
            $(".mobileMenu, .overlay").addClass("open");
            open=true;
        });
    
    
        $(".content").on("click",function(){
            if(open){
                $(".mobileMenu, .overlay").removeClass("open");
                open=false;
            }
        });

        for(var i=0;i<timeButtons.length;i++){
            if(timeButtons[i].classList.contains('btn-danger')){
                timeButtons[i].disabled=true;
            }
        }
    

    var editNameIcon=$("#edit_name");
    var name=$("#nav_name");
    var currentName=name.text();
    var divPicture=$('.picture')
    divPicture.on("click", $('sup'),function(event){
              
              if((!name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
                  name.html("<input id='nameEdit' type='text'><sup><img id='edit_name' src='./../static/images/edit_icon.png' alt=></sup>");
                  var nameInput=$('#nameEdit')[0];
                  nameInput.value=currentName;
              }

              else if((name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
                  var nameInput=$('#nameEdit')[0];
                  currentName=nameInput.value;
                  name.html(currentName+'<sup><img id="edit_name" src="./../static/images/edit_icon.png" alt=""></sup>');
             
              }
  });  
});