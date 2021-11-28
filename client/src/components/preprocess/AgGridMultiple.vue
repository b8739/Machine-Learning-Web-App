<template>
  <div>
    Multiple
    <v-btn @click="getFinalColumns">getFinalColumns</v-btn>
    <ag-grid-vue
      v-show="currentGrid == gridID && viewMode == 'table'"
      style="width: 1550px; height:600px"
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
       onColumnMoved: onColumnMoved,
    >
    </ag-grid-vue>
  </div>
</template>

<script>
import Vue from "vue";
import AgGridMix from "@/components/preprocess/AgGridMix";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import axios from "axios";
import { InfiniteRowModelModule } from "@ag-grid-community/infinite-row-model";
import { CsvExportModule } from "@ag-grid-community/csv-export";
import "@ag-grid-community/core/dist/styles/ag-grid.css";
import "@ag-grid-community/core/dist/styles/ag-theme-alpine.css";

// window.disable = function disable(id, disabled) {
//   document.querySelector(id).disabled = disabled;
// };

// window.setValue = function setValue(id, value) {
//   document.querySelector(id).value = value;
// };

export default {
  mixins: [AgGridMix],
  props: ["gridID", "datasetToLoad", "columnModel", "gridType"],

  data() {
    return {
      gridColumns: [],
      modules: [InfiniteRowModelModule, CsvExportModule],
      finalColumns: []
    };
  },
  computed: {
    // finalColumns() {
    //   let finalArray = [];
    //   // if (Object.keys(this.columnModel).length == 0) {
    //   //   return [];
    //   // } else {
    //   loop1: for (let i = 0; i < this.columnsForGrid.length; i++) {
    //     let column = this.columnsForGrid[i];
    //     loop2: for (let j = 0; j < this.datasetToLoad.length; j++) {
    //       let datasetName = this.datasetToLoad[j];
    //       if (this.columnModel[datasetName].includes(column)) {
    //         continue loop1;
    //       }
    //     }
    //     finalArray.push(column);
    //   }
    //   // }

    //   return finalArray;
    // },
    projectionModel() {
      let projection = {};
      return projection;
    },
    columnDefs() {
      let array = [];
      //ID
      let filterObj = {
        field: "ID",
        filter: "agNumberColumnFilter",
        maxWidth: 70,
        editable: false
      };

      array.push(filterObj);
      // 나머지
      this.datasetToLoad.forEach(element => {
        this.columnModel[element].forEach(element => {
          let lowered = element.toString().toLowerCase();
          let filterObj = {
            field: element,
            filter: "agNumberColumnFilter"
          };

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
      });

      return array;
    }
  },

  methods: {
    getFinalColumns() {
      loop1: for (let i = 0; i < this.columnsForGrid.length; i++) {
        let column = this.columnsForGrid[i];
        loop2: for (let j = 0; j < this.datasetToLoad.length; j++) {
          let datasetName = this.datasetToLoad[j];
          if (this.columnModel[datasetName].includes(column)) {
            continue loop1;
          }
        }
        this.finalColumns.push(column);
      }

      return this.finalColumns;
    },

    // transaction
    ...mapMutations("aggrid", ["revertUpdate"]),
    ...mapMutations("aggrid", ["addNewUpdate"]),

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

    onGridReady(params) {
      console.log("on multiple grid readty");
      let payload = { api: params.api, gridID: this.gridID };
      this.addGridApi(payload);
      payload = { api: params.columnApi, gridID: this.gridID };
      this.addGridColumnApi(payload);
      let vm = this;
      updateData(vm);
      function updateData(vm) {
        let dataSource = {
          rowCount: null,
          getRows: function(params) {
            console.log("asking for " + params.startRow + " to " + params.endRow);
            // 1) Get Filter Model
            let filterModel = vm.gridApi[vm.currentGrid].getFilterModel();
            filterModel = vm.parseFilterModel(filterModel);
            // 2_ Filter Model + Delete Transaction
            if (vm.deleteTransaction[vm.gridID] != undefined) {
              let ninFilter = { ID: { $nin: vm.deleteTransaction[vm.gridID] } };
              filterModel.push(ninFilter);
            }

            console.log(`gridID:${vm.deleteTransaction[vm.gridID]}`);
            console.log(`deleteTransaction:${vm.deleteTransaction[vm.gridID]}`);
            let path = "http://localhost:5000/infiniteRowModel";
            // debug
            // axios

            axios({
              method: "post",
              url: path,
              data: {
                tableName: vm.datasetToLoad,
                projectName: vm.projectName,
                startRow: params.startRow,
                endRow: params.endRow,
                filterModel: filterModel,
                columnModel: vm.columnModel,
                gridType: vm.gridType
              }
            })
              .then(res => {
                console.log(res.data);
                params.successCallback(res.data, -1);
              })
              .catch(error => {
                console.error(error);
              });
          }
        };
        params.api.setDatasource(dataSource);
      }
    },

    onFirstDataRendered() {
      // console.log("first");
      // setValue("#undoInput", 0);
      // disable("#undoInput", true);
      // disable("#undoBtn", true);
      // setValue("#redoInput", 0);
      // disable("#redoInput", true);
      // disable("#redoBtn", true);
    }
  },
  created() {
    this.datasetToLoad.forEach(element => {
      this.loadColumns(element);
    });
  },
  mounted() {},
  beforeMount() {}
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
