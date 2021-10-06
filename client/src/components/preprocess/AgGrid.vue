<template>
  <div>
    <v-btn @click="test">d</v-btn>
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
      :maxConcurrentDatasourceRequests="maxConcurrentDatasourceRequests"
      :infiniteInitialRowCount="infiniteInitialRowCount"
      :maxBlocksInCache="maxBlocksInCache"
      :modules="modules"
    >
    </ag-grid-vue>
  </div>
</template>

<script>
import Vue from "vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

import { AgGridVue } from "@ag-grid-community/vue";
import { InfiniteRowModelModule } from "@ag-grid-community/infinite-row-model";
import "@ag-grid-community/core/dist/styles/ag-grid.css";
import "@ag-grid-community/core/dist/styles/ag-theme-alpine.css";
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      modules: [InfiniteRowModelModule],

      gridApi: null,
      columnApi: null,
      defaultColDef: {
        flex: 1,
        resizable: true,
        minWidth: 100
      },
      components: null,
      rowBuffer: null,
      rowSelection: null,
      rowModelType: null,
      paginationPageSize: null,
      cacheOverflowSize: null,
      maxConcurrentDatasourceRequests: null,
      infiniteInitialRowCount: null,
      maxBlocksInCache: null
    };
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      datasetSize: state => state.initialData.datasetSize,
      tableName: state => state.initialData.tableName
    }),

    columnDefs() {
      let array = [{ field: "ID" }];
      this.columns.forEach(element => {
        let lowered = element.toString().toLowerCase();
        console.log(element);
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
      return array;
    }
  },
  components: {
    AgGridVue
  },
  methods: {
    test(event) {
      console.log(this.gridApi.getFilterInstance());
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
                if (item[filterColumn] > filterValue || item[filterColumn] != filterValue) {
                  continue itemLoop;
                }
                break;
              case "greaterThan":
                if (item[filterColumn] <= filterValue) {
                  continue itemLoop;
                }
                break;
              case "greaterThanOrEqual":
                if (item[filterColumn] < filterValue || item[filterColumn] != filterValue) {
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
                  new Date(item[filterColumn]) > dateFrom ||
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
                  new Date(item[filterColumn] < dateFrom) ||
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
            console.log(params);
            console.log("asking for " + params.startRow + " to " + params.endRow);
            let path = "http://localhost:5000/infiniteRowModel";

            // axios
            axios({
              method: "post",
              url: path,
              data: {
                tableName: vm.tableName,
                startRow: params.startRow.toString(),
                endRow: params.endRow.toString()
              }
            })
              .then(res => {
                let dataAfterFiltering = vm.filterData(res.data, params.filterModel);

                params.successCallback(dataAfterFiltering, vm.datasetSize);
              })

              .catch(error => {
                console.error(error);
              });
          }
        };

        params.api.setDatasource(dataSource);
      }
    }
  },
  beforeMount() {
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
    this.infiniteInitialRowCount = 1000;
    this.maxBlocksInCache = 10;
  }
};
</script>
