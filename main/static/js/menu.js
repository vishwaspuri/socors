var open=false;
var numPages=0;
var textIndent=parseInt($('input').css('text-indent'))/100;
var searchWidth=textIndent*parseInt($('input').css('width'));
var startString= '<div class="shop row">'+
                    '<div class="col-3"><div class="row"><img src="../static/images/shop.png" alt="shop_img"></div>'+
                        '<div class="row status">'+
                            'Status: <span class="';
                            
var midString1= '</span></div></div>';
                            
var midString2= '<div class="col-7">'+
                    '<div class="row justify-content-center">'+
                        '<p class="shop_name">';             

var midString3='</p>'+
            '</div>'+
            '<div class="row justify-content-center">'+
                '<p class="shop_address">';
                
var midString4='</p>'+
                '</div>'+
                '<div class="d-flex flex-row-reverse">'+
                '<button type="button" class="btn';

var endString='><a class="get-slots" href="';

var lastString='">Get Timeslot</a></button>'+
                '</div>'+
            '</div>'+  
        '</div>';
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

        $('input').on("click", function(event){
            if(event.offsetX <= searchWidth){
                loadShops();

            }
        });
        if(numPages>=1){
            document.querySelector('.load-more').addEventListener("click", function(){
                console.log("load more click")
                
                loadShops();
            })
        }


        function loadShops(){
            var searchQuery=document.getElementById("search_input").value;
                document.querySelector('.content').innerHTML='';        
                var xhr=new XMLHttpRequest();
                xhr.open("GET",'https://vishwastest.pythonanywhere.com/api/search-shop/'+searchQuery+'/', true);
                xhr.onload=function(){
                    if(this.status==200){
                        var shops=JSON.parse(this.responseText);
                        
                        var output='<h1 id="h1">Search Results</h1>';
                        if(shops.status==true){
                            var k=shops.payload.length;
                            for(var i=numPages*10;i<numPages*10+10;i++){
                                if(i<k){
                                    var btnClass=' "';
                                    var shopStatus='open';
                                    var d= new Date();
                                    if(d.getHours()<shops.payload[i].start_time.slice(0,2)|| d.getHours()>shops.payload[i].stop_time.slice(0,2)){
                                        shopStatus="closed";
                                    }
                                    if(shopStatus=="closed"){
                                        btnClass=' disabled" disabled="true"';
                                    }
                                    output+=startString+shopStatus+'">'+shopStatus.charAt(0).toUpperCase()+shopStatus.slice(1)+midString1+midString2+shops.payload[i].name+midString3+shops.payload[i].shop_address_street+" "+shops.payload[i].shop_address_area+" "+shops.payload[i].shop_address_city+" "+ shops.payload[i].shop_address_state+midString4+btnClass+endString+'https://vishwastest.pythonanywhere.com/shops-slots/'+shops.payload[i].gst_id+'/'+lastString;
                                }
                                
                            }
                            numPages+=1;
                            document.getElementsByClassName('content')[0].innerHTML+=output+'<div class="load-more"><p>Load More</p></div>';
                            document.querySelector('.load-more').addEventListener("click", function(){
                                loadShops();
                            })
                        }
                    }
                }
            xhr.send();
        }  
});
