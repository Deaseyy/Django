a = [1,2]
a+=[3]
print(a)


# dic1={'a':5,'b':3}
# dic2=dic1
# dic2['c']=2
# # dic1=dic2
# # dic['b'] += 1
# a = dic1.get('d',100)
# print(a)
# print(dic1)
#
# # print({}==None)
#
# a=2
# def aa():
#     global a
#     a=a+5
#     # b=a+3
#     print(a)
#
# print(a)
# aa()




# a=2
# def aa():
#     global b
#     # a=a+5
#     b = a+10  # 先在局部查找 局部找到后发现使用在定义之前,会报错,没找到就会去全局查找
#     # a=10
#     # b=a+3
#     print(b)
# aa()
# print(a)


# if request.session.get('goods_dict') == None:  # 请求进来第二个数据就没有了
#     request.session['goods_dict'] = {}
#
# count = int(request.GET.get('count'))
# goods_id = request.GET.get('id')
# if request.session['goods_dict'].get(goods_id):
#     request.session['goods_dict'][goods_id][1] += count  # 请求进来加的数据就没有了
#     return JsonResponse({'success': '成功添加到购物车', 'goods_type_count': 2})
#
# # request.session['goods_dict'][goods_id] = [goods_id, count]
# a = request.session['goods_dict']
# a[goods_id] = [goods_id, count]
#
# # goods_type_count = len(request.session.get('goods_dict'))
# return JsonResponse({'success': '成功添加到购物车', 'goods_type_count': 2})