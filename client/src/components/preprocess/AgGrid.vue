<template>
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
        array.push({ field: element });
      });

      return array;
    }
  },
  components: {
    AgGridVue
  },
  methods: {
    // onGridReady(params) {
    //       this.gridApi = params.api;
    //       this.gridColumnApi = params.columnApi;

    //       const updateData = (data) => {
    //         var dataSource = {
    //           rowCount: null,
    //           getRows: function (params) {
    //             console.log(
    //               'asking for ' + params.startRow + ' to ' + params.endRow
    //             );
    //             setTimeout(function () {
    //               var rowsThisPage = data.slice(params.startRow, params.endRow);
    //               var lastRow = -1;
    //               if (data.length <= params.endRow) {
    //                 lastRow = data.length;
    //               }
    //               params.successCallback(rowsThisPage, lastRow);
    //             }, 500);
    //           },
    //         };
    //         gridApi.setDatasource(dataSource);
    //       };

    //       fetch('https://www.ag-grid.com/example-assets/olympic-winners.json')
    //         .then((resp) => resp.json())
    //         .then((data) => updateData(data));
    //     },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
      let vm = this;
      updateData(vm);

      // function
      function updateData(vm) {
        var dataSource = {
          rowCount: null,
          getRows: function(params) {
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
                var lastRow = -1;
                if (vm.datasetSize <= params.endRow) {
                  lastRow = vm.datasetSize;
                }
                params.successCallback(res.data, lastRow);
              })
              .catch(error => {
                console.error(error);
              });
          }
        };
        console.log(dataSource);
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
