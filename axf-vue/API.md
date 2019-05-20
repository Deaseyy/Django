# AXF

## 接口


### 首页
- /axf/home/

### 闪购
- 商品类型
  - /axf/foodtypes/
    - GET
- 商品列表
  - /axf/market/
    - GET
    - Params
      - typeid  一级类型
      - childcid 二级类型
      - order_rule 排序规则

### 个人中心
- 注册
  - /axf/users/
    - POST
    - Params
      - action=register
    - FormData
      - u_username
      - u_password
      - u_email
- 用户名预校验
  - /axf/users/
  - POST
  - Params
    - action=checkname
  - FormData
    - u_username
- 上传头像
  - /axf/users/
  - POST
  - FormData
    - u_icon
- 登陆
  - /axf/users/
    - POST
    - Params
      - action=login
    - FormData
      - u_username
      - u_password
- 获取个人中心信息
  - /axf/users/
    - GET
    - Params
      - token
  
  
### 购物车
- /axf/carts/
  - 通用Params
    - token
  - GET
  - 操作
    - action=add_to_cart
      - Params
        - goodsid
    - action=change_cart_status
      - Params
        - cartid
    - action=add_shopping
      - Params
        - cartid
    - action=sub_shopping
      - Params
        - cartid
    - all_select
      - Params
        - cart_list
          - 数据格式  id#id
    - all
      - 获取所有数据
      

### 订单
- /axf/orders/
  - 获取所有订单
    - GET
    - Params
      - token
  - 生成订单
    - POST
    - Params
      - token
  
- /axf/orders/(?P<pk>\d+)/
  - 获取单个订单
    - GET
    - Params
      - token

### 支付
- /axf/alipay/
  - GET
  - Params
    - token
    - action=pay
      - 调支付宝
    - action=payed
      - 通知付款完成


