<template>
  <div class="sidebar">
    sidebar
  </div>
</template>

<script>
export default {
  data(){
    return{
      
    }
  },
  props: ['sidebarStatus'],
}

</script>
<style>
  .sidebar{
    width: 300px;
    height:100vh;
    position: absolute;
    border-right: 1px solid #DEE4EA;
  }
  
</style>