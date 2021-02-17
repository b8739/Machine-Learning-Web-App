<template>
  <div id="app">
    <Header />
    <div id="content" class="content">
        <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Header from "./components/Header.vue"
// import Sidebar from "./components/Sidebar.vue"
import DataSummary from "./views/DataSummary.vue"

import Login from "./views/Login.vue"


export default {
    name: "App",

    components:{
      Header,
      // Login,
      // FileUploader,

      // Sidebar,
      DataSummary
    },
};

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans&family=Nunito+Sans&display=swap');
/* reset */
*{
  font-family: 'Nunito Sans', sans-serif, 'Noto Sans', sans-serif;
    margin: 0;
  padding: 0;
}
a{
  text-decoration: none;
}

body,p,span{

}
/* base.html */



</style>



