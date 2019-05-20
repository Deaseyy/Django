<template>
  <div id="market">
      <h3 class="header">闪送超市</h3>
      <!-- 左边的大类型导航 -->
      <aside>
          <ul>
              <li v-for="item in foodtypes" :key="item.typeid" @click="selected(item)">
                  <a >{{ item.typename }}</a>
                  <span v-show="typeid == item.typeid" class="yellowSlide"></span>
              </li>
          </ul>
      </aside>


        <section>
            <nav>
                <ul>
                    <li id="all_types" @click="toggleTypeModal()"><span>全部分类 <span class="glyphicon glyphicon-chevron-down"></span></span></li>
                    <li id="sort_rule" @click="toggleRuleModal()"><span>综合排序 <span class="glyphicon glyphicon-chevron-down"></span></span></li>
                </ul>
            </nav>

            <menu>
                <ul>
                    <li v-for="item in goods_list" :key="item.id">
                        <a href="#">
                            <img :src="item.productimg" :alt="item.productlongname">
                            <div class="shoppingInfo">
                                <h6>{{ item.productlongname }}</h6>
                                <p class="detailTag">
                                    <span>精选</span>
                                    <span></span>
                                </p>
                                <p class="unit">{{ item.specifics }}</p>
                                <p class="price">
                                    <span>{{ item.price }}</span>
                                    <s>{{ item.marketprice }}</s>
                                </p>
                            </div>
                        </a>

                        <section>
                            <el-button class="steps" icon="el-icon-minus" circle @click="subShopping(item)" disabled></el-button>
                            <span>{{item.productnum}}</span>
                            <el-button class="steps" icon="el-icon-plus" circle @click="addShopping(item)" :disabled="false"></el-button>
                        </section>
                    </li>
                </ul>
                <div id="all_types_container" v-show="typeVisiable">
                    <div>
                      <a v-for="item in foodtype_childname_list" :key="item.id" @click="fetchTypeMark(item)">
                        <button :class="childcid == item.child_value ?'btn btn-success':'btn btn-default'">{{ item.child_name }}</button>
                      </a>
                    </div>
                </div>

                <div id="sort_rule_container" v-show="ruleVisiable">
                    <div >
                      <a v-for="item in order_rule_list" :key="item.id" @click="fetchRuleMark(item)">
                          <button :class="order_rule == item.order_value ?'btn btn-success':'btn btn-default'">{{ item.order_name }}</button>
                      </a>
                    </div>
                </div>
            </menu>
        </section>

    </div>
</template>

<script>

export default {
  name: 'Market',
  methods:{
    fetchMarket: function(){
      const params = {
        typeid:this.typeid,
        childcid:this.childcid,
        order_rule:this.order_rule
      }
      this.axios.get('/api/goods/market/',{
        params
      }).then(response => {
        const resp = response.data;
        console.log(resp.data.goods_list)
        if(resp.code == 200) {
          const data = resp.data;
          this.goods_list = data.goods_list;
          this.order_rule_list = data.order_rule_list;
          this.foodtype_childname_list = data.foodtype_childname_list;
        }
      });
    },
    fetchTypeMark:function(item){
      this.childcid = item.child_value;
      this.fetchMarket();
      this.toggleTypeModal();
    },
    fetchRuleMark:function(item){
      this.order_rule = item.order_value;
      this.fetchMarket();
      this.toggleRuleModal();
    },
    selected: function(item) {
      this.typeid = item.typeid;
      // 分类改变清空搜索条件
      this.childcid = '0';
      this.order_rule = '0';
      this.fetchMarket();
    },
    toggleTypeModal: function(){
      this.typeVisiable = !this.typeVisiable;
      this.ruleVisiable = false;
    },
    toggleRuleModal: function(){
      this.ruleVisiable = !this.ruleVisiable;
      this.typeVisiable = false;
    },
    subShopping:function(id){
      console.log(id)
    },
    addShopping: function (item){
      const params = {
        token:this.token,
        goodsid:item.id,
      }
      console.log(this.token)
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
          // const data = resp.data;
          // this.goods_list = data.goods_list;
          // this.order_rule_list = data.order_rule_list;
          // this.foodtype_childname_list = data.foodtype_childname_list;
          console.log(data);
        }else{
          this.$message({
            type:"error",
            message:resp.msg
          });
        }
      });
    }

  },
  data: function() {
    return {
      foodtypes:[],
      goods_list:[],
      order_rule_list:[],
      foodtype_childname_list:[],
      typeVisiable:false,
      ruleVisiable:false,
      typeid:'104749',
      order_rule:'0',
      childcid:'0',
      token:localStorage.getItem('axf_token')
    }
  },
  mounted: function (){

    this.axios.get('/api/goods/foodtype/').then(response => {
      const resp = response.data;
      console.log(resp)
      if(resp.code == 200) {
        const data = resp.data;
        this.foodtypes = data;
        this.typeid = data[0].typeid;
      }
    });
    this.fetchMarket();
  }
}
</script>

