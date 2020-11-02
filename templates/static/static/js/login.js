window.onload=function() {
    var aInput = document.getElementsByTagName('input');
    var oUser = aInput[0];
    var oPwd = aInput[1]
    var aI = document.getElementsByTagName('i')[0];


    //密码检测

    oPwd.onfocus = function () {
        if (oUser.value == "") {
            aI.innerHTML = '该项不可为空';
        }
        oPwd.removeAttribute("placeholder");
    }
    oPwd.onblur = function () {
        if (this.value == "") {
            aI.innerHTML = '密码不可为空';
        }
        oPwd.setAttribute("placeholder");
        oPwd.style.placeholder = '请输入确认密码';
    }
}
    
    
