<template>
  <div>
    <img class="logo" src="../../assets/attic_logo.png" alt="" />
    <nav>
      <a href="#">Datasets</a>
      <a href="#">Preprocess</a>
      <a href="#">EDA</a>
      <a href="#">Modeling</a>
      <a href="#">Optimize</a>
    </nav>
  </div>
</template>

<style scoped>
/* reset */

body {
  background-color: #f0f0f0;
}
a {
  text-decoration: none;
}
/* base.html */
.logo {
  width: 4%;
  position: absolute;
  top: 15px;
  left: 20px;
}

nav {
  text-align: center;
  height: 60px;
  /* background-color: #87ceeb; */
  background-color: #f5f5f5;
  overflow: hidden;
  border-bottom: 0.5px solid #cccbcbe7;
}
nav a {
  display: inline-block;
  color: rgb(53, 53, 53);
  margin: 13px 60px 0 0;
  font-size: 20px;
}
/* index.html */
</style>
