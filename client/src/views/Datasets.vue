<template>
  <div>
    <Header />

    <v-container fluid class="pl-10 pt-10">
      <v-row align="start">
        <v-btn max-width="200px" class="mr-2" @click="enterDataset" color="primary">
          <v-icon left class="mdi-24">
            mdi-location-enter
          </v-icon>
          Enter project</v-btn
        >
        <v-btn max-width="200px" class="mr-2" @click="openUploader" color="success">
          <v-icon left class="mdi-24">
            mdi-plus
          </v-icon>
          Add Dataset
        </v-btn>

        <v-btn max-width="200px" @click="editMode = !editMode" color="error">
          <v-icon left class="mdi-24">
            mdi-trash-can
          </v-icon>
          Delete Dataset
        </v-btn>
      </v-row>
      <v-row>
        <v-sheet
          light
          outlined
          width="350px"
          v-for="(tableName, tableIndex) in tableList"
          :key="tableIndex"
          class="mr-5 mt-5 cursor-pointer"
        >
          <v-container>
            <v-row v-if="tableList" justify="end">
              <v-btn v-show="editMode" @click="dropTable(tableName)" x-small light>X</v-btn></v-row
            >
            <v-row>
              <v-card-text class="font-weight-bold body-1 ">{{ tableName }}</v-card-text>
              <v-card-text class="font-weight-light body-2 pt-0">Created Date:</v-card-text>
              <v-card-text class="font-weight-thin caption">Creator:</v-card-text>
              <v-card-text class="font-weight-thin caption pt-0">Size:</v-card-text></v-row
            >
          </v-container>
        </v-sheet>
      </v-row>
      <!-- modal -->
      <DefineDataset @onComplete="onCompleteEvent" :dialog.sync="dialog_define" />
      <Uploader :dialog.sync="dialog_uploader" />
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

import { eventBus } from "@/main";

import DefineDataset from "@/components/modal/DefineDataset";
import Uploader from "@/components/modal/Uploader";
export default {
  /*
      Defines the data used by the component
    */
  data() {
    return {
      dialog_uploader: false,
      dialog_define: false,
      editMode: false,
      files: [],
      datasets: [1, 2]
    };
  },
  props: ["sidebarStatus"],
  components: { DefineDataset, Uploader },

  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,

      projectName: state => state.initialData.projectName
    })
  },
  /*
      Defines the method used by the component
    */
  methods: {
    ...mapMutations("initialData", ["loadTableList"]),
    ...mapMutations("initialData", ["setNavStatus"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["setTableName"]),
    onCompleteEvent() {
      this.showTables();
      this.files = [];
      this.dialog_uploader = false;
      this.dialog_define = false;
    },
    enterDataset() {
      if (!this.editMode) {
        this.$router.push("/preprocess");

        // this.loadSummarizedData();
      }
    },
    showTables() {
      let path = "http://localhost:8000/showTables";
      axios({
        method: "post",
        url: path,
        data: { projectName: this.projectName }
      })
        .then(res => {
          this.loadTableList(res.data);
        })
        .catch(error => {
          console.error(error.response.data);
        });
    },
    dropTable(tableName) {
      if (
        confirm("선택한 Dataset을 Database에서 삭제하시겠습니까? (다시 복구할 수 없습니다)") == true
      ) {
        let path = "http://localhost:8000/dropTable";
        axios({
          method: "post",
          url: path,
          data: { projectName: this.projectName, tableName: tableName }
        })
          .then(res => {
            this.showTables();
            this.editMode = false;
            console.log("Table Successfully Deleted");
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    openUploader() {
      this.dialog_uploader = true;
    }
  },
  //실험
  created() {
    this.showTables();
    this.setNavStatus("datasets");
    eventBus.$on("dataUploadMode", modalStatus => {
      this.dialog_define = true;
    });
  },
  mounted() {
    // console.log("mounted");
    this.showTables();
    this.setNavStatus("datasets");
  }
};
</script>

<style scoped></style>
