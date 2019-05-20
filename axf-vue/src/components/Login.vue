<template>
  <div>
    <header>
      <span class="glyphicon glyphicon-chevron-left" @click='back()'></span>
    </header>

    <div class="container">
        <form method="post" @submit.prevent>
            <div class="form-group">
                <label for="username_input">用户名</label>
                <input name="username" type="text" class="form-control" id="username_input" placeholder="用户名/邮箱" v-model="userName">
            </div>

            <div class="form-group">
                <label for="password_input">密码</label>
                <input name="password" type="password" class="form-control" id="password_input" placeholder="请输入密码" v-model="password">
            </div>
            <button type="submit" class="btn btn-success btn-block" @click="login()">登录</button>
        </form>
    </div>
  </div>

</template>

<script>
export default {
  name: 'login',
  methods:{
    back:function(){
      this.$router.back()
    },
    login:function(){
      const params ={
        u_username:this.userName,
        u_password:this.password,
      }
      this.axios.post('/api/user/auth/login/', {
        ...params
      }).then(response => {
        console.log(response.data.data.token)
        if(response.data.code == 200){
          this.$message({
            type:"success",
            message:"登录成功"
          });
          const token  = response.data.data.token;
          console.log( token )
          localStorage.setItem('axf_token',token);
          this.$router.push({path:'/'})
        }else{
          this.$message({
            type:"error",
            message:response.data.msg
          });
        }

      });
    }
  },
  data: function() {
    return {
      userName:'',
      password:''
    }
  },
  mounted: function (){

  }
}
</script>

<style scoped>
#app{
  margin-top: 0;
}
header{
    height: 1.5rem;
    background: darkorange;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    padding-left: 15px
}
.form-group{
  text-align: left;
}
</style>
