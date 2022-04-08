<template>
  <div style="width:100%;">
    <v-container fluid>
      <v-row>
        <v-col cols=""> <AgSideMenu @openDialog="dialogAction"/></v-col>
        <v-col cols="10">
          <!-- <v-btn @click="selectAll"></v-btn> -->
          <portal-target name="edaPortal"> </portal-target>

          <!-- <modal
            name="my-first-modal"
            :draggable="true"
            :clickToClose="false"
            :overlayTransition="'background-color:red'"
            class="modal-override"
          >
            This is my first modal
          </modal> -->
          <!-- <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>
                개발 현황
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-simple-table>
                  <template>
                    <thead>
                      <tr>
                        <th>Feature</th>
                        <th>Single Datatable</th>
                        <th>Merged Datatable</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(info, index) in devProgess" :key="index">
                        <td>{{ info.function }}</td>
                        <td>
                          <v-icon :color="iconColor(info.singleTable)">{{
                            info.singleTable
                          }}</v-icon>
                        </td>
                        <td>
                          <v-icon :color="iconColor(info.mergedTable)">{{
                            info.mergedTable
                          }}</v-icon>
                        </td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels> -->

          <!-- {{ loadedColumns }}
          <v-btn @click="test"> test</v-btn> -->
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
          <v-toolbar :width="aggridWidth">
            <v-chip-group class="ml-10">
              <v-chip
                v-for="(grid, gridIndex) in gridList"
                :key="grid.id"
                v-if="grid != undefined"
                v-bind="dynamicVchipProp(grid.id)"
                @click="setCurrentGrid(grid.id)"
                class="ml-1"
                close
                @click:close="removeGrid(grid.id)"
                label
              >
                {{ grid.name }}
              </v-chip>
            </v-chip-group>
            <!-- <v-btn @click="shortcut()">shortcut create table</v-btn> -->

            <v-btn class="mr-2" small @click="readyToAddDataTable"
              ><v-icon>mdi-plus</v-icon> Add Datatable</v-btn
            >

            <v-chip-group v-model="viewStatus" active-class="primary--text">
              <v-chip class="mr-2" label small @click="setViewMode('table')"> Data Table</v-chip>
              <v-chip class="mr-2" label small @click="setViewMode('statistics')">
                Summary Statistics</v-chip
              >
              <!-- 
              <v-chip class="mr-2" label small @click="setViewMode('distribution')">
                Feature Distribution</v-chip
              > -->
            </v-chip-group>
          </v-toolbar>
          <!-- <AgGridMultiple
      :gridID="0"
      :columnModel="{ boston: ['CRIM'], concrete: ['cement'] }"
      :datasetToLoad="['boston', 'concrete']"
      gridType="AgGridMultiple"
    /> -->
          <v-card v-show="viewMode == 'table'" :width="aggridWidth" height="80vh">
            <component
              v-for="(grid, gridIndex) in gridList"
              :key="grid.id"
              v-if="grid != undefined"
              v-bind:is="gridType[grid.id]"
              :gridID="grid.id"
              :columnModel="columnModel[grid.id]"
              :datasetToLoad="datasetToLoad[grid.id]"
              :gridType="gridType[grid.id]"
            ></component>
          </v-card>

          <AgGridSummary />
          <AddGridDialog :dialog.sync="dialog_newGrid" />
          <!-- Delete Column -->
          <AgGridDialog
            v-if="columnModel[currentGrid]"
            :dialog.sync="dialog_colDisplay"
            :dialogName="'deleteColumn'"
          >
            <template v-slot:deleteColumn="slotProps">
              <v-card-title>Delete Column</v-card-title>
              <v-card-subtitle
                >Check columns that need to be deleted, and click CONFIRM</v-card-subtitle
              >

              <v-subheader>Current Dataset: {{ currentDataset }}</v-subheader>
              <v-select
                :items="columnModel[currentGrid][currentDataset]"
                chips
                multiple
                v-model="slotProps.select"
                @input="slotProps.saveSelectedColumns"
              ></v-select>
            </template>

            <template v-slot:deleteColumn_action="slotProps">
              <v-btn @click="slotProps.dropColumn">Confirm</v-btn>
            </template>
          </AgGridDialog>

          <!-- Change Name -->
          <AgGridDialog
            v-if="columnModel[currentGrid]"
            :dialog.sync="dialog_colName"
            :gridColumns="gridColumns"
            :dialogName="'changeName'"
          >
            <template v-slot:default>
              <v-row>
                <v-card-title>Change Name</v-card-title>
                <v-card-subtitle></v-card-subtitle>
              </v-row>
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
            <template v-slot:changeName_action="slotProps">
              <v-btn @click="slotProps.updateColumnName">Confirm</v-btn>
            </template>
          </AgGridDialog>

          <!-- Change Data Type -->
          <AgGridDialog
            v-if="columnModel[currentGrid]"
            :dialog.sync="dialog_colType"
            :dialogName="'changeType'"
            :dataTypes="dataTypes"
          >
            <template v-slot:changeType="slotProps">
              <v-row>
                <v-card-title>Change Type</v-card-title>
                <v-card-subtitle></v-card-subtitle>
              </v-row>
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
            <template v-slot:changeType_action="slotProps">
              <v-btn @click="slotProps.updateDataType()">Confirm</v-btn>
            </template>
          </AgGridDialog>
          <!-- Fill NA -->
          <AgGridDialog
            v-if="columnModel[currentGrid]"
            :dialog.sync="dialog_fillNa"
            :dialogName="'fillNa'"
          >
            <template v-slot:fillNA="slotProps">
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
            <template v-slot:fillNa_action="slotProps">
              <v-btn @click="slotProps.applyFillNa()">Confirm</v-btn>
            </template>
          </AgGridDialog>
          <!-- Delete NA -->
          <AgGridDialog
            v-if="columnModel[currentGrid]"
            :dialog.sync="dialog_deleteNA"
            :dialogName="'deleteNA'"
          >
            <template v-slot:deleteNA="slotProps">
              {{ slotProps.deleteNaModel }}
              <v-card-subtitle>Leave the checkbox if not applying 'Delete NA'</v-card-subtitle>
              <v-row
                v-for="(colName, colIndex) in columnModel[currentGrid][datasetToLoad[currentGrid]]"
                :key="colIndex"
              >
                <v-col><v-subheader v-text="colName"></v-subheader></v-col>
                <!-- <v-col>Num of NA.:{{}}</v-col> -->
                <v-col>
                  <v-checkbox v-model="slotProps.deleteNaModel[colName]" solo dense></v-checkbox
                ></v-col>
              </v-row>
            </template>
            <template v-slot:deleteNa_action="slotProps">
              <v-btn @click="slotProps.applyDeleteNa()">Confirm</v-btn>
            </template>
          </AgGridDialog>
          <!--  Merge Grid -->
          <AgGridDialog :dialog.sync="dialog_merge" :dialogName="'mergeTables'">
            <template v-slot:default>
              현재는 ID를 기준으로 Table이 병합됩니다. (다른 컬럼 (ex.Date) 기준으로 병합할 수
              있도록 업데이트 예정)
              <!-- {{ tablesToMerge }} -->
              <v-select
                :items="gridList"
                item-text="name"
                item-value="id"
                chips
                multiple
                v-model="tablesToMerge"
                :rules="mergeTableRule"
              ></v-select>
            </template>

            <template v-slot:mergeTable_action="slotProps">
              <v-btn @click="mergeTables(tablesToMerge), (tablesToMerge = [])">Confirm</v-btn>
            </template>
          </AgGridDialog>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Vue from "vue";
