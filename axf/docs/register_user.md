### 注册接口


#### 请求地址: /api/user/auth/register/


#### 请求方式: POST


#### 请求参数

    u_username  注册账号  string  必填
    
    u_password  注册密码  string  必填
    
    u_password2  确认密码  string  必填
    
    email  注册邮箱  string  必填
    
#### 响应

##### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'user_id': user.id
            
        }
    }
    
##### 2.失败响应

    {
        'code': 1001,
        
        'msg': '注册账号已存在!'
    }
    
    {
        'code': 1002,
        
        'msg': '确认密码不一致!'
    }
    
    {
        'code': 1003,
        
        'msg': '邮箱格式有误!'
    }
    
    {
        'code': 1000,
        
        'msg': '注册参数有误!'
    }
      
##### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    user_id 用户id string