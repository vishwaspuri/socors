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
})