function getLength(str){
    return str.replace(/[^\x00-xff]/g,"xx").length;  //\x00-xff 此区间是单子节 ，除了此区间都是双字节。
}
function findStr(str,n){
    var tmp=0;
    for(var i=0;i<str.length;i++){
        if(str.charAt(i)==n){
            tmp++;
        }
    }
    return tmp;
}
    


    //确认密码
    pwd2.onblur=function() {
        if (this.value != pwd.value) {
            pwd2_msg.innerHTML = '<i></i>两次密码输入到不一致';
            pwd.style.border = '1px solid red';
        } else if (this.value == "") {
            pwd2_msg.innerHTML = '<i></i>请输入密码';
            pwd.style.border = '1px solid red';
        } else {
            pwd2.style.border = '1px solid #fff';
        }

    }








































