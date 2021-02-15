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
import FileUploader from "./views/FileUploader.vue"
import Datatable from "./views/Datatable.vue"
import Login from "./views/Login.vue"

export default {
    name: "App",
    components:{
      Header,
      Login,
      FileUploader,
      Datatable,
    },
};

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans&family=Nunito+Sans&display=swap');
/* reset */
*{
  font-family: 'Nunito Sans', sans-serif, 'Noto Sans', sans-serif;
}
a{
  text-decoration: none;
}

body,p,span{
  margin: 0;
  padding: 0;
}
/* base.html */



</style>



