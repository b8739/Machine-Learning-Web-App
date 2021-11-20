<template>
  <div style="width:100%">
    <v-btn @click="getGridColumns"></v-btn>
    <!-- <v-toolbar>
      <v-toolbar-title class="mr-2 font-weight-bold subheading">Undo/Redo:</v-toolbar-title>
      <label>Available Undo's:</label>
      <input id="undoInput" readonly class="undo-redo-input" />
      <label>Available Redo's:</label>
      <input id="redoInput" readonly class="undo-redo-input" />
      <v-btn outlined color="blue-grey" class="mr-2 " small id="undoBtn" v-on:click="undo()"
        >Undo</v-btn
      >
      <v-btn outlined color="blue-grey" class="mr-2 " small id="redoBtn" v-on:click="redo()"
        >Redo</v-btn
      >
    </v-toolbar> -->
    {{ selectedColumns }}
    <v-toolbar>
      <v-toolbar-title class="mr-2 font-weight-bold subheading"> Save </v-toolbar-title>
      <v-btn color="blue-grey" class="mr-2 " outlined small @click="saveDialog = true"
        >Save Draft</v-btn
      >
      <v-chip-group class="ml-10">
        <v-chip
          v-for="(draft, draftIndex) in draftList"
          :key="draftIndex"
          label
          @click="loadDraft(draft.draftName)"
        >
          {{ draft.draftName }}
        </v-chip>
      </v-chip-group>
    </v-toolbar>
    <v-btn @click="hidePanel = !hidePanel" small>Hide Panel</v-btn>

    <div v-show="hidePanel">
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
        <v-toolbar-title class="mr-2 font-weight-bold subheading">
          Export CSV FIle:</v-toolbar-title
        >
        <v-btn class="mr-2" outlined color="blue-grey" small v-on:click="exportLoadedData()"
          >Download CSV file <label style="color:red">(Only currently loaded data)</label></v-btn
        >
        <v-btn class="mr-2" outlined color="blue-grey" small v-on:click="exportAllData()"
          >Download CSV file <label style="color:red">(All Data)</label></v-btn
        >
      </v-toolbar>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Edit Rows</v-toolbar-title>
        <v-btn class="mr-2" outlined color="blue-grey" small @click="updateRows()"
          >Update Row</v-btn
        >
        <v-btn class="mr-2" outlined color="blue-grey" small @click="deleteRows()"
          >Delete Row</v-btn
        >
      </v-toolbar>

      <v-dialog v-model="dialog_merge">
        <v-card>
          <v-card-text>현재는 데이터셋 2개만 합칠 수 있습니다.</v-card-text>

          <v-container>
            <v-select
              :items="items"
              item-text="name"
              item-value="datasetName"
              v-model="tableToMerge"
              chips
              multiple
            ></v-select>
          </v-container>
          <v-card-actions>
            <v-btn @click="createMergedGrid">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Edit Columns</v-toolbar-title>
        <v-btn class="mr-2" outlined color="blue-grey" small @click="openDisplayDialog()"
          >Drop Column (Hide)</v-btn
        >
        <v-dialog v-model="dialog_colDisplay">
          <v-card>
            <v-container>
              <v-select
                v-for="(model, modelIndex) in columnModel[currentGrid]"
                :key="modelIndex"
                :items="model"
                chips
                multiple
                v-model="selectedColumns[modelIndex]"
              ></v-select>
            </v-container>
            <v-card-actions>
              <v-btn @click="hideColumn">Confirm</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>

      <v-toolbar>
        <v-toolbar-title class="mr-2 font-weight-bold subheading">
          Edit Column Info</v-toolbar-title
        >

        <v-btn color="blue-grey" outlined @click="openChangeNameDialog" small
          >Change Column Name</v-btn
        >

        <v-dialog v-model="dialog_colName">
          <v-card>
            <v-container>
              <v-row>
                <v-col>From</v-col>
                <v-col>To</v-col>
              </v-row>
              <v-row v-for="(column, columnIndex) in loadedColumns" :key="columnIndex">
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
        <v-toolbar-title class="mr-2 font-weight-bold subheading"> Data Cleansing</v-toolbar-title>
        <v-btn
          color="blue-grey"
          disabled
          @click="dialog_nullToZero = true"
          class="mr-2 "
          outlined
          small
          >Null -> Zero</v-btn
        >
        <v-btn color="blue-grey" disabled @click="dialog_negativeToZero = true" outlined small
          >Negative -> Zero</v-btn
        >
      </v-toolbar>

      <!-- savedialog -->
      <v-dialog v-model="saveDialog" persistent max-width="300">
        <v-card class="pa-2">
          <v-card-title>Draft 저장</v-card-title>
          <v-text-field v-model="draftName" :counter="10" label="파일명"></v-text-field>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue-grey" text @click="saveDraft(draftName), (saveDialog = false)">
              저장
            </v-btn>
            <v-btn color="blue-grey" text @click="saveDialog = false">
              취소
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- <v-col> datasetToLoad {{ datasetToLoad }} </v-col>
    <v-col> currentGrid {{ currentGrid }} </v-col>
    <v-col> gridList {{ gridList }} </v-col>
    <v-col> tableToMerge {{ tableToMerge }} </v-col> -->

      <!-- <v-col> loadedColumns {{ loadedColumns }} </v-col>
    <v-col> gridColumns {{ gridColumns }} </v-col> -->
      <!-- <v-col> columnModel {{ columnModel }} </v-col> -->
      <!-- <v-col> gridList {{ gridList }}</v-col> -->
    </div>
    <v-toolbar>
      <v-chip-group class="ml-10">
        <v-chip
          v-for="(gridID, gridIndex) in gridList"
          :key="gridIndex"
          v-if="gridID != undefined"
          v-bind="dynamicVchipProp(gridIndex)"
          @click="setCurrentGrid(gridID)"
          class="ml-1"
          close
          @click:close="removeGrid(gridID)"
          label
        >
          Data {{ gridID }}
        </v-chip>
      </v-chip-group>

      <v-btn class="mr-2" small @click="readyToAddDataTable"
        ><v-icon>mdi-plus</v-icon> Add Datatable</v-btn
      >
      <v-btn class="mr-2" small @click="showAnalysis" outlined> Show Analysis</v-btn>
    </v-toolbar>
    <!-- <AgGridMultiple
      :gridID="0"
      :columnModel="{ boston: ['CRIM'], concrete: ['cement'] }"
      :datasetToLoad="['boston', 'concrete']"
      gridType="AgGridMultiple"
    /> -->

    <component
      v-for="(gridID, gridIndex) in gridList"
      :key="gridIndex"
      v-if="gridID != undefined"
      v-bind:is="gridType[gridID]"
      :gridID="gridID"
      :columnModel="columnModel[gridID]"
      :datasetToLoad="datasetToLoad[gridID]"
      :gridType="gridType[gridID]"
    ></component>

    <AgGridSummary />
    <AddGridDialog :dialog.sync="dialog_newGrid" />
    <!-- debug

    <strong> columnsForGrid:</strong>
    {{ columnsForGrid }}

    <br />
    <strong> datasetToLoad:</strong>
    {{ datasetToLoad }}

    <br />
    <strong> columnModel:</strong>
    {{ columnModel }} -->
  </div>
