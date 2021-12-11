<template>
  <v-dialog @click:outside="removeFile(), closeDialog()" v-model="dialog" width="30vw">
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
  props: ["dialog"],
  /*
      Defines the data used by the component
    */
  data() {
    return {
      files: []
    };
  },

  /*
      Defines the method used by the component
    */
  computed: {},
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapMutations("initialData", ["setTableName"]),

    /*
        Submits files to the server
      */
    //사실상 사용하지 않고, DefineDataset에서 데이터 업로드
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
        let fileType = file.substring(file.length - 3);
        if (fileType != "csv") {
          this.errorMessage = `File type '${fileType}' is not supported, please upload 'csv' type file`;
          return false;
        }
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
          localStorage.clear();
          console.log(res.data);
          this.setTableName(this.tableName);

          // this.loadSummarizedInfo(res);
        })
        .catch(ex => {
          this.errorMessage = ex;
          console.log("ERROR : ", ex);
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
    closeDialog() {
      this.$emit("update:dialog", false);
    },
    // dropzone methods
    onDrop(event) {
      const uploadedFiles = event.dataTransfer.files;
      // Do something with the dropped file
      let fileName = uploadedFiles[0].name;
      let fileType = fileName.substring(fileName.length - 3);
      if (fileType != "csv") {
        alert(`Only csv file type is supported (requested file type: ${fileType})`);
        this.removeFile();
        return;
      }
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
      eventBus.$emit("dataUploadMode", true); //define dataset dialog 열기
      eventBus.$emit("formData", formData);
    }
    //실험
  },
  created() {
    eventBus.$on("removeFile", status => {
      this.removeFile();
    });
  },
  mounted() {
    this.errorMessage = "";
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
