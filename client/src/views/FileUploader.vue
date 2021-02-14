<template>
  <div class="container">
    <div class="dropBox" @dragover.prevent @drop.stop.prevent="onDrop">
      <label><strong> Drop A File</strong></label>
      <p>OR</p>
      <!-- dropzone -->
        <!-- <dropzone :dropzoneFiles="files"> </dropzone> -->
      <!-- manual -->
      <div class="large-12 medium-12 small-12 cell">
        <label>Select File
          <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>
        </label>
      </div>
      <div class="large-12 medium-12 small-12 cell">
        <div v-for="(file, index) in files" class="file-listing" :key="index">{{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Remove</span></div>
      </div>
      <br>
      <br>
      <div class="large-12 medium-12 small-12 cell">
        <button v-on:click="submitFiles()">Submit</button>
      </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
// import Dropzone from '../components/Dropzone.vue';

  export default {
    /*
      Defines the data used by the component
    */
    data(){
      return {
        files: []
      }
    },
    components: {
        // dropzone: Dropzone,
    },
    /*
      Defines the method used by the component
    */
    methods: {
      /*
        Submits files to the server
      */
      submitFiles(){
        /*
          Initialize the form data
        */
        let formData = new FormData();
        /*
          Iteate over any file sent over appending the files
          to the form data.
        */
        for( var i = 0; i < this.files.length; i++ ){
          let file = this.files[i];
          formData.append('csv_data', file);
        }
        /*
          Make the request to the POST /select-files URL
        */
        axios.post( 'http://localhost:5000/dataupload',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
          }
        ).then((res) => {
                console.log(res);
                this.$router.push({path: 'dataSummary'});
            })
          .catch((ex)=> {
              console.log("ERR!!!!! : ", ex);
              // this.$router.push('/dataSummary'); //delete later
          });
      },
      /*
        Handles the uploading of files
      */
      handleFilesUpload(){
        let uploadedFiles = this.$refs.files.files;
        console.log(uploadedFiles);
        /*
          Adds the uploaded file to the files array
        */
        for( var i = 0; i < uploadedFiles.length; i++ ){
          this.files.push( uploadedFiles[i] );
        }
      },
      /*
        Removes a select file the user has uploaded
      */
      removeFile( key ){
        this.files.splice( key, 1 );
      },
      // dropzone methods
      onDrop(event) {
        const uploadedFiles = event.dataTransfer.files;
        // Do something with the dropped file
        // console.log(uploadedFiles);
        for( var i = 0; i < uploadedFiles.length; i++ ){
        this.files.push( uploadedFiles[i] );
      }
    //일단 바로 submit (추후 수정)
            /*
  Initialize the form data
*/
let formData = new FormData();
/*
  Iteate over any file sent over appending the files
  to the form data.
*/
for( var i = 0; i < this.files.length; i++ ){
  let file = this.files[i];
  formData.append('csv_data', file);
}
/*
  Make the request to the POST /select-files URL
*/
axios.post('http://localhost:5000/dataupload',
  formData,
  {
    headers: {
        'Content-Type': 'multipart/form-data'
    }
  }
).then((response) => {
        // console.log(response);
        this.result = response.data;
        this.$router.push({name: 'dataSummary', params: {dataset: this.result}});
    })
  .catch((ex)=> {
      console.log("ERR!!!!! : ", ex);
      // this.$router.push('/dataSummary'); //delete later
  });
},
//실험
  created() {
    console.log("Datatable created");
  },
  beforeUpdate(){
    console.log("Datatable beforecreate");
  },
  updated() {
    console.log("Datatable updated");
  },
  mounted() {
    console.log("Datatable mounted");
  },
    }
  }
</script>

<style>
  input[type="file"]{
    position: absolute;
    top: -500px;
  }
  div.file-listing{
    width: 200px;
  }
  span.remove-file{
    color: red;
    cursor: pointer;
    float: right;
  }
/* dropbox */
  .dropBox{
    width: 300px;
    height: 200px;
    border: 2px dashed #87ceeb;
    margin: 100px auto 0;
    text-align: center;
    padding-top: 20px;
    font-size: 17px;
    background-color: #fff;
}

.dropBox p {
  color:#333333;
  font-size: 14px;
}

.dropBox button{
  background-color: #87ceeb;
  border: none;
  color:#fff;
  width: 60px;
  height: 20px;
}
.dropbox button:hover {
    background-color: #8ab6ca;
    cursor: pointer;
}
</style>