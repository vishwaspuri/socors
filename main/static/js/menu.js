var open=false;
var inputMargin=$("input[type='search']").css("marginTop");
var textIndent=parseInt($('input').css('text-indent'))/100;
var searchWidth=textIndent*parseInt($('input').css('width'));
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
   
        if(inputMargin<='50px'){
            $("input[type='search']").addClass('inputMinMargin');
            $("input[type='search']").removeClass('inputmargin');
        }

        if(inputMargin>='50px'){
            $("input[type='search']").addClass('inputmargin');
            $("input[type='search']").removeClass('inputMinMargin');
        }

        $('input').on("click", function(event){
            if(event.offsetX <= searchWidth){
                console.log("clicked on search");
            }
        });

        var editNameIcon=$("#edit_name");
    var name=$("#nav_name");
    var currentName=name.text();
    var divPicture=$('.picture')
    divPicture.on("click", $('sup'),function(event){
                
                if((!name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
                    name.html("<input id='nameEdit' type='text'><sup><img id='edit_name' src='./../nav_imgs/edit_icon.png' alt=></sup>");
                    var nameInput=$('#nameEdit')[0];
                    nameInput.value=currentName;
                }

                else if((name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
                    var nameInput=$('#nameEdit')[0];
                    currentName=nameInput.value;
                    name.html(currentName+'<sup><img id="edit_name" src="./../nav_imgs/edit_icon.png" alt=""></sup>');
               
                }
    });  
});