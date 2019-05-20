from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        {
            'code': 200,
            'msg': '请求成功',
            'data': data
        }
        """
        try:
            code = data.pop('code')
            msg = data.pop('msg')
        except:
            code = 200
            msg = '请求成功'
        try:
            result = data.pop('data')
        except:
            result = data

        # code = data.pop('code', 200)
        # msg = data.pop('msg', '请求成功')
        # result = data.pop('data', data)

        # 将http响应状态码改为200, 若不加,抛错时,http的响应状态码会显示500,前端ajax请求信息会是失败,不会进入then,直接执行catch里的语句
        renderer_context['response'].status_code = 200

        res = {
            'code': code,
            'msg': msg,
            'data': result,
        }
        return super().render(res,accepted_media_type=None, renderer_context=None)