import PlotlyDist from "@/components/graph/PlotlyDist.vue";
import AgGridSingle from "@/components/preprocess/AgGridSingle.vue";
import AgGridMultiple from "@/components/preprocess/AgGridMultiple.vue";
import AgGridSummary from "@/components/preprocess/AgGridSummary.vue";
import AddGridDialog from "@/components/preprocess/AddGridDialog.vue";
import AgGridDialog from "@/components/preprocess/AgGridDialog.vue";
import AgSideMenu from "@/components/preprocess/AgSideMenu.vue";
import { eventBus } from "@/main";

import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
// import store from "@/store/modules/dataTable/aggrid";
import axios from "axios";

export default {
  data() {
    return {
      mergeTableRule: [
        v =>
          v.length <= 2 ||
          `현재는 한번에 2개의 테이블만 병합할 수 있습니다. (선택된 테이블 개수: ${v.length} )`
      ],
      show: false,
      devProgess: [
        {
          function: "Create Table (All Columns/Only Selected Columns)",
          singleTable: "mdi-check",
          mergedTable: "mdi-check"
        },
        {
          function: "Delete Table",
          singleTable: "mdi-check",
          mergedTable: "mdi-check"
        },
        {
          function: "Load Draft",
          singleTable: "mdi-check",
          mergedTable: "mdi-check"
        },
        {
          function: "Delete Draft",
          singleTable: "mdi-check",
          mergedTable: "mdi-check"
        },
        { function: "Delete Table", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Change Column Name", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Change Column Type", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Delete Row", singleTable: "mdi-check", mergedTable: "mdi-check" },
        // { function: "Update Row", singleTable: "mdi-close", mergedTable: "mdi-close" },
        { function: "Drop Column", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Fill NA", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Delete NA", singleTable: "mdi-check", mergedTable: "mdi-check" },
        { function: "Merge Tables", singleTable: "mdi-check", mergedTable: "mdi-check" },
        {
          function: "Export as Excel (Only Loaded)",
          singleTable: "mdi-check",
          mergedTable: "mdi-close"
        },
        { function: "Export as Excel (All)", singleTable: "mdi-check", mergedTable: "mdi-close" }
      ],
      viewStatus: 0,
      draftList: [],

      draftName: "",
      saveDialog: false,
      vchipClickedProp: {
        color: "primary"
      },
      hidePanel: true,
      dialog_merge: false,
      dialog_colType: false,
      dialog_newGrid: false,
      dialog_colDisplay: false,
      dialog_colName: false,
      dialog_fillNa: false,
      dialog_deleteNA: false,

      gridColumns: [],
      loadedColumns: [],

      tablesToMerge: [],
      dataTypes: null,
      sampleDataTypes: ["float", "int", "double"],
      dataTypeItems: ["double", "string", "bool", "date", "int", "long"]
    };
  },
  computed: {
    ...mapState({
      aggridWidth: state => state.initialData.aggridWidth,
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
      datatableName: state => state.aggrid.datatableName,

      gridList: state => state.aggrid.gridList,
      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      //loadSetting
      columnsForGrid: state => state.aggrid.columnsForGrid,
      columnModel: state => state.aggrid.columnModel,
      datasetToLoad: state => state.aggrid.datasetToLoad,
      gridType: state => state.aggrid.gridType
    }),
    ...mapGetters("aggrid", ["currentDataset"]),
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
    PlotlyDist,
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
    eventBus.$on("deleteRowsByGraph", selectedRows => {
      this.addNewDeletion(selectedRows);
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    });
  },
  mounted() {
    // this.$modal.show("my-first-modal");

    console.log("loadDraft");
    this.loadDraft();
  },
  methods: {
    ...mapActions("aggrid", ["createNewGrid"]),
    ...mapActions("aggrid", ["mergeTables"]),
    selectAll() {
      this.gridApi[this.currentGrid].selectAllFiltered();
    },
    test(value) {
      console.log(value);
    },
    iconColor(value) {
      if (value == "mdi-check") {
        return "blue";
      } else return "red";
    },
    shortcut() {
      eventBus.$emit("shortcut", "s");
    },
    dialogAction(dialogName) {
      if (dialogName == "changeColName") {
        this.getGridColumns();
        this.dialog_colName = !this.dialog_colName;
      } else if (dialogName == "changeColType") {
        this.getDataTypes();
      } else if (dialogName == "dropColumn") {
        this.dialog_colDisplay = true;
      } else if (dialogName == "saveDraft") {
        var confirmflag = confirm("Draft를 덮어씌우시겠습니까?");

        if (confirmflag) {
          this.saveDraft();
        } else {
        }
      } else if (dialogName == "fillNA") {
        this.dialog_fillNa = true;
      } else if (dialogName == "deleteNA") {
        this.dialog_deleteNA = true;
      } else if (dialogName == "mergeTable") {
        if (this.gridList.length < 2) {
          alert("Dataframe이 2개 이상 로드되어 있어야 합니다.");
        } else {
          this.dialog_merge = true;
        }
      }
    },

    getDataTypes() {
      let path = "http://localhost:8000/getDataTypes";
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
    ...mapMutations("aggrid", ["addNewDeletion"]),

    ...mapMutations("aggrid", ["addGridApi"]),
    ...mapMutations("aggrid", ["addGridColumnApi"]),
    ...mapMutations("aggrid", ["setCurrentGrid"]),
    ...mapMutations("aggrid", ["setViewMode"]),
    ...mapMutations("aggrid", ["resetAggrid"]),
    ...mapMutations("aggrid", ["setAvailableUndo"]),
    ...mapMutations("aggrid", ["setAvailableRedo"]),
    ...mapActions("aggrid", ["removeGrid"]),
    ...mapActions("aggrid", ["saveDraft"]),
    ...mapMutations("aggrid", ["setDatasetToLoad"]),
    ...mapMutations("aggrid", ["setColumnModel"]),
    ...mapMutations("aggrid", ["setGridType"]),
    ...mapActions("aggrid", ["createNewGrid"]),
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
      this.loadedColumns = vm.gridColumnApi[vm.currentGrid].getColumnState().map(function(col) {
        // return { columnName: col.getColId(), columnInfo: vm.currentGrid };
        return col.colId;
      });
    },
    // test() {
    //   var columnState = JSON.stringify(this.gridColumnApi[this.currentGrid].getColumnState());
    //   console.log(columnState);
    // },
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

    showAnalysis() {
      this.setViewMode("statistics");
    },

    dynamicVchipProp(gridID) {
      if (gridID == this.currentGrid) {
        return this.vchipClickedProp;
      }
    }
  }
};
</script>
<style scoped>
.modal-override {
  background: #00000000 !important;
  position: absolute;
  border-radius: 20px !important;
  padding: 10px;
}
.v--modal-overlay {
  background: rgba(0, 0, 0, 0) !important;
}
.vm--overlay {
  z-index: -1 !important;
  background: rgba(0, 0, 0, 0) !important;
}
.vm--modal {
  /* z-index: 2000 !important; */
}
.vm--container {
  /* z-index: -1 !important; */
}
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
