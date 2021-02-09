<template>
    <div>
        <div class="dropBox" @dragover.prevent @drop.stop.prevent="onDrop"></div>
    </div>
</template>

<style>
    .dropBox{
        width: 300px;
        height: 200px;
        background-color: #123;
    }
  
</style>

<script>
export default {
    data(){
        return {
            hi: 'hi',
        }
    },
    methods: {
    // Will be fired by our '@drop.stop.prevent'; in this case, when a file is dropped over our app
    onDrop(event) {
      const file = event.dataTransfer.files[0];
      // Do something with the dropped file
      console.log(file)
    }
  }
}
</script>