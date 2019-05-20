<template>
	<div id="home">
		<h3 class="header">首页</h3>
		<!-- 首页顶部轮播 -->
    <div class="block">
      <el-carousel height="150px" indicator-position="none">
        <el-carousel-item v-for="item in main_wheels" :key="item.id">
          <img :src="item.img" alt="">
        </el-carousel-item>
      </el-carousel>
    </div>
		<!-- 首页顶部的导航 -->
    <div class="topMenu">
        <nav>
            <ul>
              <li v-for="item in main_navs" :key="item.id">
                  <img :src="item.img" :alt="item.name">
                  <span>{{ item.name }}</span>
              </li>
            </ul>
        </nav>
    </div>
		<!-- 首页必购 -->
    <div class="swiper-container" id="swiperMenu">
        <ul class="swiper-wrapper">
          <li class="swiper-slide" v-for="item in main_mustbuys" :key="item.id">
              <img :src="item.img" :alt="item.name">
          </li>
        </ul>
    </div>
		<!-- 首页商店 -->
    <div class="shop_container">
        <h2>
            <img :src="main_shops.length ? main_shops[0].img :''" >
        </h2>

        <fieldset>
            <a href="#" v-for="item in main_shops.slice(1,3)" :key="item.id">
                <img :src="item.img" :alt="item.name">
            </a>
        </fieldset>

         <ul>
            <li v-for="item in main_shops.slice(3,7)" :key="item.id">
                <img :src="item.img" :alt="item.name">
                <span>{{ item.name }}</span>
            </li>
        </ul>

        <ol>
            <li v-for="item in main_shops.slice(7)" :key="item.id">
                <a href="#">
                    <img :src="item.img" :alt="item.name">
                </a>
            </li>
        </ol>
    </div>

		<!-- 首页主显示 -->
    <ul>
        <li class="mainInfo" v-for="item in main_shows" :key="item.id">
            <section>
                <h3>{{ item.name }}
                    <a href="#">更多&gt;</a>
                    <span></span>
                </h3>

                <div>
                    <a href="#">
                        <img :src="item.img" :alt="item.name">
                    </a>
                </div>

                <ul>
                    <li>
                        <a href="#">
                            <img :src="item.img1" :alt="item.longname1">
                            <p class="description">{{ item.longname1 }}</p>
                            <span>{{ item.price1 }}</span>
                            <s>{{ item.marketprice1 }}</s>
                        </a>
                        <button>
                            <span>+</span>
                        </button>
                    </li>
                    <li>
                        <a href="#">
                            <img :src="item.img2" :alt="item.longname2">
                            <p class="description">{{ item.longname2 }}</p>
                            <span>{{ item.price2 }}</span>
                            <s>{{ item.marketprice2 }}</s>
                        </a>
                        <button>
                            <span>+</span>
                        </button>
                    </li>
                    <li>
                        <a href="#">
                            <img :src="item.img3" :alt="item.longname3">
                            <p class="description">{{ item.longname3 }}</p>
                            <span>{{ item.price3 }}</span>
                            <s>{{ item.marketprice3 }}</s>
                        </a>
                        <button>
                            <span>+</span>
                        </button>
                    </li>
                </ul>

            </section>
        </li>
    </ul>
	</div>
</template>

<script>

export default {
  name: 'Home',
  methods:{
  	func:function(){
  		console.log("--------------")
  	},
  	jump:function(page){
  		this.$router.push({path:'/home/'+page, query:{a:1}})
  	}
  },
  data: function() {
    return {
      main_wheels:[],
      main_navs:[],
      main_mustbuys:[],
			main_shops:[],
			main_shows:[]
    }
  },
  created:function(){

  },
  mounted: function (){



    this.axios.get('/api/goods/home/').then(response => {
      const resp = response.data;
      console.log(resp)
      if(resp.code == 200) {
        const data = resp.data;
        this.main_wheels = data.main_wheels;
        this.main_navs = data.main_navs;
				this.main_mustbuys = data.main_mustbuys;
				this.main_shops = data.main_shops;
        this.main_shows = data.main_shows;
      }
    }, response => {
      console.log(response);
      // error callback
    });
  },
  updated:function(){
    var mySwiper = new Swiper ('#swiperMenu', {
          slidesPerView: 3
        })
  }
}
</script>

