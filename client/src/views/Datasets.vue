<template>
  <div>
    <Header />

    <v-container fluid class="pl-10 pt-10">
      <v-row align="start">
        <v-btn max-width="200px" class="mr-2" @click="openUploader" color="success">
          <v-icon left class="mdi-24">
            mdi-plus
          </v-icon>
          Add Dataset
        </v-btn>

        <v-btn max-width="200px" @click="deleteMode = !deleteMode" color="error">
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
            <v-row justify="end">
              <v-btn v-show="deleteMode" @click="dropTable(tableName)" x-small light
                >X</v-btn
              ></v-row
            >
            <v-row>
              <v-card-text class="font-weight-bold body-1 ">{{ tableName }}</v-card-text>
              <v-card-text class="font-weight-light body-2 pt-0">Created Date:</v-card-text>
              <v-card-text class="font-weight-thin caption">Creator:</v-card-text>
              <v-card-text class="font-weight-thin caption pt-0">Size:</v-card-text></v-row
            >
            <v-row justify="end">
              <v-btn small dark color="secondary" @click="enterDataset(tableName)"
                ><v-icon> mdi-subdirectory-arrow-right</v-icon>
              </v-btn>
            </v-row>
          </v-container>
        </v-sheet>
      </v-row>
      <!-- modal -->
      <DefineDataset />
      <Uploader />
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
      deleteMode: false,
      files: [],
      datasets: [1, 2]
    };
  },
  props: ["sidebarStatus"],
  components: { DefineDataset, Uploader },

  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    })
  },
  /*
      Defines the method used by the component
    */
  methods: {
    ...mapMutations("initialData", ["loadTableList"]),
    ...mapMutations("initialData", ["setNavStatus"]),
    ...mapMutations("initialData", ["resetState"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["saveTableName"]),

    enterDataset(tableName) {
      this.resetState();
      this.saveTableName(tableName);
      this.loadSummarizedData();
    },
    showTables() {
      let path = "http://localhost:5000/showTables";
      axios
        .get(path)
        .then(res => {
          // this.tableList = res.data;
          this.loadTableList(res.data);
        })
        .catch(error => {});
    },
    dropTable(tableName) {
      if (
        confirm("선택한 Dataset을 Database에서 삭제하시겠습니까? (다시 복구할 수 없습니다)") == true
      ) {
        let path = "http://localhost:5000/dropTable";
        axios
          .get(path, {
            params: {
              tableName: tableName
            }
          })
          .then(res => {
            this.showTables();
            this.deleteMode = false;
            console.log("Table Successfully Deleted");
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    openUploader() {
      eventBus.$emit("openUploader", true);
    }
  },
  //실험
  created() {
    console.log("created");
    this.showTables();
    this.setNavStatus("datasets");
    console.log("Datatable created");
  },
  mounted() {
    console.log("mounted");
    this.showTables();
    this.setNavStatus("datasets");
  }
};
</script>

<style scoped></style>
