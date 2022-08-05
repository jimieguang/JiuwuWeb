window.addEventListener('load',function(){
    //虚拟按钮
    var newbtn = this.document.querySelector('.newbtn');
    newbtn.addEventListener('click',function(){
        document.querySelector('.acubtn').click();
    })
})