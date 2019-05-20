### 提交订单接口


#### 请求地址: /api/order/order/


#### 请求方式: POST


#### 请求参数:
    
    token  s5ds4d5s4d5s4d5s4ds string
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '下单OK!'
        
        'data':{
        
            
        }
    }
    
#### 2.失败响应

    {
       'code': 1009,
       'msg': '购物车中没有商品,请先添加!'
    }
    
   
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    