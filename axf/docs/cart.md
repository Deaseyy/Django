### 购物车商品展示接口


#### 请求地址: /api/cart/cart/


#### 请求方式: GET


#### 请求参数:

    token  s5ds4d5s4d5s4d5s4ds string
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'carts': serializer.data,
            
            'total_price': total_price,
        }
    }
    
#### 2.失败响应

    
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    data
    
        carts 购物车对象  json
    
        total_price 总价  int
    