<style scoped>
#home{
	padding-bottom: 3rem;
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

.el-carousel__item img {
  width: 100%;
  height: 100%;
}

.el-carousel__item:nth-child(2n) {
   background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
   background-color: #d3dce6;
}
/*
    顶部导航
*/

.topMenu {
    padding-bottom: 0;
}

.topMenu nav {
    margin: 0.35rem 0 0.26rem;
    background: white;
}

.topMenu nav ul {
    display: flex;
}

.topMenu nav li {
    width: 2.5rem;
    text-align: center;
    font-size: 0.35rem;
}

.topMenu nav li img {
    width: 2.5rem;
}
/*
    必购
*/

#swiperMenu {
    width: 100%;
}

#swiperMenu li img {
    width: 100%;
}

/*
    商店
*/
.shop_container {
    background: white;
    margin-top: 0.3rem;
}

.shop_container h2 img {
    width: 100%;
}

.shop_container fieldset {
    border: none;
    padding: 0;
}

.shop_container fieldset > a {
    display: inline-block;
    width: 49%;
}

.shop_container fieldset img {
    width: 100%;
}

.shop_container ul {
    display: flex;
}

.shop_container ul li {
    width: 2.5rem;
    text-align: center;
    font-size: 0.35rem;
}

.shop_container ul li img {
    width: 2.5rem;
}

.shop_container ol {
    display: flex;
    flex-wrap: wrap;
}

.shop_container ol li {
    list-style: none;
    width: 5rem;
}

.shop_container > ol a {
    display: block;
}

.shop_container ol a img {
    width: 100%;
}

/*
    主显示
*/
.mainInfo {
    background-color: white;
}

.mainInfo > section {
    margin: 0.2rem auto 0;
    padding: 0.2rem 0;
    width: 9.2rem;
}

.mainInfo > section h3 {
    text-align: center;
    height: 1.2rem;
    position: relative;
}

.mainInfo > section h3 a {
    color: grey;
    font-size: 0.3rem;
    line-height: 0rem;
    position: absolute;
    right: 0.1rem;
    display: block;
}

.mainInfo > section h3 > span {
    background-color: yellow;
    width: 0.6rem;
    height: 0.1rem;
    position: absolute;
    bottom: 0.25rem;
    left: 4.3rem;
}

.mainInfo > section > div > a > img {
    width: 100%;
}

.mainInfo > section > ul {
    display: flex;
    justify-content: space-around;
}

.mainInfo > section > ul > li {
    width: 2.6rem;
    position: relative;
}

.mainInfo > section > ul > li > a {
    font-size: 0.4rem;
    color: red;
    display: block;
}


.mainInfo > section > ul > li > a > span:before {
    color: red;
    content: "¥";
}

.mainInfo > section > ul > li > a > img {
    width: 100%;
}

.mainInfo > section > ul > li > a > s {
    color: grey;
    font-size: 0.3rem;
}

.mainInfo > section > ul > li > a > s:before {
    color: grey;
    content: "¥";
}

.mainInfo .description {
    font-size: 0.37rem;
    color: black;
    width: 100%;
    display: block;
    line-height: 1.2em;
    height: 2.4em;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
}

.mainInfo > section > ul > li > button {
    border: 1px solid lightgrey;
    border-radius: 1111px;
    width: 0.6rem;
    height: 0.6rem;
    display: block;
    line-height: 0.0rem;
    text-align: center;
    color: orangered;
    font-size: 0.6rem;
    position: absolute;
    right: 0;
    top: 3.6rem;
    background: white;
}

.mainInfo > section > ul > li > button > span {
    position: relative;
    /*top: -0.05rem;*/
    margin: auto;
}
</style>
