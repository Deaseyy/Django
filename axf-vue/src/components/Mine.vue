<template>
  <div id="mine">
    <div class="fixed">
        <span>
            <img v-if="false" class="u_icon" src="1111" alt="1212">
            <span v-else class="glyphicon glyphicon-user"></span>
        </span>

        <p v-if="token">{{user_info.u_username}}</p>
        <p v-else id="not_login" @click="jump('login')">未登录</p>

        <p>
            <span class="glyphicon glyphicon-fire"></span>
            <span>等级</span>
        </p>

        <div v-show="!token" id="regis" @click="jump('register')">注册</div>

        <p>
            <span class="glyphicon glyphicon-heart"></span>
            <span>商品收藏</span>
        </p>

    </div>

    <div class="mine">
        <p>
          <span>全部订单</span>
          <router-link to="/orders">全部订单</router-link>
        </p>

        <nav id="nav">
            <ul>
                <li id="not_pay">
                    <span v-show='true' class="badge">
                      {{orders_not_pay_num}}
                    </span>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-usd"></span>
                        </dt>
                        <dd>待付款</dd>
                    </dl>
                </li>
                <li>
                    <span class="badge" v-show='true'>
                      {{orders_not_send_num}}
                    </span>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-envelope"></span>
                        </dt>
                        <dd>待收货</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-pencil"></span>
                        </dt>
                        <dd>待评价</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-retweet"></span>
                        </dt>
                        <dd>退款/售后</dd>
                    </dl>
                </li>
            </ul>
        </nav>
        <menu>
            <ul>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-bullhorn"></span>
                        </dt>
                        <dd>积分商城</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-credit-card"></span>
                        </dt>
                        <dd>优惠卷</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-import"></span>
                        </dt>
                        <dd>收货地址</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-phone-alt"></span>
                        </dt>
                        <dd>客服反馈</dd>
                    </dl>
                </li>
                <li>
                    <dl>
                        <dt>
                            <span class="glyphicon glyphicon-asterisk"></span>
                        </dt>
                        <dd>关于我们</dd>
                    </dl>
                </li>
            </ul>
        </menu>
        <p v-show='token'>
            <a @click="logout()">退出</a>
        </p>

    </div>

</div>
</template>

<script>
export default {
  name: 'Market',
  methods:{
    jump:function(page){
  		this.$router.push({path:'/'+page})
  	},
    logout:function(){
      localStorage.removeItem('axf_token');
      this.$router.push({path:'/login'})
    }
  },
  data: function() {
    return {
      user_info:'',
      token:localStorage.getItem('axf_token'),
      orders_not_pay_num:0,
      orders_not_send_num:0
    }
  },
  mounted: function (){
    this.axios.get('/api/user/auth/?token=' + this.token).then(response => {
      console.log(response.data)
      if(response.data.code == 200) {
        const { data } = response.data;
        this.user_info = data.user_info;
        this.orders_not_pay_num = data.orders_not_pay_num;
        this.orders_not_send_num = data.orders_not_send_num;
      }
    }, response => {
      // error callback
    });
  }
}
</script>

<style scoped>
  /*
      底部图标和文字
  */
  footer .mine_icon span {
      background: url(/static/img/mine_selected.png) no-repeat;
      background-size: 0.513889rem;
  }

  footer .mine_icon dd {
      color: orange;
  }

  /*
      内容容器
  */
  #mine {
      width: 100%;
      height: 100%;
      position: absolute;
      z-index: +10;
      background: whitesmoke;
      overflow: hidden;
      padding-top: calc(4rem - 60px);
      padding-bottom: 1.5rem;
  }

  .fixed {
      position: fixed;
      top: 0;
      width: 100%;
      height: 4rem;
      background: pink;
      padding-top: 0.5rem;
      text-align: left;
  }

  .fixed > span {
      display: block;
      width: 2rem;
      height: 2rem;
      float: left;
      margin: 0 0.3rem 0;
      font-size: 1.5rem;
      color: black;
      background: white;
      text-align: center;
      border-radius: 50%;
      line-height: 1.8rem;
  }

  .fixed > span > .u_icon{
      width: 2rem;
      height: 2rem;
      border-radius: 50%;
  }

  .fixed p {
      margin-bottom: 0.5rem;
      font-size: 0.5rem;
      color: white;
  }

  .fixed p span:first-child {
      color: black;
  }

  .fixed p span:last-child {
      color: red;
      display: inline-block;
      text-indent: 0.3rem;
  }

  #regis {
      position: absolute;
      right: 0.3rem;
      top: 1.3rem;
      color: white;
      font-size: 1rem;
  }

  .fixed p:last-child {
      background: #f0e000;
      width: 100%;
      position: absolute;
      text-align: center;
      bottom: 0;
      margin-bottom: 0;
      font-size: 0.4rem;
      line-height: 0.5rem;
      height: 1rem;
  }

  .fixed p:last-child span {
      margin: 0.2rem 0;
  }


  .fixed p:last-child span:first-child {
      color: red;
  }

  .fixed p:last-child span:last-child {
      color: white;
  }


  /*
      我的中的各种
  */

  .mine {
      width: 100%;
      height: 100%;
      overflow: auto;
      padding-bottom: 1.5rem;
      font-size: 0.4rem;
  }

  .mine p {
      line-height: 1.5rem;
      padding: 0 0.3rem;
      background: white;
      border-bottom: 0.04rem solid lightyellow;
      display: flex;
      justify-content: space-between;
  }

  .mine p a {
      color: grey;
      float: right;
  }



  .mine #nav, .mine menu {
      padding: 0.5rem 0 0.3rem;
      margin-bottom: 0.4rem;
      background: white;
  }

  .mine #nav ul, .mine menu ul {
      display: flex;
      justify-content: space-around;
  }

  .mine #nav ul li, .mine menu ul li{
      position: relative;
  }

  .mine #nav ul li dl, .mine menu ul li dl {
      text-align: center;
  }

  .mine #nav ul li > span {
      right: 0;
      position: absolute;
      color: white;
      background: red;
  }

  .mine #nav ul li dl dt, .mine menu ul li dl dt {
      width: 100%;
      line-height: 1rem;
  }

  .mine #nav ul li dl dt span, .mine menu ul li dl dt span {
      font-size: 0.5rem;
  }

  .mine menu ul {
      flex-wrap: wrap;
  }

  .mine menu ul li {
      width: 25%;
  }

  .mine menu ul li:last-child {
      width: 100%;
  }

  .mine menu ul li:last-child dl {
      width: 25%;
  }

  .mine p:last-child > a {
      line-height: 1.5rem;
      text-align: center;
      width: 100%;
      display: block;
      float: none;
  }
</style>
