<template>
  <div>
    <label class="list_order" id="info_f304ba748b4cc1faa1cdc419651b5c17_0_0__1_0"></label>
    <div class="viewport">
      <!--页头-->
      <header class="navbar">
        <div class="nav_main">
          <a>商品订单</a>
        </div>
      </header>
      <nav class="ol_select_bar">
        <ul>
          <a :class="{hover:order_all}" @click="order_select('all')"><li>全部</li></a>
          <a :class="{hover:order_pay}" @click="order_select('not_pay')"><li>待付款</li></a>
          <a :class="{hover:order_send}" @click="order_select('not_send')"><li>待收货</li></a>
        </ul>
      </nav>
      <div class="block" v-for="goods in order_goods">
        <div class="order_list">
          <div class="cart_item prd_ebook">
            <a onclick="" v-for="g in goods.order_goods_info">
              <div :style="">
                <img :src="g.o_goods.productimg" class="fl pro_pic" alt="">
              </div>
              <div class="detail">
                <div class="fr prd_state">
                  <div class="prd_state_title">
                    <!--交易成功-->
                  </div>
                </div>
                <p class="fl prd_tit">
                  {{ g.o_goods.productname }}
                </p>
              </div>
            </a>
            <div class="detail2">
              <span>　总价：</span><span class="order_price">￥{{ goods.o_price }}</span>
            </div>
            <!--操作按键-->
            <div class="detail3">
              <a v-if="goods.o_status">确认收货</a>
              <a v-else>支付</a>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
    export default {
      name: "List",
      data () {
        return {
          order_goods: '',
          order_all: true,
          order_pay:'',
          order_send:''
        }
      },
      mounted () {
        var params = {
          token: localStorage.getItem('axf_token')
        }
        this.axios.get('/api/orders/orders/', { params }).then(res => {
          var resp = res.data
          if(resp.code == 200){
            console.log(resp.data[0].order_goods_info)
            this.order_goods = resp.data
          }

        }).catch(err => {
          console.log(err)
        })
      },
      methods: {
        order_select: function (msg) {
          if(msg == 'all'){
            var params = {
              o_status: 'all',
              token: localStorage.getItem('axf_token')
            }
            this.order_all = true
            this.order_pay = false
            this.order_send = false
          }else if (msg == 'not_pay'){
            var params = {
              o_status: 'not_pay',
              token: localStorage.getItem('axf_token')
            }
            this.order_all = false
            this.order_pay = true
            this.order_send = false
          }else{
            var params = {
              o_status: 'not_send',
              token: localStorage.getItem('axf_token')
            }
            this.order_all = false
            this.order_pay = false
            this.order_send = true
          }
          this.axios.get('/api/orders/orders/', { params }).then(res => {
            console.log(res.data)
            var resp = res.data
            this.order_goods = resp.data
          })
        }
      }
    }
</script>

<style scoped>
  /*html5 reset*/

  .navbar {
    -webkit-box-sizing: border-box;
    position: fixed;
    width: 100%;
    height: 1.5rem;
    z-index: 999;
    top: 0;
    left: 0;
    background:#fff;
  }

  .navbar div.nav_main {
    line-height:1.55rem;
    height:1.5rem;
    border-bottom:1px solid #dfdfdf;
    font-size:0.5rem;
    text-align:center;
    position:relative;
    overflow:inherit;
    font-weight: 10;
  }

  nav{ position:fixed;top:1.35rem; width:100%;height:1.9rem; border-bottom:1px solid #dddddd;z-index:5;}
  nav ul{ background:#fff;height:1.9rem;}
  nav ul a li {float:left;width:33%;}
  nav ul li { line-height:1.75rem; display:block; margin:0 auto; width:3.6rem;text-align:center; font-size:0.4rem;font-weight: 10;color:#464646}
  nav ul li:first-child a{ width:2.4rem;}
  nav ul a.hover li{border-bottom:3px solid #ff463c;color:#ff463c}

  .block {
    border-top:1px solid #ebebeb;
    margin-top:1.3rem;
    background:#fff;
    overflow: auto;
    border-bottom: 1px solid #CFCFCF;
  }

  /*订单内容*/
  .order_list .cart_item{border-bottom: 1px solid #E1E1E1;}
  .order_list .cart_item .detail{ padding:0.4rem 0 1.7rem 0.3rem;height:1.1rem}
  .order_list .cart_item .prd_state{color:#ff463c; padding-right:1.45rem;}
  .order_list .cart_item .prd_state .prd_state_title{padding-bottom:0.1rem; float: right;}
  .order_list .cart_item .prd_state img{width:2rem;padding-left:0.8rem;}
  .order_list .cart_item .prd_tit{ width:56%;word-wrap:break-word; margin-top: 0px;}
  .order_list .cart_item .detail2{line-height:1rem; text-align:right; font-size:0.4rem; border-top:1px solid #e1e1e1;margin:0 1.45rem}
  .order_list .cart_item .detail2 span:first-child{color:#ff463c}
  .order_list .cart_item .detail2 span:nth-child(2){color:#a0a0a0}
  .order_list .cart_item .detail2 span:last-child{color:#000;font-size:0.5rem }
  .order_list .ebook_tag{top:0;left:0;}

  .detail3{text-align:right; border-top:0px solid #e1e1e1;margin:0 0.45rem}
  .detail3 a{;height:1rem; width:3.1rem; text-align:center; line-height:1rem;border:0.1rem solid #464646; display:block; float:right; margin-left:.6rem;color:#464646;border-radius:.3rem; font-size:0.5rem}

</style>
