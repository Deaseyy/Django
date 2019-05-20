### 添加购物车接口


#### 请求地址: /api/cart/cart/add_cart/


#### 请求方式: POST


#### 请求参数:
    
    token  s5ds4d5s4d5s4d5s4ds string
    
    goodsid 商品id  int
    
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '添加成功!'
        
        'data':{
        
            
        }
    }
    
#### 2.失败响应

    {
        'code': 1007,
        'msg': '请先登陆后再操作'
    }
    
   
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    
    