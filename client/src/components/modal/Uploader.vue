<template>
  <v-dialog v-model="dialog" width="30vw">
    <v-card outlined class="py-10" @dragover.prevent @drop.stop.prevent="onDrop">
      <v-row justify="center" class="ma-0">
        <v-icon color="teal" class="mdi-48px"> mdi-briefcase-upload </v-icon>
        <v-col cols="12">
          <p class="body-2 text-center ">
            <strong> Drag And Drop Your File Here </strong>
          </p>
          <p class="text-center caption font-weight-thin">File Supported: csv</p>
          <p class="text-center subheading font-weight-light">or</p>
        </v-col>
        <label>
          Browse Files
          <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()" />
        </label>
      </v-row>
      <v-row justify="center" align="center" class="ma-0">
        <v-col cols="12" v-for="(file, index) in files" class="file-listing" :key="index">
          <p class="text-center">{{ file.name }}</p>
          <span class="text-center remove-file" v-on:click="removeFile(key)">
            Remove
          </span>
        </v-col>
        <!-- <v-btn class="mb-3" v-on:click="submitFiles()">Submit</v-btn> -->
      </v-row>
    </v-card>
  </v-dialog>
</template>
<script>
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

import { eventBus } from "@/main";

export default {
  /*
      Defines the data used by the component
    */
  data() {
    return {
      files: [],
      datasets: [1, 2],
      dialog: false
    };
  },

  /*
      Defines the method used by the component
    */
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),

    /*
        Submits files to the server
      */
    submitFiles() {
      /*
          Initialize the form data
        */
      let formData = new FormData();
      /*
          Iteate over any file sent over appending the files
          to the form data.
        */
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("csv_data", file);
      }
      /*
          Make the request to the POST /select-files URL
        */
      axios
        .post("http://localhost:5000/dataupload", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(res => {
          this.loadSummarizedInfo(res);
        })
        .catch(ex => {
          console.log("ERR!!!!! : ", ex);
        });
    },
    /*
        Handles the uploading of files
      */
    handleFilesUpload() {
      let uploadedFiles = this.$refs.files.files;
      // console.log(uploadedFiles);
      /*
          Adds the uploaded file to the files array
        */
      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push(uploadedFiles[i]);
      }
    },
    /*
        Removes a select file the user has uploaded
      */
    removeFile(key) {
      this.files.splice(key, 1);
    },
    // dropzone methods
    onDrop(event) {
      const uploadedFiles = event.dataTransfer.files;
      // Do something with the dropped file
      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push(uploadedFiles[i]);
      }
      let formData = new FormData();
      /*
  Iteate over any file sent over appending the files
  to the form data.
*/
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("csv_data", file);
      }
      /*
  Make the request to the POST /select-files URL
*/
      eventBus.$emit("dataUploadMode", true);
      eventBus.$emit("formData", formData);
    }
    //실험
  },
  created() {
    eventBus.$on("openUploader", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>

<style scoped>
input[type="file"] {
  /* position: absolute;
  top: -500px; */
  display: none;
}
div.file-listing {
  width: 200px;
}
span.remove-file {
  color: red;
  cursor: pointer;
  float: right;
}

label {
  display: block;
  width: 10vw;
  border: 1px solid #009688;
  color: #009688;

  line-height: 2.5em;
  border-radius: 4px;

  /* font */
  font-size: 1em;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.0892857143em;
  font-weight: 500;
  text-indent: 0.0892857143em;
  font-size: 0.875rem;

  cursor: pointer;
}
label:hover {
  background-color: #e0f1f0;
}
</style>
