<template>
  <div>
    <!-- Toolbars -->
    <!-- <v-toolbar> {{ updateTransaction }}</v-toolbar> -->

    <v-toolbar>
      {{ hiddenCols }}
      <v-toolbar-title class="mr-2">Undo/Redo:</v-toolbar-title>
      <label>Available Undo's:</label>
      <input id="undoInput" readonly class="undo-redo-input" />
      <label>Available Redo's:</label>
      <input id="redoInput" readonly class="undo-redo-input" />
      <v-btn small id="undoBtn" v-on:click="undo()">Undo</v-btn>
      <v-btn small id="redoBtn" v-on:click="redo()">Redo</v-btn>
      <v-btn small @click="filtercheck">filtercheck</v-btn>
    </v-toolbar>
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
      <v-toolbar-title class="mr-2"> Export CSV FIle:</v-toolbar-title>
      <v-btn small v-on:click="exportLoadedData()"
        >Download CSV file <label style="color:red">(Only currently loaded data)</label></v-btn
      >
      <v-btn small v-on:click="exportAllData()"
        >Download CSV file <label style="color:red">(All Data)</label></v-btn
      >
    </v-toolbar>
    <v-toolbar>
      <v-toolbar-title class="mr-2"> CRUD Action (Server Side):</v-toolbar-title>
      <v-btn small @click="updateRows()">Update Row</v-btn>
      <v-btn small @click="deleteRows()">Delete Row</v-btn>
      <v-btn small>Delete Column</v-btn>
      <v-btn small @click="dialog_colDisplay = true">Drop Column (Hide)</v-btn>
      <v-dialog v-model="dialog_colDisplay">
        <v-card>
          <v-container>
            <v-chip-group v-model="hiddenCols" multiple active-class="error--text" class="ml-10">
              <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex" label>
                {{ column }}
              </v-chip>
            </v-chip-group>
          </v-container>
          <v-card-actions>
            <v-btn @click="hideColumn">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- AG Grid -->
    </v-toolbar>
    <v-toolbar>
      <v-btn @click="dialog_colName = !dialog_colName">Change Column Name</v-btn>

      <v-dialog v-model="dialog_colName">
        <v-card>
          <v-container>
            <v-row>
              <v-col>From</v-col>
              <v-col>To</v-col>
            </v-row>
            <v-row v-for="(column, columnIndex) in columns" :key="columnIndex">
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
      <v-chip-group class="ml-10">
        <v-chip
          v-for="(dataGrid, gridIndex) in gridList"
          :key="gridIndex"
          v-bind="dynamicVchipProp(gridIndex)"
          @click="currentGrid = gridIndex"
          class="ml-1"
          close
          @click:close="removeGrid(gridIndex)"
          label
        >
          Grid {{ gridIndex }}
        </v-chip>
      </v-chip-group>
      <v-btn @click="createNewGrid"><v-icon>mdi-plus</v-icon> Add Dataframe</v-btn></v-toolbar
    >

    <ag-grid-vue
      v-for="(dataGrid, gridIndex) in gridList"
      :key="gridIndex"
      v-show="currentGrid == gridIndex"
      style="width: 1400px; height:800px"
      class="ag-theme-alpine"
      :columnDefs="columnDefs"
      :rowModelType="rowModelType"
      @grid-ready="onGridReady"
      :defaultColDef="defaultColDef"
      :components="components"
      :rowBuffer="rowBuffer"
      :rowSelection="rowSelection"
      :paginationPageSize="paginationPageSize"
      :cacheOverflowSize="cacheOverflowSize"
      :cacheBlockSize="cacheBlockSize"
      :maxConcurrentDatasourceRequests="maxConcurrentDatasourceRequests"
      :infiniteInitialRowCount="infiniteInitialRowCount"
      :modules="modules"
      :undoRedoCellEditing="true"
      :undoRedoCellEditingLimit="undoRedoCellEditingLimit"
      @first-data-rendered="onFirstDataRendered"
      @cell-value-changed="onCellValueChanged"
      :getRowStyle="getRowStyle"
      :maintainColumnOrder="true"
    >
    </ag-grid-vue>
  </div>
