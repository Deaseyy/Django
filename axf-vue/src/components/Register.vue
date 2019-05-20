<template>
  <div>
    <header>
      <span class="glyphicon glyphicon-chevron-left" @click='back()'></span>
    </header>

    <div class="container">
      <div>
          <div class="form-group">
              <label for="username_input">用户名</label>
              <input name="username" type="text" class="form-control" id="username_input" placeholder="请输入用户名" v-model="userName">
              <span id="username_info"></span>
          </div>
          <div class="form-group">
              <label for="email_input">邮箱</label>
              <input name="email" type="text" class="form-control" id="email_input" placeholder="请输入邮箱" v-model="email">
          </div>
          <div class="form-group">
              <label for="password_input">密码</label>
              <input name="password" type="password" class="form-control" id="password_input" placeholder="请输入密码" v-model="password">
          </div>
          <div class="form-group">
              <label for="password_confirm_input">确认密码</label>
              <input type="password" class="form-control" id="password_confirm_input" placeholder="请再次输入密码" v-model="password2">
          </div>
          <!-- <div class="form-group">
              <label for="icon_input">头像</label>
              <input name="icon" type="file" id="icon_input">
          </div> -->
          <button class="btn btn-success btn-block" @click="reigst()">注册</button>
      </div>
  </div>
  </div>

</template>

<script>
export default {
  name: 'reigster',
  methods:{
    back:function(){
      this.$router.back()
    },
    jump:function(page){
  		this.$router.push({path:'/'+page})
  	},
    reigst:function(){
      const params ={
        u_username:this.userName,
        u_password:this.password,
        u_password2:this.password2,
        u_email:this.email
      }
      this.axios.post('/api/user/auth/register/',{
        ...params
      }).then(response => {
        console.log(response.data);
        const resp = response.data;
        if(resp.code == 200) {
          const data = resp.data;
          if(data.user_id){
            this.$router.push({path:'/login'})
          }
        }else{
          this.$message({
            type:"error",
            message:resp.msg
          });
        }
      });
    },
    func:function(){
      return false
    }
  },
  data: function() {
    return {
      userName:'',
      email:'',
      password:'',
      password2:''
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
