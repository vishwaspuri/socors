$(document).ready(function(){
    var open=false;
    var h1Margin=$("#h1").css("marginTop");
    
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

    if(h1Margin<='50px'){
        $('h1').addClass('h1MinMargin');
        $('h1').removeClass('h1margin');
    }

    if(h1Margin>='50px'){
        $('h1').addClass('h1margin');
        $('h1').removeClass('h1MinMargin');
    }

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

