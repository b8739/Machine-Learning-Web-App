<template>
  <div style="width:100%">
    <!-- <v-toolbar>
      <v-toolbar-title class="mr-2 font-weight-bold subheading">Undo/Redo:</v-toolbar-title>
      <label>Available Undo's:</label>
      <input id="undoInput" :value="availableUndo" />
      <input id="undoInput" readonly class="undo-redo-input" />
      <label>Available Redo's:</label>
      <input id="redoInput" readonly class="undo-redo-input" />
      <v-btn outlined color="blue-grey" class="mr-2 " small id="undoBtn" v-on:click="undo()"
        >Undo</v-btn
      >
      <v-btn outlined color="blue-grey" class="mr-2 " small id="redoBtn" v-on:click="redo()"
        >Redo</v-btn
      >
    </v-toolbar> -->
    <v-btn @click="hidePanel = !hidePanel" small>Hide Panel</v-btn>

    <div v-show="hidePanel">
      <v-toolbar v-show="false">
        <div class="row">
          <label>columnSeparator = </label>
          <select id="columnSeparator">
            <option value="none">(default)</option>
            <option value="tab">tab</option>
            <option value="|">bar (|)</option>
          </select>
        </div>
      </v-toolbar>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading">
          Export CSV FIle:</v-toolbar-title
        >
        <v-btn class="mr-2" outlined color="blue-grey" small v-on:click="exportLoadedData()"
          >Download CSV file <label style="color:red">(Only currently loaded data)</label></v-btn
        >
        <v-btn class="mr-2" outlined color="blue-grey" small v-on:click="exportAllData()"
          >Download CSV file <label style="color:red">(All Data)</label></v-btn
        >
      </v-toolbar>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Edit Rows</v-toolbar-title>
        <v-btn class="mr-2" outlined color="blue-grey" small @click="updateRows()"
          >Update Row</v-btn
        >
        <v-btn class="mr-2" outlined color="blue-grey" small @click="deleteRows()"
          >Delete Row</v-btn
        >
      </v-toolbar>

      <v-dialog v-model="dialog_merge">
        <v-card>
          <v-card-text>현재는 데이터셋 2개만 합칠 수 있습니다.</v-card-text>

          <v-container>
            <v-select
              :items="items"
              item-text="name"
              item-value="tableName"
              v-model="tableToMerge"
              chips
              multiple
            ></v-select>
          </v-container>
          <v-card-actions>
            <v-btn @click="createMergedGrid">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Edit Columns</v-toolbar-title>
        <v-btn class="mr-2" outlined color="blue-grey" small @click="openDisplayDialog()"
          >Drop Column (Hide)</v-btn
        >
        <v-dialog v-model="dialog_colDisplay">
          <v-card>
            <v-container>
              <v-chip-group
                v-model="selectedColumns[currentGrid]"
                multiple
                active-class="error--text"
                class="ml-10"
              >
                <v-chip v-for="(column, columnIndex) in loadedColumns" :key="columnIndex" label>
                  {{ column }}
                </v-chip>
              </v-chip-group>
            </v-container>
            <v-card-actions>
              <v-btn @click="hideColumn">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>

      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading">
          Edit Column Info</v-toolbar-title
        >

        <v-btn color="blue-grey" outlined @click="openChangeNameDialog" small
          >Change Column Name</v-btn
        >

        <v-dialog v-model="dialog_colName">
          <v-card>
            <v-container>
              <v-row>
                <v-col>From</v-col>
                <v-col>To</v-col>
              </v-row>
              <v-row v-for="(column, columnIndex) in loadedColumns" :key="columnIndex">
                <v-col><v-text-field disabled :label="column"></v-text-field></v-col>
                <v-icon>mdi-arrow-right</v-icon>
                <v-col
                  ><v-text-field
                    v-model="gridColumns[columnIndex]"
                    :placeholder="column"
                  ></v-text-field
                ></v-col>
              </v-row>
            </v-container>
            <v-card-actions>
              <v-btn @click="updateColumnName">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Data Cleansing</v-toolbar-title>
        <v-btn
          color="blue-grey"
          disabled
          @click="dialog_nullToZero = true"
          class="mr-2 "
          outlined
          small
          >Null -> Zero</v-btn
        >
        <v-btn color="blue-grey" disabled @click="dialog_negativeToZero = true" outlined small
          >Negative -> Zero</v-btn
        >
      </v-toolbar>
      <!-- dialog -->
      <!-- <v-dialog v-model="dialog_nullToZero">
      <v-card>
        <v-container>
          <v-chip-group v-model="nullCols" multiple active-class="error--text" class="ml-10">
            <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex" label>
              {{ column }}
            </v-chip>
          </v-chip-group>
        </v-container>
        <v-card-actions>
          <v-btn @click="dialog_nullToZero = false">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialog_negativeToZero">
      <v-card>
        <v-container>
          <v-chip-group v-model="negativeCols" multiple active-class="error--text" class="ml-10">
            <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex" label>
              {{ column }}
            </v-chip>
          </v-chip-group>
        </v-container>
        <v-card-actions>
          <v-btn>Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog> -->
      <!-- <v-col> tableNameToLoad {{ tableNameToLoad }} </v-col>
    <v-col> currentGrid {{ currentGrid }} </v-col>
    <v-col> gridList {{ gridList }} </v-col>
    <v-col> tableToMerge {{ tableToMerge }} </v-col> -->

      <!-- <v-col> loadedColumns {{ loadedColumns }} </v-col>
    <v-col> gridColumns {{ gridColumns }} </v-col> -->
      <!-- <v-col> columnsToExclude {{ columnsToExclude }} </v-col> -->
      <!-- <v-col> gridList {{ gridList }}</v-col> -->

      <v-toolbar width="100%">
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Merge/Concat</v-toolbar-title>

        <v-btn class="mr-2" outlined color="blue-grey" small @click="dialog_merge = true"
          >Merge Grid</v-btn
        ></v-toolbar
      >
    </div>
    <v-toolbar>
      <v-chip-group class="ml-10">
        <v-chip
          v-for="(gridID, gridIndex) in gridList"
          :key="gridIndex"
          v-if="gridID != undefined"
          v-bind="dynamicVchipProp(gridIndex)"
          @click="setCurrentGrid(gridIndex), undoCalculate()"
          class="ml-1"
          close
          @click:close="removeGrid(gridID)"
          label
        >
          Data {{ gridID }}
        </v-chip>
      </v-chip-group>

      <v-btn class="mr-2" small @click="dialog_newGrid = true"
        ><v-icon>mdi-plus</v-icon> Add Datatable</v-btn
      >
      <v-btn class="mr-2" small @click="showAnalysis" outlined> Show Analysis</v-btn>
    </v-toolbar>
    <AgGridData
      v-for="(gridID, gridIndex) in gridList"
      :key="gridIndex"
      v-if="gridID != undefined"
      :gridID="gridID"
      :columnsToExclude="columnsToExclude[gridID]"
      :tableNameToLoad="tableNameToLoad[gridID]"
    />

    <AgGridSummary />
    <v-dialog v-model="dialog_newGrid" width="500">
      <v-card class="pa-4">
        <v-select
          v-model="tableNameToLoad[parseInt(currentGrid) + 1]"
          @input="loadColumns"
          :items="tableList"
          label="Select Dataset"
        ></v-select>
        <v-select
          v-model="columnsToExclude[parseInt(currentGrid) + 1]"
          :items="columnsForGrid"
          chips
          multiple
          label="Columns to Exclude (Load All Columns if not select any column)"
        ></v-select>

        <v-card-actions>
          <v-btn @click="createNewGrid()">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Vue from "vue";
