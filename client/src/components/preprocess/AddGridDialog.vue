<template>
  <v-dialog v-model="dialog" @click:outside="closeDialog" width="600">
    <v-card class="pa-4">
      <!-- <strong>columnModel</strong>{{ columnModel }}
      <br />
      <strong>datasetToLoad</strong>{{ datasetToLoad }} -->
      <v-tabs v-model="tab" align-with-title>
        <v-tabs-slider color="yellow"></v-tabs-slider>

        <v-tab
          v-for="(item, itemIndex) in tabMenu"
          :key="itemIndex"
          @click="resetLoadInfo"
          :disabled="itemIndex == 1"
        >
          {{ item }}
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab">
        <v-form ref="singleDataValidate">
          <v-tab-item>
            <v-card flat>
              <v-text-field
                label="Table Name"
                placeholder="입력하지 않으면 'unnamed'로 생성됩니다"
                v-model="datatableName"
              ></v-text-field>
              <v-select
                v-model="datasetToLoad"
                @input="loadColumns"
                :items="tableList"
                label="Select Dataset"
                clearable
                clear-icon
                :rules="datasetRule"
              ></v-select>
              <v-btn color="primary" outlined small @click="selectAllItems()"
                >Select All Columns</v-btn
              >
              <v-select
                v-model="columnModel[datasetToLoad]"
                :items="columnsForGrid[datasetToLoad]"
                chips
                multiple
                label="Select Columns (Only selected columns are loaded)"
                :rules="columnRule"
                return-object
              ></v-select>
            </v-card>
          </v-tab-item>
        </v-form>
        <v-tab-item>
          <v-card height="800px" flat>
            <v-text-field label="Table Name" v-model="datatableName"></v-text-field>

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
      datasetRule: [v => v.length != 0 || `Dataset은 필수 선택사항입니다.`],

      columnRule: [
        v => v.length != 0 || "Column은 필수 선택 사항입니다. (모두 Load할 시에 Select All Columns)"
      ],
      tabMenu: ["Load Single Dataset", "Load Integrated Datasets"],
      tab: null,
      merge_innerTab: null,
      // dataset load setting
      datasetToLoad: [],
      columnModel: {},
      datatableName: ""
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,
      projectName: state => state.initialData.projectName,
      columnsForGrid: state => state.aggrid.columnsForGrid,
      currentGrid: state => state.aggrid.currentGrid,
      gridList: state => state.aggrid.gridList
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
    ...mapMutations("aggrid", ["setDatatableName"]),
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
    getRandValue() {
      let gridIdList = this.gridList.map(function(gridInfo) {
        return gridInfo.randValue;
      });
      let randValue = Math.floor(Math.random() * (10 - 1) + 1);

      while (gridIdList.includes(randValue)) {
        randValue = Math.floor(Math.random() * (10 - 1) + 1);
      }
      return randValue;
    },
    onDialogConfirm() {
      if (!this.$refs.singleDataValidate.validate()) {
        alert("필수 설정이 완료되지 않았습니다.");
        return;
      }
      let randValue = this.getRandValue();
      let payload = {
        newGridID: randValue,
        datatableName: this.datatableName,
        datasetToLoad: this.datasetToLoad,
        columnModel: this.columnModel
      };

      this.createNewGrid(payload);
      if (this.tab == 0) {
        this.setGridType("AgGridSingle");
      } else {
        this.setGridType("AgGridMultiple");
      }
      // dialog 초기화
      this.resetLoadInfo();
      this.closeDialog();
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
      this.datatableName = "";
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
      let path = "http://localhost:5000/loadColumns";
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

      this.createNewGrid();
      this.setGridType("AgGridSingle");

      // dialog 초기화
      this.resetLoadInfo();
    });
  }
};
</script>
