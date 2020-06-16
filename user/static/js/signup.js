$(document).ready(function(){

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
            const request = new XMLHttpRequest();
        
            request.onload= function(){
                var responseJSON= JSON.parse(request.responseText);
                if(responseJSON.status){
                        document.getElementsByClassName("center")[1].innerHTML="<p>Swipe to Continue</p>";
                        document.getElementsByClassName("otp")[0].innerHTML='<img src=holding_mobile_phone alt="hand_holding_mobile"><h1>Enter OTP</h1><div id="otp-form">'+
                            '<input id="one" type="text" onkeypress="focusTwo()" required>'+
                            '<input id="two" type="text" onkeypress="focusThree()" required>'+
                            '<input id="three" type="text" onkeypress="focusFour()" required>'+
                            '<input id="four" type="text" required>'+
                    
                            '<input type="submit" value="submit" id="otp-submit">'+
                        '</div>';

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
                                document.getElementById("next").classList.add("swiper-button-next");
                                document.getElementById("next").classList.remove("swiper-button-disabled");
                            }
                        }
                    
                        const OTPRequestData={
                            "phone": form.phone.value,
                            "otp": OTPform.otp.children[0].value+OTPform.otp.children[1].value+OTPform.otp.children[2].value+OTPform.otp.children[3].value
                        }
                    
                        const OTPstring=JSON.stringify(OTPRequestData);
                        console.log(OTPstring)
                        OTPrequest.open('post',transferProtocol+"://socorsnearyou.xyz/user/api/otp/");
                        OTPrequest.setRequestHeader('Content-type', 'application/json');
                        OTPrequest.send(OTPstring);
                    })
                }
                else{
                    console.log(this.responseText)
                }
            }
        
            const requestData={
                "phone": form.phone.value,
                "full_name": form.full_name.value,
                "email": form.email.value,
                "password": form.password.value
            }
        
            const reqJSON=JSON.stringify(requestData)
            request.open('post', transferProtocol+'://socorsnearyou.xyz/user/api/validate-phone/');
            request.setRequestHeader('Content-type', 'application/json');
            request.send(reqJSON);
        })
    
    var eyePos=0.87*parseInt($('#password').css('width'));
    var i=0;
    $('#password').on("click", function(event){
        if(event.offsetX>eyePos){
            if(i==0){
                $('#password').css("background-image","url(images/show.png)");
                $('#password')[0].attributes[0].value="text";
                i=1;
            }
            else{
                $('#password').css("background-image","url(images/hide.png)");
                $('#password')[0].attributes[0].value="password";
                i=0;
            }
        }
    })
});
