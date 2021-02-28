<template>
  <div>
    <img class="logo" src="../assets/attic_logo.png" alt="" />
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
  background-color: #f2f2f2;
}
a {
  text-decoration: none;
}
/* base.html */
.logo {
  width: 4%;
  position: absolute;
  top: 15px;
  left: 12px;
}

nav {
  text-align: center;
  height: 60px;
  /* background-color: #87ceeb; */
  background-color: #97cfb7;
  overflow: hidden;
}
nav a {
  display: inline-block;
  color: #fafafa;
  margin: 13px 60px 0 0;
  font-size: 20px;
}
/* index.html */
</style>
