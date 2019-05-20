### 商品分类展示接口


#### 请求地址: /api/goods/foodtype/


#### 请求方式: GET


#### 请求参数:

    
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'foodtypes':foodtypes
        }
    }
    
#### 2.失败响应

    
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    data 响应数据 
        foodtypes  商品分类  string 
    