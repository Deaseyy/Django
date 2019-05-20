### 登陆接口


#### 请求地址: /api/user/auth/login/


#### 请求方式: POST


#### 请求参数:

    u_username  登陆账号 string 必填
    
    U_password  登录密码 string 必填
    
    
#### 响应

#### 1.响应成功

    {
        'code': 200,
        
        'msg': '请求成功',
        
        'data':{
        
            'token':'qweqweqweqwe'
        }
    }
    
#### 2.失败响应

    {
        'code': 1004,
        
        'msg': '账号不存在!'
    }
    
    {
        'code': 1005,
        
        'msg': '密码错误!'
    }
    
    {
        'code': 1006,
        
        'msg': '登陆参数有误!'
    }
      
#### 3.响应参数

    code 状态码  int
    
    msg 响应信息  string
    
    token 登陆标识符 string
    