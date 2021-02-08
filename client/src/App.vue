<template>
  <div id="app">
    <div id="content" class="content">
        <router-view></router-view>
    </div>
  </div>
</template>

<script>
import FileUploader from "./views/FileUploader.vue"

export default {
    name: "App",
    components:{
      FileUploader,
    },
};

</script>
<style>
#app {
  margin-top: 60px
}
</style>



