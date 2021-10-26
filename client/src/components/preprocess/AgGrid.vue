<template>
  <div>
    <!-- Toolbars -->
    <v-toolbar> {{ updateTransaction }}</v-toolbar>
    <v-toolbar>
      <v-toolbar-title class="mr-2">Undo/Redo:</v-toolbar-title>
      <label>Available Undo's:</label>
      <input id="undoInput" readonly class="undo-redo-input" />
      <label>Available Redo's:</label>
      <input id="redoInput" readonly class="undo-redo-input" />

      <v-btn small id="undoBtn" v-on:click="undo()">Undo</v-btn>
      <v-btn small id="redoBtn" v-on:click="redo()">Redo</v-btn>
      <v-btn small @click="test">test</v-btn>
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
      <v-btn small>Insert</v-btn>
      <v-btn small @click="updateRows()">Update</v-btn>
      <v-btn small @click="deleteRows()">Delete</v-btn>

      <!-- AG Grid -->
    </v-toolbar>
    <v-dialog v-model="dialog">
      <v-card>
        <input id="csvResult" />
      </v-card>
    </v-dialog>
    <ag-grid-vue
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
      dialog: false,
      modules: [InfiniteRowModelModule, CsvExportModule],

      gridApi: null,
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
        minWidth: 100,
        editable: true,
        resizable: true,
        // undo
        undoRedoCellEditingLimit: null
      },
      getRowStyle: null,
      updateTransaction: []
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
      let selectedRows = this.gridApi.getSelectedRows();
      let selectedIDs = [];
      selectedRows.forEach(element => {
        selectedIDs.push(element["ID"]);
      });
      let path = "http://localhost:5000/deleteRows";

      // axios
      axios({
        method: "post",
        url: path,
        data: {
          projectName: this.projectName,
          tableName: this.tableName,
          selectedIDs: selectedIDs
        }
      })
        .then(res => {
          // let dataAfterFiltering = vm.filterData(res.data, params.filterModel);
          // console.log(res.data);
          this.gridApi.refreshInfiniteCache();
          console.log(res.data);
        })

        .catch(error => {
          console.error(error);
        });
    },
    filtercheck() {
      let dd = this.gridApi.getFilterModel();
      console.log(dd);
    },

    getDisplayedRowCount() {
      var count = this.gridApi.getDisplayedRowCount();
      console.log("getDisplayedRowCount() => " + count);
    },
    printAllDisplayedRows() {
      var count = this.gridApi.getDisplayedRowCount();
      console.log("## printAllDisplayedRows");
      for (var i = 0; i < count; i++) {
        var rowNode = this.gridApi.getDisplayedRowAtIndex(i);
        console.log("row " + i + " is " + rowNode.data);
      }
    },
    getRowData() {
      var rowData = [];
      this.gridApi.forEachNode(function(node) {
        rowData.push(node.data);
      });
      console.log("Row Data:");
      console.log(rowData);
    },
    exportAllData() {
      let filterModel = this.gridApi.getFilterModel();
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

      this.gridApi.exportDataAsCsv(params);
    },
    onBtnUpdate() {
      this.dialog = true;

      document.querySelector("#csvResult").value = this.gridApi.getDataAsCsv(this.getParams());
    },
    test() {
      let getSelectedNodes = this.gridApi.getSelectedNodes();
      let getSelectedRows = this.gridApi.getSelectedRows();
      console.log(getSelectedNodes);
      console.log(getSelectedRows);
    },

    filterData(data, filterModel) {
      // Filter 존재 여부 검사
      // [If Filter exists] fitler 안하고 그대로 반환
      let filterList = Object.keys(filterModel);

      let isFilterPresent = filterModel && Object.keys(filterModel).length > 0;
      if (!isFilterPresent) {
        return data;
      }

      // [If Not]
      let resultOfFilter = [];
      // loop
      itemLoop: for (let i = 0; i < data.length; i++) {
        let item = data[i];
        filterLoop: for (let j = 0; j < filterList.length; j++) {
          let filterColumn = filterList[j];
          let filterType = filterModel[filterColumn].filterType;
          let filterCalculation = filterModel[filterColumn].type;

          //switch
          if (filterType == "text") {
            let filterValue = filterModel[filterColumn].filter;
            switch (filterCalculation) {
              case "contains":
                if (item[filterColumn].includes(filterValue.toString()) == false) {
                  continue itemLoop;
                }
                break;
              case "notContains":
                if (item[filterColumn].includes(filterValue.toString())) {
                  continue itemLoop;
                }
                break;
              case "startsWith":
                if (item[filterColumn].toString()[0] != filterValue) {
                  continue itemLoop;
                }
                break;
              case "endsWith":
                if (
                  item[filterColumn].toString()[item[filterColumn].toString().length - 1] ==
                  filterValue
                ) {
                  continue itemLoop;
                }
            }
          } else if (filterType == "number") {
            let filterValue = filterModel[filterColumn].filter;
            switch (filterCalculation) {
              case "equals":
                if (item[filterColumn] != filterValue) {
                  continue itemLoop;
                }
                break;
              case "notEqual":
                if (item[filterColumn] == filterValue) {
                  continue itemLoop;
                }
                break;

              case "lessThan":
                if (item[filterColumn] >= filterValue) {
                  continue itemLoop;
                }
                break;
              case "lessThanOrEqual":
                if (item[filterColumn] > filterValue && item[filterColumn] != filterValue) {
                  continue itemLoop;
                }
                break;
              case "greaterThan":
                if (item[filterColumn] <= filterValue) {
                  continue itemLoop;
                }
                break;
              case "greaterThanOrEqual":
                if (item[filterColumn] < filterValue && item[filterColumn] != filterValue) {
                  continue itemLoop;
                }
                break;
              case "inRange":
                if (
                  filterValue <= item[filterColumn] &&
                  item[filterColumn] < filterModel[filterColumn]["filterTo"] == false
                ) {
                  continue itemLoop;
                }
                break;
              case "dateFrom":
                if (
                  filterValue <= item[filterColumn] &&
                  item[filterColumn] < filterModel[filterColumn]["filterTo"] == false
                ) {
                  continue itemLoop;
                }
                break;

                break;
              default:
                break;
            }
          } else if (filterType == "date") {
            let dateFrom = filterModel[filterColumn].dateFrom;

            switch (filterCalculation) {
              case "equals":
                if (item[filterColumn] != dateFrom) {
                  continue itemLoop;
                }
                break;
              case "notEqual":
                if (item[filterColumn] == dateFrom) {
                  continue itemLoop;
                }
                break;

              case "lessThan":
                if (new Date(item[filterColumn]) > new Date(dateFrom)) {
                  continue itemLoop;
                }
                break;
              case "lessThanOrEqual":
                if (
                  new Date(item[filterColumn]) > dateFrom &&
                  new Date(item[filterColumn] != dateFrom)
                ) {
                  continue itemLoop;
                }
                break;
              case "greaterThan":
                if (new Date(item[filterColumn]) < new Date(dateFrom)) {
                  continue itemLoop;
                }
                break;
              case "greaterThanOrEqual":
                if (
                  new Date(item[filterColumn] < dateFrom) &&
                  new Date(item[filterColumn] != dateFrom)
                ) {
                  continue itemLoop;
                }
                break;
              case "inRange":
                let dateTo = filterModel[filterColumn].dateTo;

                if (
                  new Date(dateFrom >= item[filterColumn]) &&
                  new Date(item[filterColumn] > dateTo) == false
                ) {
                  continue itemLoop;
                }
                break;

              default:
                break;
            }
          }
        }
        resultOfFilter.push(item);
      }
      return resultOfFilter;
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
      let vm = this;
      updateData(vm);

      // function
      function updateData(vm) {
        let dataSource = {
          rowCount: null,

          getRows: function(params) {
            // console.log("asking for " + params.startRow + " to " + params.endRow);
            let filterModel = vm.gridApi.getFilterModel();
            // console.log(filterModel);
            // console.log(vm.parseFilterModel(filterModel));
            filterModel = vm.parseFilterModel(filterModel);

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
                // let dataAfterFiltering = vm.filterData(res.data, params.filterModel);
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
        return "none";
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
              let newCondition = this.filterSwitch(element, filterModel[element]["condition" + i]);
              condition[operator].push(newCondition);
            }
          }
          // NO operator
          else {
            // no operator
            condition = this.filterSwitch(element, filterModel[element]);
          }
          conditionList.push(condition);
        });
        return conditionList;
      }
    },
    filterSwitch(elementName, filterModel) {
      console.log(filterModel);
      let filter = filterModel["filter"];
      let condition = {};
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
      this.gridApi.undoCellEditing();
    },
    redo() {
      this.gridApi.redoCellEditing();
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
