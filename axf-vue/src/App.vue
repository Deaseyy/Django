<template>
  <div id="app">
    <router-view/>


    <!--四个按钮-->
    <footer>
      <router-link class="home" active-class="homeActive" to="/home"><dl><dt><span></span></dt><dd>首页</dd></dl></router-link>
      <router-link class="market" active-class="marketActive" to="/market"><dl><dt><span></span></dt><dd>闪送超市</dd></dl></router-link>
      <router-link class="cart" active-class="cartActive" to="/cart"><dl><dt><span></span></dt><dd>购物车</dd></dl></router-link>
      <router-link class="mine" active-class="mineActive" to="/mine"><dl><dt><span></span></dt><dd>我的</dd></dl></router-link>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
footer{
  position: fixed;
  display: flex;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1.5rem;
  background-color: #fff;
  border-top: 1px solid #f0f0f0;
  z-index: 10;
}

footer a{
  display: block;
  flex: 1;
  text-align: center;
  overflow: hidden!important;
}

footer dl dt {
  height: 0.777778rem;
  padding-top: 0.208333rem;
}


footer dl span {
  display: inline-block;
  width: 0.513889rem;
  height: 0.513889rem;
}


footer .home span{
  background: url(./assets/home.png) no-repeat;
  background-size: 0.513889rem;
}
footer .market span{
  background: url(./assets/market.png) no-repeat;
  background-size: 0.513889rem;
}
footer .cart span{
  background: url(./assets/cart.png) no-repeat;
  background-size: 0.513889rem;
}
footer .mine span{
  background: url(./assets/mine.png) no-repeat;
  background-size: 0.513889rem;
}

footer .homeActive span{
  background: url(./assets/home1.png) no-repeat;
  background-size: 0.513889rem;
}
footer .marketActive span{
  background: url(./assets/market1.png) no-repeat;
  background-size: 0.513889rem;
}
footer .cartActive span{
  background: url(./assets/cart1.png) no-repeat;
  background-size: 0.513889rem;
}
footer .mineActive span{
  background: url(./assets/mine1.png) no-repeat;
  background-size: 0.513889rem;
}
</style>
