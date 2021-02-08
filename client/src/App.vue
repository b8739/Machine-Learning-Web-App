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

export default {
    name: "App",
    components:{
      Header,
      FileUploader,
      Datatable,
    },
};

</script>
<style>
</style>



