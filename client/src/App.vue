<template>
  <div id="app">
    Jo
    <div class="container">
      <!-- file Uploader -->
      <div class="fileUploader">
        <div class = "uploadGuide">
          <h2 style="color:#fff">Drag Your File Here</h2>
          <p style="color:#fff">OR</p>
        </div>
        <form method=POST enctype=multipart/form-data action="http://localhost:5000/dataupload" class="">
          <input type="file" name="csv_data">
          <input type="submit"  class="">
          <input type="reset"  value="Reset" class="">
        </form>
      </div>
    </div>
    <router-view/>
  </div>
</template>
<!-- style -->
<style>
#app {
  margin-top: 60px
}
</style>