<style scoped>

/*
    闪购页面的数据容器
*/
#market {
    /* padding: 1.5rem 0;
    overflow: auto;
    height: 100%;
    width: 100%;
    position: fixed; */
}

.header {
	text-align: center;
	position: fixed;
	z-index: +100;
	width: 100%;
	border-bottom: 0.04rem solid lightgrey;
	line-height: 1.5rem;
	background: #fff;
	top: 0;
}


/*
    左侧大类型
*/
aside {
    width: 2.5rem;
    float: left;
    position: relative;
    background: #fafafa;
    overflow: auto;
}

aside ul {
    background: #fafafa;
}

aside ul li {
    list-style: none;
    text-align: center;
    border-bottom: 0.04rem solid #e0e0e0;
    line-height: 1.35rem;
    width: 2.25rem;
    position: relative;
    z-index: +1;
}

aside ul li a {
    display: block;
    font-size: 0.35rem;
    color: grey;
    z-index: +1;
}

.yellowSlide {
    background: yellow;
    width: 0.1rem;
    height: 0.7rem;
    position: absolute;
    left: 0;
    top: 0.3rem;
    display: block;
}

/*
    右侧商品数据内容
*/

div > section {
    background-color: #fafafa;
    width: 7.5rem;
    float: right;
    position: relative;
    height: 100%;
    overflow: auto;
    padding: 1.4rem 0 0;
    clear: none;
}

/*
    右侧顶部导航
*/
nav {
    top: 1.61rem;
    right: 0;
    position: fixed;
    z-index: +1;
    background: white;
    border-bottom: 0.04rem solid #e0e0e0;
}

nav ul {
    display: flex;
    background: white;
    height: 1.38rem;
    padding-top: 0.475rem;
}

nav ul li {
    text-align: center;
    width: 3.75rem;
    line-height: 0.475rem;
    font-size: 0.35rem;
    border-right: 0.04rem solid #e0e0e0;
    height: 0.5rem;
}

nav ul li:last-child {
    border: none;
}

nav ul li > span {
    width: 100%;
    height: 1rem;
    display: block;
}

/*
    商品数据
*/
section menu {
    height: 100%;
    position: relative;
    overflow: auto;
}

section menu ul {
    position: relative;
}

section menu ul li {
    background: white;
    border-bottom: 0.04rem solid #e0e0e0;
    position: relative;
}

section menu ul li a {
    display: block;
    height: 3rem;
}

section menu ul li a img {
    display: block;
    width: 2.8rem;
    float: left;
}

/*
    商品详细信息
*/
.shoppingInfo {
    width: 4.6rem;
    float: right;
    font-size: 0.35rem;
}

.shoppingInfo h6 {
    margin: 0.1rem 0 0;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 0.5rem;
    white-space: nowrap;
    font-weight: 500;
    font-size: 0.38rem;
}

/****细节标签*********/
.detailTag {
    margin: 0.2rem 0;
}

.detailTag span {
    border: 0.05rem solid red;
    border-radius: 0.15rem;
    padding: 0 0.1rem;
    color: white;
    background: red;
    margin-right: 0.3rem;
}

.detailTag span:first-child {
    background: white;
    color: red;
}

/******单位**********/
.unit {
    color: grey;
    position: absolute;
    bottom: 1rem;
}

.price {
    position: absolute;
    bottom: 0.15rem;
    font-weight: 200;
    margin: 0.2rem 0;
}

.price > span {
    padding: 0 0.35rem 0 0;
    color: red;
}

.price > span:before {
    content: "¥";
    color: red;
}

.price > s {
    color: grey;
}

.price > s:before{
    color: gray;
    content: "¥";
}

/*
    添加到购物车
*/
li > section {
    position: absolute;
    right: 0.4rem;
    bottom: 0.4rem;
    height: 0.75rem;
    border-radius: 1rem;
}

section > button {
    background: white;
    border: 1px solid orange;
    border-radius: 1111px;
    color: red;
    display: inline-block;
    text-align: center;
    line-height: 0.5rem;
    font-weight: 900;
    width: 0.5rem;
    height: 0.5rem;
}

.steps{
  padding: 0;
}

li > section > span {
    display: inline-block;
    width: 0.4rem;
    text-align: center;
    line-height: 0.4rem;
}

.subShopping, .addShopping {
    font-size: 0.4rem;
    font-weight: 100;
}


/*
    全部分类，综合排序
*/
section menu > div {
    position: fixed;
    top: 2.7rem;
    left: 2.55rem;
    width: 7.45rem;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    color: grey;
    /* display: none; */
}

section menu > div > div {
    background: white;
    padding-bottom: 0.3rem;
    text-align: left;
}

section menu > div > div > a > button {
    border: 0.04rem solid #e0e0e0;
    padding: 0.1rem 0.2rem;
    margin-left: 0.3rem;
    border-radius: 0.2rem;
    font-size: 0.375rem;
    display: inline-block;
    margin-top: 0.3rem;
}

</style>
