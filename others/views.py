from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect

import os
from PIL import Image

def printer(req):
    if req.method == 'POST':
        file = req.FILES.get("image")
        num = req.POST.get("num")
        # 灰度打印与否
        gray = req.POST.get("gray")
        # 单双页打印
        two_side = req.POST.get("one_side")
        if two_side != "no":
            sides_comment = "sides=two-sided-short-edge"
        else:
            sides_comment = "sides=one-sided"
        os.chdir(r"../")
        with open(file.name,"wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        # 转灰度图
        if gray == "yes":
            try:
                image = Image.open(file.name)
                image = image.convert("L")
                image.save(file.name)
            except Exception as e:
                print("非图片格式！")
        
        os.system(f"lpr {file.name} -# {num} -o {sides_comment} -r")
    return render(req,"others/printer.html",locals())
