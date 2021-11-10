<template>
  <div>
    <ag-grid-vue
      v-show="analysisDisplay == true"
      style="width: 1400px; height:800px"
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
    summarizedInfo: {
      handler: function() {
        // if (this.summarizedInfo[this.currentGrid] != undefined) {
        // }
        this.gridApi.setRowData(this.summarizedInfo[this.currentGrid]);
      },
      deep: true
    }
  },
  // setFilterModel
  data() {
    return {
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
        { field: "mean" },
        { field: "mode" },
        { field: "median" },
        { field: "standard" },
        { field: "Q1" },
        { field: "Q2" },
        { field: "Q3" },
        { field: "Q4" },
        { field: "numOfNA" }
      ]
    };
  },
  computed: {
    ...mapState({
      summarizedInfo: state => state.initialData.summarizedInfo,
      // gridapi
      gridApi: state => state.aggrid.summaryGridApi,
      gridColumnApi: state => state.aggrid.summaryGridColumnApi,
      currentGrid: state => state.aggrid.currentGrid,
      gridList: state => state.aggrid.gridList,
      analysisDisplay: state => state.aggrid.analysisDisplay
    }),
    rowData() {
      return this.summarizedInfo[this.currentGrid];
    }
  },
  components: {
    AgGridVue
  },
  methods: {
    ...mapMutations("aggrid", ["setSummaryGridApi"]),
    ...mapMutations("aggrid", ["setSummaryColumnGridApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["addGridList"]),
    ...mapMutations("aggrid", ["setAnalysisDisplay"]),
    onGridReady(params) {
      this.setSummaryGridApi(params.api);
      this.setSummaryColumnGridApi(params.columnApi);
      // this.gridApi = params.api;
      // this.gridColumnApi = params.columnApi;
    }
  },
  created() {},
  mounted() {},
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
