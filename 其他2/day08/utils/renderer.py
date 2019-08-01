
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

        res = {
            'code': code,
            'msg': msg,
            'data': result
        }

        # super(MyJsonRenderer, self).render()
        return super().render(res, accepted_media_type=None, renderer_context=None)



