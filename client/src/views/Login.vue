<template>
  <div class="wrapper">
    <p>Login</p>
    <div class="container">
      <div class="userName"><input type="input" value="Username" /></div>
      <div class="password"><input type="input" value="Password" /></div>
      <button class="signIn">Sign in</button>
    </div>
  </div>
</template>
<script>
export default {};
</script>
<style scoped>
.wrapper {
  width: 300px;
  height: 200px;
  border: 3px solid #87ceeb;
  margin: 100px auto 0;
  text-align: center;
  padding-top: 20px;
  font-size: 17px;
  background-color: #fff;
  border-radius: 5px;
}
.container {
  text-align: left;
  font-size: 13px;
}
.userName {
}
.userName input {
  margin: 0 auto;
  display: block;
  border: 0.5px solid #6b6b6b;
  margin-bottom: 5px;
}
.password input {
  margin: 0 auto;
  display: block;
  border: 0.5px solid #6b6b6b;
  margin-bottom: 5px;
}
.signIn {
  margin: 0 auto;
  display: block;
  border: 0.5px solid #6b6b6b;
  margin-bottom: 5px;
  color: aliceblue;
  background-color: #51bee9;
  font-weight: 500;
}
</style>
