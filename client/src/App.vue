<template>
  <div id="app">
    <div id="content" class="content">
      header!
        <router-view></router-view>
    </div>
  </div>
</template>

<script>
import FileUploader from "./views/FileUploader.vue"
import Datatable from "./views/Datatable.vue"

export default {
    name: "App",
    components:{
      FileUploader,
      Datatable,
    },
};

</script>
<style>
#app {
  margin-top: 60px
}
</style>



