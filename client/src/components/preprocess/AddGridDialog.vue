<template>
  <v-dialog v-model="dialog" @click:outside="closeDialog" width="600">
    <v-card class="pa-4">
      <!-- <strong>columnModel</strong>{{ columnModel }}
      <br />
      <strong>datasetToLoad</strong>{{ datasetToLoad }} -->
      <v-tabs v-model="tab" align-with-title>
        <v-tabs-slider color="yellow"></v-tabs-slider>

        <v-tab v-for="(item, itemIndex) in tabMenu" :key="itemIndex" @click="resetLoadInfo">
          {{ item }}
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab">
        <v-tab-item>
          <v-card flat>
            <v-select
              v-model="datasetToLoad"
              @input="loadColumns"
              :items="tableList"
              label="Select Dataset"
              clearable
              clear-icon
            ></v-select>
            <v-btn small @click="selectAllItems()">Select All Columns</v-btn>
            <v-select
              v-model="columnModel[datasetToLoad]"
              :items="columnsForGrid[datasetToLoad]"
              chips
              multiple
              label="Select Columns (Only selected columns are loaded)"
            ></v-select>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card height="800px" flat>
            <v-select
              v-model="datasetToLoad"
              :items="tableList"
              label="Select Multiple Datasets"
              multiple
              chips
            ></v-select>
            <v-toolbar color="grey" dark flat>
              <v-toolbar-title>추가할 컬럼</v-toolbar-title>
              <template v-slot:extension>
                <v-tabs v-model="merge_innerTab" align-with-title>
                  <v-tabs-slider color="yellow"></v-tabs-slider>

                  <v-tab
                    v-for="(datasetName, tableIndex) in datasetToLoad"
                    :key="tableIndex"
                    @click.once="loadColumns(datasetName)"
                  >
                    {{ datasetName }}
                  </v-tab>
                </v-tabs>
              </template>
            </v-toolbar>
            <v-tabs-items v-model="merge_innerTab">
              <v-tab-item v-for="(datasetName, tableIndex) in datasetToLoad" :key="tableIndex">
                <v-card dark>
                  <v-container>
                    <v-row
                      v-for="(column, columnIndex) in columnsForGrid[datasetName]"
                      :key="columnIndex"
                      v-if="column != 'ID'"
                    >
                      <v-col cols="12">
                        <v-checkbox
                          @change="
                            booleanValue => onCheckboxChange(datasetName, column, booleanValue)
                          "
                          dense
                          :label="column"
                        ></v-checkbox
                      ></v-col> </v-row
                  ></v-container>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-tab-item>
      </v-tabs-items>

      <v-card-actions>
        <v-btn @click="onDialogConfirm()">Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import { eventBus } from "@/main";

import axios from "axios";

export default {
  data() {
    return {
      tabMenu: ["Load Single Dataset", "Load Integrated Datasets"],
      tab: null,
      merge_innerTab: null,
      // dataset load setting
      datasetToLoad: [],
      columnModel: {}
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,
      projectName: state => state.initialData.projectName,
      columnsForGrid: state => state.aggrid.columnsForGrid,
      currentGrid: state => state.aggrid.currentGrid
    }),
    columnsWithSelectAll() {
      let array = [];
      array.push("ID");
      this.columnsForGrid[this.datasetToLoad].forEach(element => {
        array.push(element);
      });
      return array;
    }
  },
  props: ["dialog"],
  methods: {
    ...mapMutations("aggrid", ["setDatasetToLoad"]),
    ...mapMutations("aggrid", ["setColumnModel"]),
    ...mapMutations("aggrid", ["setColumnsForGrid"]),
    ...mapMutations("aggrid", ["onTabChange"]),
    ...mapMutations("aggrid", ["setGridType"]),
    ...mapActions("aggrid", ["createNewGrid"]),
    selectAllItems() {
      if (
        this.columnModel[this.datasetToLoad].length ==
        this.columnsForGrid[this.datasetToLoad].length
      ) {
        this.columnModel[this.datasetToLoad].splice(0);
      } else {
        this.columnModel[this.datasetToLoad].splice(0);

        this.columnsForGrid[this.datasetToLoad].forEach(element => {
          this.columnModel[this.datasetToLoad].push(element);
        });
      }
    },
    onDialogConfirm() {
      // load 정보 vuex에 전송
      this.setDatasetToLoad(this.datasetToLoad);
      this.setColumnModel(this.columnModel);
      if (this.tab == 0) {
        this.setGridType("AgGridSingle");
      } else {
        this.setGridType("AgGridMultiple");
      }
      this.createNewGrid();
      // dialog 초기화
      this.resetLoadInfo();
      //columnsToExclude랑 datasetToload
    },
    onCheckboxChange(datasetName, column, booleanValue) {
      if (this.columnModel[datasetName] == undefined) {
        this.columnModel[datasetName] = [];
      }
      if (booleanValue) {
        this.columnModel[datasetName].push(column);
      } else {
        var indexToRemove = this.columnModel[datasetName].indexOf(column);
        this.columnModel[datasetName].splice(indexToRemove, 1);
      }
      console.log(this.columnModel);
    },
    resetLoadInfo() {
      this.columnModel = {};
      this.datasetToLoad = [];
    },
    closeDialog() {
      this.resetLoadInfo();
      this.$emit("update:dialog", false);
    },
    loadColumns(datasetName) {
      if (this.tab == 0) {
        this.onTabChange();
      }
      if (this.columnModel[datasetName] == undefined) {
        this.columnModel[datasetName] = [];
      }
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadColumns";
      // let tableName = this.tableNameToLoad[parseInt(this.currentGrid) + 1];
      axios({
        method: "post",
        url: path,
        data: {
          tableName: datasetName,
          projectName: this.projectName
        }
      })
        .then(res => {
          let payload = { tableName: datasetName, data: res.data };
          this.setColumnsForGrid(payload);
          // this.columnsForGrid = res.data;
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    eventBus.$on("shortcut", dialogStatus => {
      // load 정보 vuex에 전송
      this.setDatasetToLoad("boston");
      this.setColumnModel({ boston: ["CRIM", "CHAS", "ZN", "INDUS"] });
      this.setGridType("AgGridSingle");

      this.createNewGrid();
      // dialog 초기화
      this.resetLoadInfo();
    });
  }
};
</script>
