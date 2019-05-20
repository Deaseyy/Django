<template>
  <div id="cart">
    <h3>购物车</h3>
    <div class="full">
      <section>
        <ul>
          <li>收&nbsp;&nbsp;货&nbsp;&nbsp;人:&nbsp;童大宝</li>
          <li>电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话:&nbsp;12345678912</li>
          <li>地&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;址:&nbsp;大宝的家庭住址，不告诉你</li>
        </ul>

        <div class="bill">

          <p>闪送超市</p>
          <p>0元起送满30免运费22:00前可送达</p>
          <a href="#">凑单专区</a>

        </div>

        <div class="delivery">
          <span>收货时间</span>
          <span>一小时内送达</span>
          <a href="#">可预订&gt;</a>
        </div>

        <div class="delivery">
          <span>收获备注</span>
          <input type="text" placeholder="可输入100字以内的特殊要求">
        </div>

        <ul>
          <li class="menuList" v-for="item in carts" :key="item.id">
            <div class="confirm">
                                <span>
                                    <!--{% if cart.c_is_select %}-->
                                        <span>√</span>
                                        <!--{% else %}-->
                                        <!--<span></span>-->
                                    <!--{% endif %}-->
                                </span>
            </div>
            <a href="#">
              <img :src="item.c_goods.productimg" :alt="item.c_goods.productlongname">
              <p>{{ item.c_goods.productlongname }}</p>
              <p class="presentPrice">{{ item.c_goods.price }}</p>
            </a>


            <section>
              <button class="subShopping" @click="subShopping(item.c_goods)">-</button>
              <span>{{ item.c_goods_num }}</span>
              <button class="addShopping" @click="addShopping(item.c_goods)" >+</button>
            </section>

          </li>

        </ul>

        <div class="payTheBill">
          <div class="all_select">
                        <span>
                            <!--{% if is_all_select %}-->
                                <span>√</span>
                                <!--{% else %}-->
                                <!--<span></span>-->
                            <!--{% endif %}-->
                        </span>
          </div>

          <p>
            <span>全选</span>
            <span>共计:</span>
            <span id="total_price">{{ total_price }}</span>
          </p>

          <span id="make_order" @click="createOrder()">下单</span>
        </div>

      </section>


    </div>
  </div>
</template>

<script>
export default {
  name: 'Cart',
  methods:{
  	jump:function(page){
  		this.$router.push({path:'/home/'+page, query:{a:1}})
  	},
    createOrder:function(){
      const token = localStorage.getItem('axf_token');
      this.axios.post(`/api/orders/orders/?token=${token}`)
      .then(response => {
        if(response.data.code == 200){
          this.$message({
            type:"success",
            message:"下单成功"
          });
          this.$router.push({path:'/mine'});
        }
      });
    },
    addShopping: function (item){
      const params = {
        token:this.token,
        goodsid:item.id,
      }
      this.axios.post('/api/cart/cart/add_cart/',{
        ...params
      }).then(response => {
        const resp = response.data;
        console.log(resp)
        if(resp.code == 200) {
          this.$message({
            type:"success",
            message:resp.msg
          });
          this.$router.go(0);
          console.log(data);
        }else{
          this.$message({
            type:"error",
            message:resp.msg
          });
        }
      });
    },
    subShopping:function (item){
      const params = {
        token:this.token,
        goodsid:item.id,
      }
      this.axios.post('/api/cart/cart/sub_cart/',{
        ...params
      }).then(response => {
        const resp = response.data;
        console.log(resp)
        if(resp.code == 200) {
          this.$message({
            type:"success",
            message:resp.msg
          });
          this.$router.go(0);
          console.log(data);
        }else{
          this.$message({
            type:"error",
            message:resp.msg
          });
        }
      });
    },
  },
  data: function() {
    return {
      carts:[],
      token:localStorage.getItem('axf_token'),
      total_price:0
    }
  },
  mounted: function (){
    const params = {
      token:this.token,
    }
    this.axios.get('/api/cart/cart/',{
        params
    }).then(response => {
      const resp = response.data;
      console.log(resp)
      if(resp.code == 200) {
        const data = resp.data;
        this.carts = data.carts;
        this.total_price = data.total_price;
      }
    });
  }
}
</script>

