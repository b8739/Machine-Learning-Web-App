import { AgGridVue } from "@ag-grid-community/vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import axios from "axios";

export default {
  components: {
    AgGridVue
  },
  data() {
    return {
      columnsForGrid: [],

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
      viewMode: state => state.aggrid.viewMode,
      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      deleteModel: state => state.aggrid.deleteModel,
      // model
      renameModel: state => state.aggrid.renameModel,
      columnState: state => state.aggrid.columnState,
      typeModel: state => state.aggrid.typeModel,
      fillNaModel: state => state.aggrid.fillNaModel,
      deleteNaModel: state => state.aggrid.deleteNaModel,
      filterModel: state => state.aggrid.filterModel,
      clientFilterModel: state => state.aggrid.clientFilterModel
    })
  },
  methods: {
    ...mapMutations("aggrid", ["addGridApi"]),
    ...mapMutations("aggrid", ["addGridColumnApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["setViewMode"]),
    ...mapMutations("aggrid", ["setColumnState"]),
    ...mapMutations("aggrid", ["setFilterModel"]),
    ...mapMutations("aggrid", ["setClientFilterModel"]),
    loadColumnState(gridID) {
      if (this.columnState[gridID]) {
        var columnState = JSON.parse(this.columnState[gridID]);
        if (columnState) {
          // console.log(typeof columnState);

          this.gridColumnApi[gridID].applyColumnState({
            state: columnState,
            applyOrder: true
          });
        }
      }
    },
    loadFilterState(gridID) {
      this.gridApi[gridID].setFilterModel(this.clientFilterModel[gridID]);
    },
    updateColumnHeader(gridID) {
      let columnDefs = this.gridApi[gridID].getColumnDefs();

      let renameModel;
      if (this.renameModel[gridID] != undefined) {
        renameModel = this.renameModel[gridID];
      } else {
        renameModel = [];
      }
      // console.log(renameModel);
      renameModel.forEach((element1, index) => {
        columnDefs.forEach(element2 => {
          if (element1["from"] == element2["colId"]) {
            element2.headerName = element1["to"];
          }
        });
      });
      this.gridApi[gridID].setColumnDefs(columnDefs);
      // console.log(columnDefs);
    },
    onColumnMoved(params) {
      var columnState = JSON.stringify(params.columnApi.getColumnState());
      this.setColumnState(columnState);
      // console.log(params.columnApi.getColumnState());
    },
    onFilterChanged(params) {
      let filterModel = params.api.getFilterModel();
      this.setClientFilterModel(filterModel);

      let finalFilterModel = this.parseFilterModel(filterModel);
      this.setFilterModel(finalFilterModel);
    },
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

    onBtnUpdate() {
      this.dialog = true;

      document.querySelector("#csvResult").value = this.gridApi[this.currentGrid].getDataAsCsv(
        this.getParams()
      );
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
          this.deleteModel(index);
        }
      });

      // 배열에 입력

      this.addNewUpdate(update);
    }
  },
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
    this.rowModelType = "infinite";
    this.paginationPageSize = 100;
    this.cacheOverflowSize = 2;
    this.maxConcurrentDatasourceRequests = 1;
    this.infiniteInitialRowCount = 1;

    this.undoRedoCellEditingLimit = 5;
  }
};
