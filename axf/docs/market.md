### 登陆接口


#### 请求地址: /api/goods/market/


#### 请求方式: GET


#### 请求参数:

    typeid  总分类id
    childcid  子分类id
    order_rule  排序id
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'goods_list':  serializer.data,
            'order_rule_list':  order_rule_list,
            'foodtype_childname_list':  foodtype_childname_list,
        }
    }
    
#### 2.失败响应


#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    data
        goods_list 商品信息 string
        order_rule_list  排序
        foodtype_childname_list 商品子分类
    