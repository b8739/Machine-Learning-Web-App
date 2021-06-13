<template>
  <div>
    <Header />
    <v-app>
      <v-container fluid class="pl-10 pt-10">
        <v-row align="start" no-gutter dense>
          <v-col cols="1">
            <v-btn @click="openUploader" block color="success">
              <v-icon left class="mdi-24">
                mdi-plus
              </v-icon>
              Add Dataset
            </v-btn>
          </v-col>
          <v-col cols="9"></v-col>
          <v-sheet
            light
            outlined
            width="350px"
            height="300px"
            v-for="(tableName, tableIndex) in tableList"
            :key="tableIndex"
            class="mr-5 mt-5 cursor-pointer"
            @click="enterDataset"
          >
            <v-card-text class="font-weight-bold body-1">{{ tableName }}</v-card-text>
            <v-card-text class="font-weight-light body-2 pt-0">Created Date:</v-card-text>
            <v-card-text class="font-weight-thin caption">Creator:</v-card-text>
            <v-card-text class="font-weight-thin caption pt-0">Size:</v-card-text>
          </v-sheet>
        </v-row>
        <!-- modal -->
        <DefineDataset />
        <Uploader />
      </v-container>
    </v-app>
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
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapMutations("initialData", ["loadTableList"]),
    ...mapMutations("initialData", ["setNavStatus"]),

    enterDataset() {
      this.$router.push({ name: "dataSummary" });
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
