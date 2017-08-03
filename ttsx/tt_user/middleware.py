class UrlMiddleware:
    def process_view(self,request,view_name,view_args,view_kwargs):
        if request.path not in [
            '/user/register/',
            '/user/register_handle/',
            '/user/login/',
            '/user/check_user_name_(\w+)/',
            '/user/check_login/',
            '/user/session(\w+)/',
            '/user/verify_code/',
        ]:
            request.session['url_path']=request.get_full_path()
