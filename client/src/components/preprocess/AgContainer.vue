<template>
  <div style="width:100%">
    <v-container>
      <v-row>
        <v-col cols="2"> <AgSideMenu @openDialog="dialogAction"/></v-col>

        <v-col cols="10">
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

          <div>
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

            <!-- Save Dialog  -->
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
          </div>
          <!-- Grid 추가, 삭제 및 관리 -->
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
            <v-chip-group v-model="viewStatus" active-class="primary--text">
              <v-chip class="mr-2" label small @click="setViewMode('table')"> Data Table</v-chip>
              <v-chip class="mr-2" label small @click="setViewMode('statistics')">
                Summary Statistics</v-chip
              >

              <v-chip class="mr-2" label small @click="setViewMode('distribution')()">
                Feature Distribution</v-chip
              >
            </v-chip-group>
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
          <!-- Delete Column -->
          <AgGridDialog
            :dialog.sync="dialog_colDisplay"
            :selectedColumns="selectedColumns"
            :dialogName="'deleteColumn'"
          >
            <template v-slot:insideContainer>
              <v-select
                v-for="(model, modelIndex) in columnModel[currentGrid]"
                :key="modelIndex"
                :items="model"
                chips
                multiple
                v-model="selectedColumns[modelIndex]"
              ></v-select>
            </template>

            <template v-slot:deleteColumnAction="slotProps">
              <v-btn @click="slotProps.hideColumn">Confirm</v-btn>
            </template>
          </AgGridDialog>

          <!-- Change Name -->
          <AgGridDialog
            :dialog.sync="dialog_colName"
            :gridColumns="gridColumns"
            :dialogName="'changeName'"
          >
            <template v-slot:insideContainer>
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
            </template>
            <template v-slot:changeNameAction="slotProps">
              <v-btn @click="slotProps.updateColumnName">Confirm</v-btn>
            </template>
          </AgGridDialog>

          <!-- Change Data Type -->
          <AgGridDialog
            :dialog.sync="dialog_colType"
            :dialogName="'changeType'"
            :dataTypes="dataTypes"
          >
            <template v-if="columnModel[currentGrid]" v-slot:insideContainer_type="slotProps">
              {{ slotProps.dataTypeModel }}
              <v-row
                v-for="(colName, colIndex) in columnModel[currentGrid][datasetToLoad[currentGrid]]"
                :key="colIndex"
              >
                <v-col><v-subheader v-text="colName"></v-subheader></v-col>
                <v-col>
                  <v-select
                    v-if="slotProps.dataTypes"
                    :items="dataTypeItems"
                    :placeholder="slotProps.dataTypes[colName]"
                    v-model="slotProps.dataTypeModel[colIndex]"
                  ></v-select
                ></v-col>
                <!-- :label에 mongodb에서 불러온 datatype을 넣어줘야 함 -->
              </v-row>
            </template>
            <template v-slot:changeTypeAction="slotProps">
              <v-btn @click="slotProps.updateDataType()">Confirm</v-btn>
            </template>
          </AgGridDialog>
          <!-- Fill NA -->
          <AgGridDialog :dialog.sync="dialog_fillNa" :dialogName="'fillNa'">
            <template v-if="columnModel[currentGrid]" v-slot:insideContainer_na="slotProps">
              fillNaModel: {{ slotProps.fillNaModel }}
              <v-card-subtitle>Leave the select box if not applying 'fillNa'</v-card-subtitle>
              <v-row
                v-for="(colName, colIndex) in columnModel[currentGrid][datasetToLoad[currentGrid]]"
                :key="colIndex"
              >
                <v-col><v-subheader v-text="colName"></v-subheader></v-col>
                <v-col>
                  <v-select
                    :items="[0, 1, 'min', 'max', 'mean', 'std']"
                    v-model="slotProps.fillNaModel[colName]"
                  ></v-select
                ></v-col>
              </v-row>
            </template>
            <template v-slot:fillNaAction="slotProps">
              <v-btn @click="slotProps.applyFillNa()">Confirm</v-btn>
            </template>
          </AgGridDialog>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Vue from "vue";
import AgGridSingle from "@/components/preprocess/AgGridSingle.vue";
import AgGridMultiple from "@/components/preprocess/AgGridMultiple.vue";
import AgGridSummary from "@/components/preprocess/AgGridSummary.vue";
import AddGridDialog from "@/components/preprocess/AddGridDialog.vue";
import AgGridDialog from "@/components/preprocess/AgGridDialog.vue";
import AgSideMenu from "@/components/preprocess/AgSideMenu.vue";
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
// import store from "@/store/modules/dataTable/aggrid";
import axios from "axios";

export default {
  data() {
    return {
      viewStatus: 0,
      draftList: [],

      draftName: "",
      saveDialog: false,
      vchipClickedProp: {
        color: "primary"
      },
      hidePanel: true,
      dialog_colType: false,
      dialog_newGrid: false,
      dialog_colDisplay: false,
      dialog_colName: false,
      dialog_fillNa: false,

      gridColumns: [],
      loadedColumns: [],
      selectedColumns: {},
      tableToMerge: [],
      dataTypes: null,
      sampleDataTypes: ["float", "int", "double"],
      dataTypeItems: ["double", "string", "bool", "date", "int", "long", "decimal"]
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
    AgGridSingle,
    AgGridDialog,
    AgSideMenu
  },
  created() {
    this.resetSummarizedInfo();
    this.resetAggrid();
  },
  mounted() {},
  methods: {
    dialogAction(dialogName) {
      if (dialogName == "changeColName") {
        this.getGridColumns();
        this.dialog_colName = !this.dialog_colName;
      } else if (dialogName == "changeColType") {
        this.getDataTypes();
      } else if (dialogName == "dropColumn") {
        this.dialog_colDisplay = true;
      } else if (dialogName == "fillNA") {
        this.dialog_fillNa = true;
      } else if (dialogName == "saveDraft") {
        this.saveDialog = true;
      }
    },

    getDataTypes() {
      let path = "http://localhost:5000/getDataTypes";
      axios({
        method: "post",
        url: path,
        data: {
          projectName: this.projectName,
          tableName: this.datasetToLoad[this.currentGrid],
          columnModel: this.columnModel[this.currentGrid][this.datasetToLoad[this.currentGrid]]
        }
      })
        .then(res => {
          this.dataTypes = res.data;
          this.dialog_colType = true;
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
    ...mapMutations("aggrid", ["setViewMode"]),
    ...mapMutations("aggrid", ["resetAggrid"]),
    ...mapMutations("aggrid", ["setAvailableUndo"]),
    ...mapMutations("aggrid", ["setAvailableRedo"]),
    ...mapActions("aggrid", ["removeGrid"]),
    ...mapActions("aggrid", ["saveDraft"]),

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
    test(value) {
      alert(value);
    },
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

    showAnalysis() {
      this.setViewMode("statistics");
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
