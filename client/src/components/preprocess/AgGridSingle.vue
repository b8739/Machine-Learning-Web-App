<template>
  <div>
    <ag-grid-vue
      v-show="currentGrid == gridID && viewMode == 'table'"
      style="width: 100%; height:700px"
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
      @column-moved="onColumnMoved"
      @filter-changed="onFilterChanged"
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
export default {
  mixins: [AgGridMix],

  props: ["gridID", "datasetToLoad", "columnModel", "gridType"],
  watch: {},
  data() {
    return {
      modules: [InfiniteRowModelModule, CsvExportModule]
    };
  },
  computed: {
    // finalColumns() {

    //   return this.columnModel[this.datasetToLoad];
    // },

    columnDefs() {
      return this.columnModel[this.datasetToLoad].map(function(col) {
        let lowered = col.toString().toLowerCase();
        if (lowered == "id") {
          return { field: col, filter: "agNumberColumnFilter", maxWidth: 70, editable: false };
        } else if (
          lowered == "ts" ||
          lowered == "timeseries" ||
          lowered == "date" ||
          lowered == "datetime"
        ) {
          return { field: col, filter: "agDateColumnFilter" };
        } else {
          return { field: col, filter: "agNumberColumnFilter" };
        }
      });
    }
  },
  methods: {
    onBtOrderColsMedalsFirst() {
      this.gridColumnApi[this.gridID].applyColumnState({
        state: [{ colId: "ZN" }, { colId: "CRIM" }],
        applyOrder: true
      });
    },
    resetCache() {
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    onFirstDataRendered() {
      // setValue("#undoInput", 0);
      // disable("#undoInput", true);
      // disable("#undoBtn", true);
      // setValue("#redoInput", 0);
      // disable("#redoInput", true);
      // disable("#redoBtn", true);
    },

    onGridReady(params) {
      // console.log("on single grid readty");
      let payload = { api: params.api, gridID: this.gridID };
      this.addGridApi(payload);
      payload = { api: params.columnApi, gridID: this.gridID };
      this.addGridColumnApi(payload);
      this.loadColumnState(this.gridID); // Order
      this.loadFilterState(this.gridID); // Filter
      this.updateColumnHeader(this.gridID);

      let vm = this;

      updateData(vm);

      function updateData(vm) {
        let dataSource = {
          rowCount: null,
          getRows: function(params) {
            console.log("asking for " + params.startRow + " to " + params.endRow);
            // 1) Get Filter Model
            let filterModel;
            if (vm.filterModel[vm.gridID] != undefined) {
              filterModel = vm.filterModel[vm.gridID];
            } else {
              filterModel = {};
            }

            // 2) Delete Model
            let deleteModel;
            if (vm.deleteModel[vm.gridID] != undefined) {
              deleteModel = vm.deleteModel[vm.gridID];
            } else {
              deleteModel = [];
            }
            // 3) Rename Model
            let renameModel;
            if (vm.renameModel[vm.gridID] != undefined) {
              renameModel = vm.renameModel[vm.gridID];
            } else {
              renameModel = [];
            }
            // 3) Type Model
            let typeModel;
            if (vm.typeModel[vm.gridID] != undefined) {
              typeModel = vm.typeModel[vm.gridID];
            } else {
              typeModel = [];
            }
            // 4) fill Na Model

            let fillNaModel;
            if (vm.fillNaModel[vm.gridID] != undefined) {
              fillNaModel = vm.fillNaModel[vm.gridID];
            } else {
              fillNaModel = [];
            }
            // 5) delete Na Model

            let deleteNaModel;
            if (vm.deleteNaModel[vm.gridID] != undefined) {
              deleteNaModel = vm.deleteNaModel[vm.gridID];
            } else {
              deleteNaModel = [];
            }

            // axios
            let path = "http://localhost:5000/infiniteRowModel";

            axios({
              method: "post",
              url: path,
              data: {
                tableName: vm.datasetToLoad,
                projectName: vm.projectName,
                startRow: params.startRow,
                endRow: params.endRow,
                deleteModel: deleteModel,
                filterModel: filterModel,
                columnModel: vm.columnModel[vm.datasetToLoad],
                renameModel: renameModel,
                typeModel: typeModel,
                fillNaModel: fillNaModel,
                deleteNaModel: deleteNaModel,
                gridType: vm.gridType
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
    }
  },
  created() {
    this.loadColumns(this.datasetToLoad);
  },
  mounted() {
    // console.log("single mounted");
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