import AgGridData from "@/components/preprocess/AgGridData.vue";
import AgGridSummary from "@/components/preprocess/AgGridSummary.vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

import axios from "axios";

export default {
  data() {
    return {
      vchipClickedProp: {
        color: "primary"
      },
      hidePanel: true,
      dialog_newGrid: true,
      dialog_colDisplay: false,
      dialog_colName: false,
      dialog_nullToZero: false,
      dialog_negativeToZero: false,
      dialog_merge: false,
      gridColumns: [],
      tableNameToLoad: {},
      columnsToExclude: {},
      columnsForGrid: [],
      loadedColumns: [],
      selectedColumns: [],
      tableToMerge: []
    };
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      tableList: state => state.initialData.tableList,
      datasetSize: state => state.initialData.datasetSize,
      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName,
      summarizedInfo: state => state.initialData.summarizedInfo,
      // gridapi
      gridApi: state => state.aggrid.gridApi,
      gridColumnApi: state => state.aggrid.gridColumnApi,
      currentGrid: state => state.aggrid.currentGrid,
      analysisDisplay: state => state.aggrid.analysisDisplay,
      hiddenCols: state => state.aggrid.hiddenCols,
      gridList: state => state.aggrid.gridList,
      // undo redo
      availableUndo: state => state.aggrid.availableUndo,
      availableRedo: state => state.aggrid.availableRedo,
      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      deleteTransaction: state => state.aggrid.deleteTransaction
    }),
    items() {
      let array = [];
      this.gridList.forEach(element => {
        let item = { name: "Data " + element, tableName: this.tableNameToLoad[element] };
        array.push(item);
      });
      return array;
    }
  },
  components: {
    AgGridData,
    AgGridSummary
  },
  created() {
    this.resetSummarizedInfo();
    this.resetAggrid();
  },
  methods: {
    ...mapMutations("initialData", ["resetSummarizedInfo"]),
    ...mapMutations("aggrid", ["addGridApi"]),
    ...mapMutations("aggrid", ["addGridColumnApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["addCurrentGrid"]),
    ...mapMutations("aggrid", ["setAnalysisDisplay"]),
    ...mapMutations("aggrid", ["resetAggrid"]),
    ...mapMutations("aggrid", ["addGridList"]),
    ...mapMutations("aggrid", ["setAvailableUndo"]),
    ...mapMutations("aggrid", ["setAvailableRedo"]),
    ...mapMutations("aggrid", ["addDeleteTransaction"]),
    ...mapActions("aggrid", ["removeGrid"]),

    openChangeNameDialog() {
      this.loadedColumns = [];
      let columns = this.getGridColumns();
      columns.forEach(element => {
        this.loadedColumns.push(element);
      });
      this.dialog_colName = !this.dialog_colName;
    },
    getGridColumns() {
      let vm = this;
      return this.gridColumnApi[this.currentGrid].getAllColumns().map(function(col) {
        return col.getColId();
      });
    },
    openDisplayDialog() {
      this.loadedColumns = [];
      let columns = this.getGridColumns();
      columns.forEach(element => {
        this.loadedColumns.push(element);
      });
      this.dialog_colDisplay = true;
    },

    // excel
    getValue(inputSelector) {
      var text = document.querySelector(inputSelector).value;
      switch (text) {
        case "string":
          return (
            'Here is a comma, and a some "quotes". You can see them using the\n' +
            "api.getDataAsCsv() button but they will not be visible when the downloaded\n" +
            "CSV file is opened in Excel because string content passed to\n" +
            "prependContent and appendContent is not escaped."
          );
        case "array":
          return [
            [],
            [
              {
                data: {
                  value: 'Here is a comma, and a some "quotes".',
                  type: "String"
                }
              }
            ],
            [
              {
                data: {
                  value:
                    "They are visible when the downloaded CSV file is opened in Excel because custom content is properly escaped (provided that suppressQuotes is not set to true)",
                  type: "String"
                }
              }
            ],
            [
              {
                data: {
                  value: "this cell:",
                  type: "String"
                },
                mergeAcross: 1
              },
              {
                data: {
                  value: "is empty because the first cell has mergeAcross=1",
                  type: "String"
                }
              }
            ],
            []
          ];
        case "none":
          return;
        default:
          return text;
      }
    },
    parseFilterModel(filterModel) {
      if (Object.keys(filterModel).length == 0) {
        return [];
      } else {
        let filterKeys = Object.keys(filterModel);
        let conditionList = [];
        filterKeys.forEach(element => {
          // YES operator
          let condition = {};

          if ("operator" in filterModel[element]) {
            let operator;
            if (filterModel[element]["operator"] == "AND") {
              operator = "$and";
            } else {
              operator = "$or";
            }
            condition[operator] = [];
            for (let i = 1; i < 3; i++) {
              let newCondition = this.serverSideFilter(
                element,
                filterModel[element]["condition" + i]
              );
              condition[operator].push(newCondition);
            }
          }
          // NO operator
          else {
            // no operator
            condition = this.serverSideFilter(element, filterModel[element]);
          }
          conditionList.push(condition);
        });
        return conditionList;
      }
    },
    getParams() {
      return { columnSeparator: this.getValue("#columnSeparator") };
    },
    exportAllData() {
      let filterModel = this.gridApi[this.currentGrid].getFilterModel();
      filterModel = this.parseFilterModel(filterModel);

      let path = "http://localhost:5000/exportAllData";
      // axios
      axios({
        method: "post",
        url: path,
        data: {
          projectName: this.projectName,
          tableName: this.tableNameToLoad[this.currentGrid],
          filterModel: filterModel
        }
      })
        .then(res => {
          console.log(res);
          const url = window.URL.createObjectURL(new Blob([res.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "file.csv"); //or any other extension
          document.body.appendChild(link);
          link.click();
        })

        .catch(error => {
          console.error(error);
        });
    },
    exportLoadedData() {
      let params = this.getParams();
      if (params.columnSeparator) {
        alert(
          "NOTE: you are downloading a file with non-standard separators - it may not render correctly in Excel."
        );
      }

      this.gridApi[this.currentGrid].exportDataAsCsv(params);
    },
    // undo
    undoCalculate() {
      var undoSize = this.gridApi[this.currentGrid].getCurrentUndoSize();
      this.setAvailableUndo(undoSize);
      var redoSize = this.gridApi[this.currentGrid].getCurrentRedoSize();
      this.setAvailableRedo(redoSize);
    },
    undo() {
      this.gridApi[this.currentGrid].undoCellEditing();
    },
    redo() {
      this.gridApi[this.currentGrid].redoCellEditing();
    },

    hideColumn() {
      //방법 1) columnExclude에 추가
      this.selectedColumns[this.currentGrid].forEach(element => {
        if (element != null) {
          this.columnsToExclude[this.currentGrid].push(this.loadedColumns[element]);
        }
      });
      this.dialog_colDisplay = false;
      this.selectedColumns = [];
      // 방법 2) hide
      // 문제: columnDef가 computed라서 원상복구됨

      // let finalState = [];
      // let state = {};

      // this.loadedColumns.forEach((element, index) => {
      //   if (this.hiddenCols[this.currentGrid].includes(index)) {
      //     state = { colId: element, hide: true };
      //   } else {
      //     state = { colId: element, hide: false };
      //   }
      //   finalState.push(state);
      //   console.log(finalState);
      // });

      // this.gridColumnApi[this.currentGrid].applyColumnState({
      //   state: finalState
      // });
    },
    updateColumnName() {
      const columnDefs = this.gridApi[this.currentGrid].getColumnDefs();

      let changedElementIndex = [];
      this.gridColumns.forEach((element, index) => {
        if (element != null) {
          columnDefs[index].headerName = element;
        }
      });

      this.gridApi[this.currentGrid].setColumnDefs(columnDefs);
      this.gridColumns = [];
      //닫기
      this.dialog_colName = false;
    },
    deleteRows() {
      let selectedRows = this.gridApi[this.currentGrid].getSelectedRows();
      this.addDeleteTransaction(selectedRows);
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    showAnalysis() {
      this.setAnalysisDisplay(!this.analysisDisplay);
    },
    loadColumns() {
      let path = "http://localhost:5000/loadColumns";
      axios({
        method: "post",
        url: path,
        data: {
          tableName: this.tableNameToLoad[parseInt(this.currentGrid) + 1],
          projectName: this.projectName
        }
      })
        .then(res => {
          this.columnsForGrid = res.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    createNewGrid() {
      this.addGridList();
      this.addCurrentGrid();
      this.setAnalysisDisplay(false);
    },
    createMergedGrid() {
      Vue.set(this.tableNameToLoad, parseInt(this.currentGrid) + 1, this.tableToMerge);
      this.columnsToExclude[parseInt(this.currentGrid) + 1] = [];
      this.addGridList();

      this.addCurrentGrid();
      this.setAnalysisDisplay(false);
    },

    dynamicVchipProp(gridIndex) {
      if (gridIndex == this.currentGrid) {
        return this.vchipClickedProp;
      }
    }
  }
};
</script>
<style scoped>
.button-group {
  padding-bottom: 4px;
  display: inline-block;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-size: 13px;
}
#undoInput {
  color: grey;
}
#redoInput {
  color: grey;
}
.undo-redo-input {
  width: 20px;
}

.undo-btn {
  margin-left: 20px;
}

.redo-btn {
  margin-left: 5px;
}
</style>