<style scoped>


  #cart {
    z-index: +15;
    width: 100%;
    background: #fafafa;
    overflow: hidden;
    text-align: left;
  }

  h3 {
    text-align: center;
    position: fixed;
    z-index: +100;
    width: 100%;
    border-bottom: 0.04rem solid lightgrey;
    line-height: 1.5rem;
    background: #fff;
    top: 0;
  }



  .full > section {
    background: lightpink;
  }

  .full > section > ul {
    border: 0.2rem dashed lightgreen;
    border-width: 0.1rem 0;
    margin-bottom: 0.2rem;
  }

  .full > section > ul > li {
    padding-left: 0.3rem;
    line-height: 0.8rem;
    font-size: 0.375rem;
  }

  .clear:after {
    content: "";
    display: block;
    visibility: hidden;
    clear: both;
    height: 0;
  }

  .full > section > ul > li > div > p:last-child {
    float: right;
    width: 78%;
  }

  .full > section > ul > li > div > p:last-child > span {
    padding: 0.15rem;
  }

  .infoJustify {
    float: left;
    width: 20%;
    height: 0.8rem;
    overflow: hidden;
    text-align: justify;
  }

  .infoJustify > b {
    display: inline-block;
    width: 100%;
  }

  .change {
    float: right;
    padding-right: 0.2rem;
  }

  /**

   */
  .bill {
    line-height: 0.75rem;
    position: relative;
    border-bottom: 0.04rem solid lightgrey;
  }

  .bill > p {
    padding: 0 0.3rem;
    font-size: 0.3rem;
    color: green;
  }

  .bill > p:first-child:before {
    width: 0.2rem;
    height: 0.3rem;
    background: yellow;
    content: ".";
    color: yellow;
    margin-right: 0.2rem;
  }

  .bill > a {
    border: 0.05rem solid orangered;
    position: absolute;
    border-radius: 0.3rem;
    padding: 0 0.3rem;
    font-size: 0.35rem;
    line-height: 0.65rem;
    top: 0.2rem;
    right: 0.5rem;
  }

  /*************收货时间*****收货备注************/
  .delivery {
    line-height: 1.5rem;
    border-bottom: 0.04rem solid lightgrey;
    font-size: 0.4rem;
    padding: 0 0.3rem;
  }

  .delivery > span:first-child {
    padding-right: 0.3rem;
  }

  .delivery > span:nth-child(2) {
    color: orangered;
  }

  .delivery > a:last-child {
    float: right;
  }

  .delivery > input {
    height: 0.8rem;
    line-height: 0.8rem;
    border-radius: 0.1rem;
    border-width: 0.04rem;
    width: 70%;
  }

  /**************menu***************/
  .menuList {
    border-bottom: 0.04rem solid lightgrey;
    height: 2.5rem;
    position: relative;
  }

  .confirm, .all_select{
    padding: 0.95rem 0;
    width: 15%;
    height: 2.5rem;
    display: inline-block;
    box-sizing: border-box;
    text-align: center;
    float: left;
  }

  .confirm > span, .all_select > span {
    box-sizing: border-box;
    border: 0.04rem solid orange;
    background: white;
    display: inline-block;
    width: 0.6rem;
    height: 0.6rem;
    overflow: hidden;
    border-radius: 50%;
    line-height: 0.6rem;
  }

  .confirm > span > span, .all_select > span > span{
    background: yellow;
    font-size: 0.5rem;
    display: block;
  }

  .menuList > a {
    width: 84%;
    display: inline-block;
    font-size: 0.4rem;
    line-height: 1rem;
  }

  .menuList > a > img {
    margin-top: 0.25rem;
    width: 25%;
    height: 100%;
    float: left;
  }

  .menuList > a > p {
    width: 70%;
    height: 1rem;
    float: right;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .menuList > section {
    position: absolute;
    right: 0.4rem;
    bottom: 0.4rem;
    height: 0.75rem;
    border-radius: 1rem;
  }

  .menuList > section > button {
    background: white;
    border: 1px solid orange;
    border-radius: 1111px;
    color: red;
    display: inline-block;
    text-align: center;
    line-height: 0.65rem;
    font-weight: 900;
    width: 0.75rem;
    height: 0.75rem;
  }

  .menuList > section > span {
    display: inline-block;
    width: 0.5rem;
    text-align: center;
    line-height: 0.5rem;
    font-size: 0.4rem;
  }

  .presentPrice:before {
    content: "¥";
    font-size: 0.33rem;
  }

  /*************payTheBill 买单*************/
  .payTheBill {
    height: 1.5rem;
    position: relative;
  }

  .payTheBill .all_select {
    width: 10%;
    padding-top: 0.4rem;
    padding-left: 0.4rem;
  }

  .payTheBill > p {
    line-height: 1.5rem;
    text-indent: 0.3rem;
  }

  .payTheBill > p > span:first-child {
    padding-right: 0.8rem;
  }

  .payTheBill > p > span:last-child {
    padding-left: 0.3rem;
    color: red;
  }

  .payTheBill > p > span:last-child:before {
    content: "¥";
    font-size: 0.35rem;
  }

  .payTheBill > span {
    background: yellow;
    position: absolute;
    right: 0;
    line-height: 1.5rem;
    top: 0;
    padding: 0 0.7rem;
  }

</style>
