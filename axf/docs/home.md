### 首页接口


#### 请求地址: /api/goods/home/


#### 请求方式: GET


#### 请求参数:

    
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'main_wheels': MainWheelSerializer(redis_main_wheels, many=True).data,
            'main_navs': MainNavSerializer(redis_main_navs, many=True).data,
            'main_mustbuys': MainMustBuySerializer(redis_main_mustbuys, many=True).data,
            'main_shops': MainShopSerializer(redis_main_shops, many=True).data,
            'main_shows': MainShowSerializer(redis_main_shows, many=True).data,
        }
    }
    

    }
    
#### 2.响应失败
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    data  响应数据  string  
        'main_wheels': 轮播图
        'main_navs': 导航图片
        'main_mustbuys': 图片
        'main_shops':  图片
        'main_shows': 展示图片
    