window.addEventListener('load',function(){
    var login = this.document.querySelector('.login');
    var register = this.document.querySelector('.register');
    var change1 = this.document.querySelector('.change1');
    var change2 = this.document.querySelector('.change2');
    change1.addEventListener('click',function(){
            login.style.opacity=('0');
            login.style.zIndex=('-1');
            register.style.opacity=('1');
            register.style.zIndex=('0');
    })
    change2.addEventListener('click',function(){
            login.style.opacity=('1');
            login.style.zIndex=('0');
            register.style.opacity=('0');
            register.style.zIndex=('-1');
    })
})