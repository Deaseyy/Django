### 订单界面展示接口


#### 请求地址: /api/order/order/


#### 请求方式: GET


#### 请求参数:
    
    token  s5ds4d5s4d5s4d5s4ds string
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '下单OK!'
        
        'data':{
        
            order:{
                order_goods_info : 订单详情对象
                
                模型中自带字段
                
            }
            
        }
    }
    
#### 2.失败响应

    {
      
    }
    
   
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    order 序列化后的购物车对象