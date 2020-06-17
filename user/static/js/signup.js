$(document).ready(function(){

    var swipeWrapper=document.querySelector('.swiper-wrapper');
    var wide=swipeWrapper.clientWidth;
    var shiftDist=wide;
    var shift="(-"+String(shiftDist)+"px,0px,0px)";
    var $submitBtn = $("#submit");
    var $passwordBox = $("#password");
    var $confirmBox = $("#confirm-password");
    var $errorMsg =  $('<br><span id="error_msg">Passwords do not match.</span>');

    $submitBtn.removeAttr("disabled");

    function checkMatchingPasswords(){
        if($confirmBox.val() != "" && $passwordBox.val != ""){
            if( $confirmBox.val() != $passwordBox.val() ){
                $submitBtn.attr("disabled", "disabled");
                $errorMsg.insertAfter($confirmBox);
            }
        }
    }

    function resetPasswordError(){
        $submitBtn.removeAttr("disabled");
        var $errorCont = $("#error_msg");
        if($errorCont.length > 0){
            $errorCont.remove();
        }  
    }

    focusTwo = function getFocus() {           
        document.getElementById("two").focus();
    }
    focusThree= function getFocus() {           
        document.getElementById("three").focus();
    }
    focusFour = function getFocus() {  
            document.getElementById("four").focus();
    }

    $("#confirm-password, #password")
         .on("keydown", function(e){

            if(e.keyCode == 13 || e.keyCode == 9) {
                checkMatchingPasswords();
            }
         })
         .on("blur", function(){                    

            checkMatchingPasswords();
        })
        .on("focus", function(){
            resetPasswordError();
        })

        const form= {
            phone: document.getElementById("phone"),
            full_name: document.getElementById("full_name"),
            email: document.getElementById("email"),
            password: document.getElementById("password"),
            submit: document.getElementById("submit")
        }
                
        form.submit.addEventListener("click", function(){
            if(phonenumber(document.querySelector("#phone").value)){
                document.getElementsByClassName("center")[1].innerHTML="";
                const request = new XMLHttpRequest();
        
                request.onload= function(){
                    var responseJSON= JSON.parse(request.responseText);
                    if(responseJSON.status){
                            document.getElementsByClassName("center")[1].innerHTML="<p>Swipe to Continue</p>";
                            document.getElementsByClassName("otp")[0].innerHTML='<h1>Enter OTP</h1><div id="otp-form">'+
                                '<input id="one" type="text" onkeypress="focusTwo()" required>'+
                                '<input id="two" type="text" onkeypress="focusThree()" required>'+
                                '<input id="three" type="text" onkeypress="focusFour()" required>'+
                                '<input id="four" type="text" required>'+
                        
                                '<input type="submit" value="submit" id="otp-submit">'+
                            '</div>';
                            swipeWrapper.style.transform="translate3d"+shift;
                            swipeWrapper.style.transitionDuration="300ms";
                            const OTPform={
                            phone: form.phone.value,
                            otp: document.getElementById("otp-form"),
                            submit: document.getElementById("otp-submit")
                        }
    
                        
                        OTPform.submit.addEventListener("click", function(){
                            const OTPrequest= new XMLHttpRequest();
                        
                            OTPrequest.onload=function(){
                                const OTPresponse=JSON.parse(this.responseText);
                                if(OTPresponse.status==true){
                                    document.getElementsByClassName("center")[2].innerHTML="<p class='red'>Click <a href='https://socorsnearyou.xyz/user/login/'>here</a> to login</p>"
                                }
                                else{
                                    showError(OTPresponse.detail)
                                }
                            }
                        
                            const OTPRequestData={
                                "password": form.password.value,
                                "phone": form.phone.value,
                                "otp": OTPform.otp.children[0].value+OTPform.otp.children[1].value+OTPform.otp.children[2].value+OTPform.otp.children[3].value
                            }
                        
                            const OTPstring=JSON.stringify(OTPRequestData);
                            OTPrequest.open('post',"https://socorsnearyou.xyz/user/api/otp/");
                            OTPrequest.setRequestHeader('Content-type', 'application/json');
                            OTPrequest.send(OTPstring);
                        })
                    }
                    else{
                           showError(responseJSON.detail);
                    }
                }
            
                const requestData={
                    "phone": form.phone.value,
                    "full_name": form.full_name.value,
                    "email": form.email.value,
                    "password": form.password.value
                }
            
                const reqJSON=JSON.stringify(requestData)
                request.open('post', 'https://socorsnearyou.xyz/user/api/validate-phone/');
                request.setRequestHeader('Content-type', 'application/json');
                request.send(reqJSON);
            }
            else{
                document.getElementsByClassName("center")[1].innerHTML="<p class='red'>Mobile Number must be 10 digits without special characters and spaces</p>"
            }
           
        })

        function showError(text){
            var modalBox=document.querySelector('.modal');
            var body=document.querySelector('body');
            document.querySelector('.modal-body').innerHTML="<span>"+text+"</span>";
            modalBox.classList.add('show');
            body.classList.add('modal-open');
            modalBox.style.display="block";
            body.addEventListener('click', function(){
                modalBox.style.display="none";
                modalBox.classList.remove('show');
                body.classList.remove('modal-open')
            })
        }
        function phonenumber(inputtxt){
            var phoneno = /^\d{10}$/;
            if( inputtxt.match(phoneno))
                    {
                return true;
                    }
                else
                    {
                    return false;
                    }
        }
});
