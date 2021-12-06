<template>
  <div v-show="viewMode == 'statistics'">
    <!-- <v-btn @click="load">수동</v-btn> -->
    <v-select
      v-model="datasetToLoad"
      :items="tableList"
      label="Select Dataset"
      @input="loadStatistics"
      clearable
      clear-icon
    ></v-select>
    <!-- @input="loadColumns" -->
    <ag-grid-vue
      style="width: 100%; height:600px"
      class="ag-theme-alpine"
      :rowData="rowData"
      @grid-ready="onGridReady"
      :defaultColDef="defaultColDef"
      :columnDefs="columnDefs"
      :components="components"
      :modules="modules"
    >
    </ag-grid-vue>
  </div>
</template>
<script>
import Vue from "vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

import { AgGridVue } from "@ag-grid-community/vue";
import { CsvExportModule } from "@ag-grid-community/csv-export";
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model";
import "@ag-grid-community/core/dist/styles/ag-grid.css";
import "@ag-grid-community/core/dist/styles/ag-theme-alpine.css";
import axios from "axios";

export default {
  props: ["tableNameToLoad"],
  watch: {
    currentDataset: {
      handler: function() {
        if (this.summarizedInfo[this.currentDataset] == undefined) {
          this.loadSummarizedData(this.currentDataset);
        } else {
          this.gridApi.setRowData(this.summarizedInfo[this.currentDataset]);
        }
      },
      deep: true
    }
  },
  // setFilterModel
  data() {
    return {
      currentDataset: null,
      datasetToLoad: [],
      columnsForGrid: [],

      gridColumns: [],

      modules: [CsvExportModule, ClientSideRowModelModule],

      components: null,
      rowBuffer: null,
      rowSelection: null,
      paginationPageSize: null,

      defaultColDef: {
        flex: 1,
        minWidth: 140,
        editable: true,
        resizable: true,
        // undo
        undoRedoCellEditingLimit: null
      },
      getRowStyle: null,
      columnDefs: [
        { field: "name" },
        { field: "dtype" },
        { field: "mean" },
        { field: "mode" },
        { field: "median" },
        { field: "std" },
        { field: "Q1" },
        { field: "Q2" },
        { field: "Q3" },
        { field: "Q4" },
        { field: "numOfNA" },
        { field: "size" },
        { field: "nunique" }
      ]
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,

      summarizedInfo: state => state.initialData.summarizedInfo,
      // gridapi
      gridApi: state => state.aggrid.summaryGridApi,
      gridColumnApi: state => state.aggrid.summaryGridColumnApi,
      currentGrid: state => state.aggrid.currentGrid,
      gridList: state => state.aggrid.gridList,
      viewMode: state => state.aggrid.viewMode
    }),
    rowData() {
      return this.summarizedInfo[this.currentGrid];
    }
  },
  components: {
    AgGridVue
  },
  methods: {
    load() {
      this.gridApi.setRowData(this.summarizedInfo["boston"]);
    },
    ...mapActions("initialData", ["loadSummarizedData"]),

    ...mapMutations("aggrid", ["setSummaryGridApi"]),
    ...mapMutations("aggrid", ["setSummaryColumnGridApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["addGridList"]),
    ...mapMutations("aggrid", ["setViewMode"]),

    onGridReady(params) {
      this.setSummaryGridApi(params.api);
      this.setSummaryColumnGridApi(params.columnApi);
    },
    loadStatistics(value) {
      console.log(`loadstatistics: ${value}`);
      this.currentDataset = value;
    }
  },
  created() {},
  mounted() {
    console.log("loadSummarize");
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

    this.paginationPageSize = 100;
  }
};
</script>