</template>

<script>
import Vue from "vue";
import AgGridSingle from "@/components/preprocess/AgGridSingle.vue";
import AgGridMultiple from "@/components/preprocess/AgGridMultiple.vue";
import AgGridSummary from "@/components/preprocess/AgGridSummary.vue";
import AddGridDialog from "@/components/preprocess/AddGridDialog.vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
// import store from "@/store/modules/dataTable/aggrid";
import axios from "axios";

export default {
  data() {
    return {
      draftList: [],
      draftName: "",
      saveDialog: false,
      vchipClickedProp: {
        color: "primary"
      },
      hidePanel: true,

      dialog_newGrid: false,
      dialog_colDisplay: false,
      dialog_colName: false,
      dialog_nullToZero: false,
      dialog_negativeToZero: false,
      dialog_merge: false,

      gridColumns: [],
      loadedColumns: [],
      selectedColumns: {},
      tableToMerge: []
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

      gridList: state => state.aggrid.gridList,
      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      //loadSetting
      columnsForGrid: state => state.aggrid.columnsForGrid,
      columnModel: state => state.aggrid.columnModel,
      datasetToLoad: state => state.aggrid.datasetToLoad,
      gridType: state => state.aggrid.gridType
    }),
    currentTableNameToLoad() {
      return this.datasetToLoad[parseInt(this.currentGrid) + 1];
    },
    items() {
      let array = [];
      this.gridList.forEach(element => {
        let item = { name: "Data " + element, datasetName: this.datasetToLoad[element] };
        array.push(item);
      });
      return array;
    }
  },
  components: {
    AgGridMultiple,
    AgGridSummary,
    AddGridDialog,
    AgGridSingle
  },
  created() {
    this.resetSummarizedInfo();
    this.resetAggrid();
  },
  mounted() {
    this.loadDraftList();
  },
  methods: {
    loadDraftList() {
      let path = "http://localhost:5000/loadDraftList";
      // axios
      axios({
        method: "post",
        url: path
      })
        .then(res => {
          this.draftList = [];

          res.data.forEach(element => {
            this.draftList.push(element);
          });
        })

        .catch(error => {
          console.error(error);
        });
    },
    readyToAddDataTable() {
      this.dialog_newGrid = true;
      // Vue.set(this.columnModel, parseInt(this.currentGrid) + 1, []);
    },

    ...mapMutations("initialData", ["resetSummarizedInfo"]),
    ...mapMutations("aggrid", ["addGridApi"]),
    ...mapMutations("aggrid", ["addGridColumnApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["setAnalysisDisplay"]),
    ...mapMutations("aggrid", ["resetAggrid"]),
    ...mapMutations("aggrid", ["setAvailableUndo"]),
    ...mapMutations("aggrid", ["setAvailableRedo"]),
    ...mapMutations("aggrid", ["addNewDeletion"]),
    ...mapMutations("aggrid", ["delColumnModelElement"]),
    ...mapActions("aggrid", ["removeGrid"]),
    ...mapActions("aggrid", ["saveDraft"]),
    ...mapActions("aggrid", ["loadDraft"]),

    resetLoadInfo() {
      let index = parseInt(this.currentGrid) + 1;
      this.columnsForGrid = {}; // 이건 props로 안줘서 초기화해도됨
      Vue.delete(this.datasetToLoad, index);
      Vue.set(this.columnModel, index, []);
    },
    openChangeNameDialog() {
      this.getGridColumns();
      this.dialog_colName = !this.dialog_colName;
    },
    getGridColumns() {
      let vm = this;
      this.loadedColumns = [];
      this.loadedColumns = vm.gridColumnApi[vm.currentGrid].getAllColumns().map(function(col) {
        // return { columnName: col.getColId(), columnInfo: vm.currentGrid };
        return col.getColId();
      });
    },
    test() {},
    openDisplayDialog() {
      // this.loadedColumns = [];
      // let columns = this.getGridColumns();
      // columns.forEach(element => {
      //   this.loadedColumns.push(element);
      // });
      this.dialog_colDisplay = true;
    },

    // excel
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
    getParams() {
      return { columnSeparator: this.getValue("#columnSeparator") };
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
          tableName: this.datasetToLoad[this.currentGrid],
          filterModel: filterModel,
          gridType: this.gridType[this.currentGrid],
          columnModel: this.columnModel[this.currentGrid]
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
    // undo
    undoCalculate() {
      var undoSize = this.gridApi[this.currentGrid].getCurrentUndoSize();
      // id에 접근해서 setting해줘야함
      var redoSize = this.gridApi[this.currentGrid].getCurrentRedoSize();
      // id에 접근해서 setting해줘야함
    },
    undo() {
      this.gridApi[this.currentGrid].undoCellEditing();
    },
    redo() {
      this.gridApi[this.currentGrid].redoCellEditing();
    },

    hideColumn() {
      //방법 1) columnExclude에 추가
      Object.keys(this.selectedColumns).forEach(datasetName => {
        // columnModel에서 삭제함으로써 reset되었을 때 불러오지도 않고, mount되면 columnDef에서도 삭제됨
        this.selectedColumns[datasetName].forEach(element => {
          let index = this.columnModel[this.currentGrid][datasetName].indexOf(element);
          let payload = { datasetName: datasetName, index: index };
          this.delColumnModelElement(payload);
          // mounted되면 계산되어서 columnDef에서도 삭제되지만, 그전에는 계산이 안되므로 일단 hide
          this.gridColumnApi[this.currentGrid].applyColumnState({
            state: [{ colId: element, hide: true }]
          });
        });
      });

      this.dialog_colDisplay = false;
      this.selectedColumns = {};
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    updateColumnName() {
      const columnDefs = this.gridApi[this.currentGrid].getColumnDefs();

      let changedElementIndex = [];
      this.gridColumns.forEach((element, index) => {
        if (element != null) {
          columnDefs[index].headerName = element;
        }
      });

      this.gridApi[this.currentGrid].setColumnDefs(columnDefs);
      this.gridColumns = [];
      //닫기
      this.dialog_colName = false;
    },
    deleteRows() {
      let selectedRows = this.gridApi[this.currentGrid].getSelectedRows();
      this.addNewDeletion(selectedRows);
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    showAnalysis() {
      this.setAnalysisDisplay(!this.analysisDisplay);
    },

    createMergedGrid() {
      Vue.set(this.datasetToLoad, parseInt(this.currentGrid) + 1, this.tableToMerge);
      this.columnModel[parseInt(this.currentGrid) + 1] = [];
      this.addGridList();

      this.addCurrentGrid();
      this.setAnalysisDisplay(false);
    },

    dynamicVchipProp(gridIndex) {
      if (gridIndex == this.currentGrid) {
        return this.vchipClickedProp;
      }
    }
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
