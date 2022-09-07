from django.shortcuts import render

def detect_login_middleware(get_response):
    '''检查用户是否登录以决定返回正常网页与否'''
    # One-time configuration and initialization.
    # 完全匹配
    need_login_urls = [
        '/goodsIssue/newGoods',
    ]
    # 部分匹配
    need_login_url_elements = [
        '/userIssue/PM/',
        '/message/', 
        '/goodsIssue/myGoods',
    ]
    def middleware(req):
        need_detect = False
        url = req.path_info
        for element in need_login_url_elements:
            if element in url:
                need_detect = True
        if url in need_login_urls or need_detect:
            if not req.session.get('islogin'):
                msg = '你还未登陆，请先登陆！'
                return render(req, 'error_msg.html', locals())
        # ↑ Code to be executed for each request before the view (and later middleware) are called.
        response = get_response(req)
        # ↓ Code to be executed for each request/response after the view is called.
        return response
    return middleware