$(document).ready(function(){
    var open=false;
    var h1Margin=$("#h1").css("marginTop");
    //toggle navbar
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


    //Edit name
    var editNameIcon=$("#edit_name");
    var name=$("#nav_name");
    var navName=name.text();
    var divPicture=$('.picture')
    var h2NameChange=$('h2');
    var h2Name=h2NameChange.text();
    var divDetails=$('.details');

    divPicture.on("click", $('sup'),function(event){
                
        var h2Name=h2NameChange.text();
        var navName=name.text();

        if((!name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
            name.html("<input id='nameEdit' type='text'><sup><img id='edit_name' src='../static/images/edit_icon.png' alt=></sup>");
            var nameInput=$('#nameEdit')[0];
            nameInput.value=navName;
        }
  
        else if((name.html().includes('<input')) &&(event.target.localName== "sup" || event.target.localName == "img")){
            var nameInput=$('#nameEdit')[0];
            navName=nameInput.value;
            name.html(navName+'<sup><img id="edit_name" src="../static/images/edit_icon.png" alt=""></sup>');
            h2NameChange.html(navName+'<sup><img id="edit_name" src="../static/images/edit.png" alt=""></sup>');
        }
    }); 

    
    divDetails.on("click", $('sup'), function(event){

        var h2Name=h2NameChange.text();
        var navName=name.text();

        if(!(h2NameChange.html().includes('<input'))&& (event.target.localName=='sup')){
            h2NameChange.html('<input id="h2NameEdit" type="text"><sup><img id="edit_name" src="../static/images/edit.png" alt=></sup>');
            var nameInput=$('#h2NameEdit')[0];
            nameInput.value=h2Name;
        }

        else if((h2NameChange.html().includes('<input'))&& (event.target.localName=='sup')){
            var nameInput=$('#h2NameEdit')[0];
            h2Name=nameInput.value;
            h2NameChange.html(h2Name+'<sup><img id="edit_name" src="images/edit.png" alt=""></sup>');
            name.html(h2Name+'<sup><img id="edit_name" src="../static/images/edit_icon.png alt=""></sup>');
        }

    });
    
    var firstBox= $('.first');
    var mobNumber=$('.number').text();
    
    var eMail=$('.email').text();
    firstBox.on("click", $('#num-mail'), function(event){
        if(!(firstBox.html().includes('<input'))&& (event.target.id=='num-mail')){
            firstBox.html('<p>Mobile no: <input id="number" type="text"></p><p>E-mail: <input id="email" type="text"></p><img id="num-mail" class="edit" src="images/edit.png" alt="edit">');
            $('#number')[0].value=mobNumber;
            $('#email')[0].value=eMail;
        }

        else if((firstBox.html().includes('<input'))&& (event.target.id=='num-mail')){
            mobNumber=$('#number')[0].value;
            eMail=$('#email')[0].value;
            firstBox.html('<p>Mobile no: <span class="number">'+mobNumber+'</span></p><p>E-mail: <span class="email">'+eMail+'</span></p><img id="num-mail" class="edit" src="images/edit.png" alt="edit">');
        }   
    });

    var streetName=$('.streeT').text();
    var area=$('.areA').text();
    var city=$('.citY').text();
    var state=$('.statE').text();
    var pin=$('.PIN').text();

    var addressCard=$('.address');
    var introString='<img class="editAdd" src="images/edit.png" alt="edit"><div class="d-flex"><div class="rad"><input type="radio" name="selectedAddress"></div><div class="addr">';
    var endString='</div></div>';


    addressCard.on("click", $('.addr'), function(){
        
        if($(this).hasClass('one')){
            if(!($('.one').html().includes('<input class="str'))&& (event.target.className=='editAdd')){
                $('.one').html(introString+'<p>Street: <input class="streeT"></p><p>Area:<input class="areA"></p><p>City:<input class="citY"></span></p><p><span class="state">State:</span><input class="statE"><span class="pincode">Pincode:</span><input class="PIN"></p>'+endString);
            }
    
            else if(($('.one').html().includes('<input class="str'))&& (event.target.className=='editAdd')){
                streetName=$('.streeT')[0].value;
                area=$('.areA')[0].value;
                city=$('.citY')[0].value;
                state=$('.statE')[0].value;
                pin=$('.PIN')[0].value;
    
                $('.one').html(introString+'<p>Street: <span class="streeT">'+streetName+'</span></p><p>Area:<span class="areA">'+area+'</span></p><p>City:<span class="citY">'+city+'</span></p><p><span class="state">State:</span><span class="statE">'+state+'</span><span class="pincode">Pincode:</span><span class="PIN">'+pin+'</span></p>'+endString)
            } 
        }

        else if($(this).hasClass('two')){
            if(!($('.two').html().includes('<input class="str'))&& (event.target.className=='editAdd')){
                $('.two').html(introString+'<p>Street: <input class="streeT"></p><p>Area:<input class="areA"></p><p>City:<input class="citY"></span></p><p><span class="state">State:</span><input class="statE"><span class="pincode">Pincode:</span><input class="PIN"></p>'+endString);
            }
    
            else if(($('.two').html().includes('<input class="str'))&& (event.target.className=='editAdd')){
                streetName=$('.streeT')[1].value;
                area=$('.areA')[1].value;
                city=$('.citY')[1].value;
                state=$('.statE')[1].value;
                pin=$('.PIN')[1].value;
    
                $('.two').html(introString+'<p>Street: <span class="streeT">'+streetName+'</span></p><p>Area:<span class="areA">'+area+'</span></p><p>City:<span class="citY">'+city+'</span></p><p><span class="state">State:</span><span class="statE">'+state+'</span><span class="pincode">Pincode:</span><span class="PIN">'+pin+'</span></p>'+endString)
            }
        }
        
    });


});

