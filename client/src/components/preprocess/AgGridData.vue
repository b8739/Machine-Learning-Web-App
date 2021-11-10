<template>
  <div>
    <ag-grid-vue
      v-show="currentGrid == gridID && analysisDisplay == false"
      style="width: 1550px; height:800px"
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

// window.disable = function disable(id, disabled) {
//   document.querySelector(id).disabled = disabled;
// };

// window.setValue = function setValue(id, value) {
//   document.querySelector(id).value = value;
// };

export default {
  props: ["gridID", "tableNameToLoad", "columnsToExclude"],

  data() {
    return {
      nullCols: [],
      negativeCols: [],

      columnsForGrid: [],
      gridColumns: [],
      dialog_newGrid: true,
      dialog_colDisplay: false,
      dialog_colName: false,
      dialog_nullToZero: false,
      dialog_negativeToZero: false,
      modules: [InfiniteRowModelModule, CsvExportModule],

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
      getRowStyle: null
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
      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      deleteTransaction: state => state.aggrid.deleteTransaction
    }),
    finalColumns() {
      let array = [];
      this.columnsForGrid.forEach(element => {
        if (!this.columnsToExclude.includes(element)) {
          array.push(element);
        }
      });
      return array;
    },
    projectionModel() {
      let projection = {};

      return projection;
    },
    columnDefs() {
      let array = [];
      this.finalColumns.forEach(element => {
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
    ...mapMutations("aggrid", ["addGridApi"]),
    ...mapMutations("aggrid", ["addGridColumnApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("aggrid", ["setAnalysisDisplay"]),
    ...mapMutations("aggrid", ["setAvailableUndo"]),
    ...mapMutations("aggrid", ["setAvailableRedo"]),
    // transaction
    ...mapMutations("aggrid", ["deleteUpdateTransaction"]),
    ...mapMutations("aggrid", ["addUpdateTransaction"]),

    loadColumns(tableName) {
      let path = "http://localhost:5000/loadColumns";
      axios({
        method: "post",
        url: path,
        data: { tableName: tableName, projectName: this.projectName }
      })
        .then(res => {
          res.data.forEach(element => {
            this.columnsForGrid.push(element);
          });
        })
        .catch(error => {
          console.error(error);
        });
    },

    getColumnDefs() {},

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
            updateTransaction: this.updateTransaction[this.currentGrid]
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

    onBtnUpdate() {
      this.dialog = true;

      document.querySelector("#csvResult").value = this.gridApi[this.currentGrid].getDataAsCsv(
        this.getParams()
      );
    },

    onGridReady(params) {
      console.log("on grid readty");
      this.addGridApi(params.api);
      this.addGridColumnApi(params.columnApi);

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
              let ninFilter = { ID: { $nin: vm.deleteTransaction[vm.currentGrid] } };
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
                tableName: vm.tableNameToLoad,
                projectName: vm.projectName,
                startRow: params.startRow.toString(),
                endRow: params.endRow.toString(),
                filterModel: filterModel,
                columnsToExclude: vm.columnsToExclude
              }
            })
              .then(res => {
                console.log(res.data);
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
      // console.log("first");
      // setValue("#undoInput", 0);
      // disable("#undoInput", true);
      // disable("#undoBtn", true);
      // setValue("#redoInput", 0);
      // disable("#redoInput", true);
      // disable("#redoBtn", true);
    },
    undoCalculate(params) {
      var undoSize = this.gridApi[this.currentGrid].getCurrentUndoSize();
      this.setAvailableUndo(undoSize);
      var redoSize = this.gridApi[this.currentGrid].getCurrentRedoSize();
      this.setAvailableRedo(redoSize);

      // setValue("#undoInput", undoSize);
      // disable("#undoBtn", undoSize < 1);
      // setValue("#redoInput", redoSize);
      // disable("#redoBtn", redoSize < 1);
    },

    onCellValueChanged(params) {
      this.undoCalculate(params);
      console.log(params);
      let update = {
        field: params.colDef.field,
        ID: params.data.ID,
        newValue: parseFloat(params.newValue)
      };
      // 중복 요소 삭제
      let substringIndex = JSON.stringify(update).indexOf("newValue");
      this.updateTransaction[this.currentGrid].forEach((element, index) => {
        if (
          JSON.stringify(element).substring(0, substringIndex) ==
          JSON.stringify(update).substring(0, substringIndex)
        ) {
          this.deleteTransaction(index);
        }
      });

      // 배열에 입력

      this.addUpdateTransaction(update);
    }
  },
  created() {
    if (Array.isArray(this.tableNameToLoad) == true) {
      this.columnsToExclude = [];

      this.tableNameToLoad.forEach(element => {
        this.loadColumns(element);
      });
    } else {
      this.loadColumns(this.tableNameToLoad);
    }
  },
  mounted() {
    let payload = {
      tableName: this.tableNameToLoad,
      tableIndex: this.gridID,
      columnsToExclude: this.columnsToExclude
    };
    this.loadSummarizedData(payload);

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
