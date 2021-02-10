<template>
    <div>
        <div class="dropBox" @dragover.prevent @drop.stop.prevent="onDrop">
          <p><strong> Drop A File</strong></p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props:[
        'dropzoneFiles'
        ],
    data(){
        return {
            hi: 'hi',
        }
    },
    methods: {
    // Will be fired by our '@drop.stop.prevent'; in this case, when a file is dropped over our app
        onDrop(event) {
            const uploadedFiles = event.dataTransfer.files;
            // Do something with the dropped file
            console.log(uploadedFiles);
            for( var i = 0; i < uploadedFiles.length; i++ ){
            this.dropzoneFiles.push( uploadedFiles[i] );
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
        for( var i = 0; i < this.dropzoneFiles.length; i++ ){
          let file = this.dropzoneFiles[i];
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
                console.log(response);
                this.result = response.data;
                this.$router.push({name: 'dataSummary', params: {dataset: this.result}});
            })
          .catch((ex)=> {
              console.log("ERR!!!!! : ", ex);
              // this.$router.push('/dataSummary'); //delete later
          });
        }
  }
}
</script>

<style>
    .dropBox{
      width: 300px;
      height: 200px;
      border: 2px dashed #87ceeb;
      margin: 100px auto 0;
      text-align: center;
      padding-top: 20px;
    }

    .dropBox p {
      color:#444444;
    }
    
  
</style>