</template>

<script>
import Vue from "vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

import { AgGridVue } from "@ag-grid-community/vue";
import { InfiniteRowModelModule } from "@ag-grid-community/infinite-row-model";
import { CsvExportModule } from "@ag-grid-community/csv-export";
import "@ag-grid-community/core/dist/styles/ag-grid.css";
import "@ag-grid-community/core/dist/styles/ag-theme-alpine.css";
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      hiddenCols: [],
      vchipClickedProp: {
        color: "primary"
      },
      currentGrid: 0,
      gridList: [0],
      gridColumns: [],
      dialog_colDisplay: false,
      dialog_colName: false,
      modules: [InfiniteRowModelModule, CsvExportModule],

      gridApi: {},
      columnApi: null,

      components: null,
      rowBuffer: null,
      rowSelection: null,
      rowModelType: null,
      paginationPageSize: null,
      cacheOverflowSize: null,
      maxConcurrentDatasourceRequests: null,
      infiniteInitialRowCount: null,
      maxBlocksInCache: null,
      cacheBlockSize: 100,
      defaultColDef: {
        flex: 1,
        minWidth: 140,
        editable: true,
        resizable: true,
        // undo
        undoRedoCellEditingLimit: null
      },
      getRowStyle: null,
      updateTransaction: [],
      deleteTransaction: { 0: { row: [], column: [] } }
    };
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      datasetSize: state => state.initialData.datasetSize,
      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName
    }),

    columnDefs() {
      let array = [];
      this.columns.forEach(element => {
        let lowered = element.toString().toLowerCase();
        let filterObj = {
          field: element,
          filter: "agNumberColumnFilter"
          //     equals: (oldVal, newVal) => {
          //       console.log(oldVal);
          //       console.log(newVal);
          //       return true;
          // }
        };
        if (lowered == "id") {
          filterObj["maxWidth"] = 70;
          filterObj["editable"] = false;
        }
        if (
          lowered == "ts" ||
          lowered == "timeseries" ||
          lowered == "date" ||
          lowered == "datetime"
        ) {
          filterObj["filter"] = "agDateColumnFilter";
        }

        array.push(filterObj);
      });
      return array;
    }
  },
  components: {
    AgGridVue
  },

  methods: {
    hideColumn() {
      let finalState = [];
      let state = {};
      this.columns.forEach((element, index) => {
        if (this.hiddenCols.includes(index)) {
          state = { colId: element, hide: true };
        } else {
          state = { colId: element, hide: false };
        }
        finalState.push(state);
        console.log(finalState);
      });

      this.gridColumnApi.applyColumnState({
        state: finalState
      });
    },

    dynamicVchipProp(gridIndex) {
      if (gridIndex == this.currentGrid) {
        return this.vchipClickedProp;
      }
    },
    removeGrid(gridIndex) {
      this.gridList.splice(gridIndex, 1);
      Vue.delete(this.deleteTransaction, gridIndex);
      this.currentGrid = this.gridList.length - 1;
    },
    getColumnDefs() {},
    createNewGrid() {
      this.currentGrid = this.gridList.length;
      this.deleteTransaction[this.currentGrid] = { row: [], column: [] };

      this.gridList.push(0);
    },
    updateColumnName() {
      let changedElementIndex = [];
      this.gridColumns.forEach((element, index) => {
        if (element != this.columns[index]) {
          changedElementIndex.push(index);
        }
      });
      //headername 변경
      const columnDefs = this.columnDefs;
      changedElementIndex.forEach((element, index) => {
        columnDefs[element].headerName = this.gridColumns[element];
      });
      this.gridApi[this.currentGrid].setColumnDefs(columnDefs);
      //닫기
      this.dialog_colName = false;
    },
    updateRows() {
      let availableUndo = document.getElementById("undoInput").value;
      if (availableUndo != 0) {
        let path = "http://localhost:5000/updateRows";
        // axios
        axios({
          method: "post",
          url: path,
          data: {
            projectName: this.projectName,
            tableName: this.tableName,
            updateTransaction: this.updateTransaction
          }
        })
          .then(res => {
            console.log(res.data);
          })

          .catch(error => {
            console.error(error);
          });
      }
    },
    deleteRows() {
      let selectedRows = this.gridApi[this.currentGrid].getSelectedRows();
      selectedRows.forEach(element => {
        this.deleteTransaction[this.currentGrid]["row"].push(element["ID"]);
      });
      this.gridApi[this.currentGrid].refreshInfiniteCache();
      // let path = "http://localhost:5000/deleteRows";

      // // axios
      // axios({
      //   method: "post",
      //   url: path,
      //   data: {
      //     projectName: this.projectName,
      //     tableName: this.tableName,
      //     selectedIDs: selectedIDs
      //   }
      // })
      //   .then(res => {

      //     this.gridApi[this.currentGrid].refreshInfiniteCache();
      //     console.log(res.data);
      //   })

      //   .catch(error => {
      //     console.error(error);
      //   });
    },
    filtercheck() {
      let dd = this.gridApi[this.currentGrid].getFilterModel();
      console.log(dd);
    },

    getDisplayedRowCount() {
      var count = this.gridApi[this.currentGrid].getDisplayedRowCount();
      console.log("getDisplayedRowCount() => " + count);
    },
    printAllDisplayedRows() {
      var count = this.gridApi[this.currentGrid].getDisplayedRowCount();
      console.log("## printAllDisplayedRows");
      for (var i = 0; i < count; i++) {
        var rowNode = this.gridApi[this.currentGrid].getDisplayedRowAtIndex(i);
        console.log("row " + i + " is " + rowNode.data);
      }
    },
    getRowData() {
      var rowData = [];
      this.gridApi[this.currentGrid].forEachNode(function(node) {
        rowData.push(node.data);
      });
      console.log("Row Data:");
      console.log(rowData);
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
          tableName: this.tableName,
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
    onBtnUpdate() {
      this.dialog = true;

      document.querySelector("#csvResult").value = this.gridApi[this.currentGrid].getDataAsCsv(
        this.getParams()
      );
    },

    onGridReady(params) {
      console.log("on grid readty");
      this.gridApi[this.gridList.length - 1] = params.api;
      this.gridColumnApi = params.columnApi;
      let vm = this;
      updateData(vm);

      // function
      function updateData(vm) {
        let dataSource = {
          rowCount: null,

          getRows: function(params) {
            // console.log("asking for " + params.startRow + " to " + params.endRow);
            let filterModel = vm.gridApi[vm.currentGrid].getFilterModel();
            // console.log(vm.parseFilterModel(filterModel));
            filterModel = vm.parseFilterModel(filterModel);
            if (vm.deleteTransaction[vm.currentGrid] != undefined) {
              let ninFilter = { ID: { $nin: vm.deleteTransaction[vm.currentGrid]["row"] } };
              console.log(filterModel);
              filterModel.push(ninFilter);
            }

            console.log(filterModel);

            let path = "http://localhost:5000/infiniteRowModel";

            // axios
            axios({
              method: "post",
              url: path,
              data: {
                tableName: vm.tableName,
                projectName: vm.projectName,
                startRow: params.startRow.toString(),
                endRow: params.endRow.toString(),
                filterModel: filterModel
              }
            })
              .then(res => {
                // console.log(res.data);

                params.successCallback(res.data, vm.datasetSize);
              })

              .catch(error => {
                console.error(error);
              });
          }
        };

        params.api.setDatasource(dataSource);
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
    serverSideFilter(elementName, filterModel) {
      let condition = {};
      let filterType = filterModel.filterType;
      if (filterType == "number") {
        let filter = filterModel["filter"];

        switch (filterModel["type"]) {
          case "equals":
            condition[elementName] = filter;
            break;
          case "notEqual":
            condition[elementName] = { $ne: filter };
            break;
          case "lessThan":
            condition[elementName] = { $lt: filter };

            break;
          case "lessThanOrEqual":
            condition[elementName] = { $lte: filter };
            break;
          case "greaterThan":
            condition[elementName] = { $gt: filter };

            break;
          case "greaterThanOrEqual":
            condition[elementName] = { $gte: filter };

            break;
          case "inRange":
            condition[elementName] = { $gt: filter, $lt: filterModel["filterTo"] };

            break;
          default:
            break;
        }
      } else if (filterType == "date") {
        let filter = filterModel["dateFrom"];

        switch (filterModel["type"]) {
          case "equals":
            condition[elementName] = filter;
            break;
          case "notEqual":
            condition[elementName] = { $ne: filter };
            break;

          case "lessThan":
            condition[elementName] = { $lt: filter };
            break;

          case "greaterThan":
            condition[elementName] = { $gt: filter };

            break;

          case "inRange":
            condition[elementName] = { $gt: filter, $lt: filterModel["filterTo"] };

            break;
          case "dateFrom":
            break;
          default:
            break;
        }
      } else if (filterType == "text") {
        let filter = filterModel["filter"];

        switch (filterModel["type"]) {
          case "contains":
            break;
          case "notContains":
            break;
          case "startsWith":
            break;
          case "endsWith":
            break;
          default:
            break;
        }
      }

      return condition;
    },
    onFirstDataRendered() {
      setValue("#undoInput", 0);
      disable("#undoInput", true);
      disable("#undoBtn", true);
      setValue("#redoInput", 0);
      disable("#redoInput", true);
      disable("#redoBtn", true);
    },
    undoCalculate(params) {
      var undoSize = params.api.getCurrentUndoSize();
      setValue("#undoInput", undoSize);
      disable("#undoBtn", undoSize < 1);
      var redoSize = params.api.getCurrentRedoSize();
      setValue("#redoInput", redoSize);
      disable("#redoBtn", redoSize < 1);
    },
    onCellValueChanged(params) {
      this.undoCalculate(params);
      //transaction
      // 출력
      // console.log(`Field Name: ${params.colDef.field}`);
      // console.log(`ID: ${params.data.ID}`);
      // console.log(`New Value: ${params.newValue}`);
      // update object
      let update = {
        field: params.colDef.field,
        ID: params.data.ID,
        newValue: params.newValue
      };
      // 중복 요소 삭제
      let substringIndex = JSON.stringify(update).indexOf("newValue");
      this.updateTransaction.forEach((element, index) => {
        if (
          JSON.stringify(element).substring(0, substringIndex) ==
          JSON.stringify(update).substring(0, substringIndex)
        ) {
          Vue.delete(this.updateTransaction, index);
        }
      });

      // 배열에 입력

      this.updateTransaction.push(update);
    },
    undo() {
      this.gridApi[this.currentGrid].undoCellEditing();
    },
    redo() {
      this.gridApi[this.currentGrid].redoCellEditing();
    },
    getParams() {
      return { columnSeparator: this.getValue("#columnSeparator") };
    },
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
    }
  },
  mounted() {
    this.columns.forEach(element => {
      this.gridColumns.push(element);
    });
  },
  beforeMount() {
    // this.getRowStyle = params => {
    //   if (params.data == undefined) {
    //     return { display: "none" };
    //   }
    // };
    this.components = {
      loadingRenderer: params => {
        if (params.value !== undefined) {
          return params.value;
        } else {
          return '<img src="https://www.ag-grid.com/example-assets/loading.gif">';
        }
      }
    };
    this.rowBuffer = 0;
    this.rowSelection = "multiple";
    this.rowModelType = "infinite";
    this.paginationPageSize = 100;
    this.cacheOverflowSize = 2;
    this.maxConcurrentDatasourceRequests = 1;
    this.infiniteInitialRowCount = 1;

    this.undoRedoCellEditingLimit = 5;
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
