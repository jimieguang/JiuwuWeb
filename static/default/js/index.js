window.addEventListener('load',function(){
    var slideshow = this.document.querySelector('.slideshow');
    var arrowl = this.document.querySelector('.arrowl');
    var arrowr = this.document.querySelector('.arrowr');
    var ul = this.document.querySelector('.pictures');
    var ol = this.document.querySelector('ol');
    
    // 轮播图动画函数
    function animate(obj,target,callback){
        clearInterval(obj.timer);
        var timer = setInterval(function(){
            var step = (target-obj.offsetLeft)/10;
            step = step>0?Math.ceil(step):Math.floor(step);
            if(obj.offsetLeft ==target){
                clearInterval(timer);
                callback && callback();
            }
            obj.style.left = obj.offsetLeft + step + 'px';
        },20);
    }

    //动态生成小圆点
    for(var i=0;i<ul.children.length;i++){
        var li = this.document.createElement('li');
        li.setAttribute('index',i);
        ol.appendChild(li);
    }
    var first = ul.children[0].cloneNode(true);
    ul.appendChild(first);
    var flag = true;//节流阀

    //点击箭头移动图片
    var slideshowWidth = slideshow.offsetWidth;
    var num=0;
    ol.children[0].className='current';
    arrowr.addEventListener('click',function(){
        if(flag){
            flag = false;
            if(num==ul.children.length-1){
                ul.style.left=0;
                num=0;
                // for(var i=0;i<ol.children.length;i++){
                //     ol.children[i].className='';
                // }
                // ol.children[0].className='current';
            }
            num++;
            animate(ul,-num*slideshowWidth,function(){
                flag = true;
            });
            for(var i=0;i<ol.children.length;i++){
                ol.children[i].className='';
            }
            ol.children[num].className='current';
        }
    });
    arrowl.addEventListener('click',function(){
        if(flag){
            flag = false;
            if(num==0){
                num=ul.children.length-1;
                ul.style.left=-num*slideshowWidth+'px';
            }
            num--;
            animate(ul,-num*slideshowWidth,function(){
                flag = true;
            });
            for(var i=0;i<ol.children.length;i++){
                ol.children[i].className='';
            }
            ol.children[num].className='current';
        }
    });
    //自动播放定时器
    var timer = this.setInterval(function(){
        arrowr.click();
    },2500);
    //鼠标移入移出暂停开始动画
    slideshow.addEventListener('mouseenter',function(){
        clearInterval(timer);
        timer=null;
    });
    slideshow.addEventListener('mouseleave',function(){
        timer = setInterval(function(){
            arrowr.click();
        },2500);
    });

    //搜索栏虚拟按钮
    var newbtn = this.document.querySelector('.newbtn');
    newbtn.addEventListener('click',function(){
        document.querySelector('.acubtn').click();
    })
})