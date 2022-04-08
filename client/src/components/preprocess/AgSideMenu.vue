<template>
  <v-navigation-drawer height="110vh" v-model="drawer" absolute :mini-variant.sync="mini">
    <!-- User -->
    <!-- <v-list-item class="mt-10 px-2">
      <v-list-item-avatar>
        <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
      </v-list-item-avatar>

      <v-list-item-title>User123</v-list-item-title>

      <v-btn icon @click.stop="mini = !mini">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
    </v-list-item> -->
    <!-- Save -->
    <v-list dense>
      <!-- <v-row justify="end">
        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-row> -->
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Versions</v-list-item-title>
        </template>
        <!-- <v-list-item>
          <v-select
            :items="draftList"
            item-text="draftName"
            label="Select Draft"
            @input="loadDraft"
          ></v-select>
        </v-list-item> -->

        <v-list-item @click="openDialog('saveDraft')" :disabled="gridList.length == 0">
          <v-list-item-icon>
            <v-icon>mdi-book-plus-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>Save Draft</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>

    <!-- Row -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Edit Row</v-list-item-title>
        </template>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-list-item
              :disabled="gridList.length == 0"
              v-for="item in items.rowMenu"
              v-bind="attrs"
              v-on="on"
              :key="item.title"
              link
              @click="item.action"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </template>
          <span>
            Delete Selected Rows와 Delete Loaded Rows의 차이: <br />
            Delete Selected Rows: 마우스로 선택한 모든 데이터를 삭제 <br />
            Delete Loaded Rows: 테이블상에 로드된 (필터 적용된/그래프로 선택된) 모든 데이터를 삭제
            <br />
          </span>
        </v-tooltip>
      </v-list-group>
    </v-list>
    <!-- Column -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Edit Column</v-list-item-title>
        </template>
        <!-- || item.title == 'Drop Column' -->
        <v-list-item
          :disabled="gridList.length == 0"
          v-for="item in items.colMenu"
          :key="item.title"
          link
          @click="item.action(item.param)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <!-- Data Cleaning -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Data Cleaning</v-list-item-title>
        </template>
        <v-list-item
          :disabled="gridList.length == 0"
          v-for="item in items.cleaningMenu"
          :key="item.title"
          link
          @click="item.action(item.param)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <!-- Table -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Table Menu</v-list-item-title>
        </template>
        <!-- :disabled="item.title == 'Merge Tables'" -->
        <v-list-item
          v-for="item in items.tableMenu"
          :key="item.title"
          link
          @click="item.action(item.param)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <!-- Export -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Export (Excel)</v-list-item-title>
        </template>
        <v-list-item
          v-for="item in items.exportMenu"
          :key="item.title"
          link
          @click="item.action"
          :disabled="gridList.length == 0"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import axios from "axios";

import { mapState, mapGetters, mapMutations, mapActions } from "vuex";

export default {
  data() {
    return {
      drawer: true,
      mini: false,
      items: {
        tableMenu: [
          {
            title: "Merge Tables",
            icon: "mdi-pencil",
            action: this.openDialog,
            param: "mergeTable"
          }
        ],
        rowMenu: [
          // { title: "Update Row", icon: "mdi-pencil", action: this.deleteRows },
          { title: "Delete Selected Row(s)", icon: "mdi-delete", action: this.deleteSelectedRows }
          // { title: "Delete Loaded Row(s)", icon: "mdi-delete", action: this.deletedLoadedRows }
        ],
        colMenu: [
          {
            title: "Change Column Name",
            icon: "mdi-pencil",
            action: this.openDialog,
            param: "changeColName"
          },
          {
            title: "Change Column Type",
            icon: "mdi-flask",
            action: this.openDialog,
            param: "changeColType"
          },
          { title: "Drop Column", icon: "mdi-delete", action: this.openDialog, param: "dropColumn" }
        ],
        exportMenu: [
          { title: "Only Loaded Data", icon: "mdi-export", action: this.exportLoadedData },
          { title: "All Data", icon: "mdi-export", action: this.exportAllData }
        ],
        cleaningMenu: [
          { title: "Fill NA", icon: "mdi-basket-fill", action: this.openDialog, param: "fillNA" },
          { title: "Delete NA", icon: "mdi-delete", action: this.openDialog, param: "deleteNA" }
        ]
      },

      activeState: true
    };
  },
  computed: {
    ...mapState({
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
      gridType: state => state.aggrid.gridType,
      draftList: state => state.aggrid.draftList,
      //filter
      deleteModel: state => state.aggrid.deleteModel,
      // model

      renameModel: state => state.aggrid.renameModel,
      columnState: state => state.aggrid.columnState,
      typeModel: state => state.aggrid.typeModel,
      fillNaModel: state => state.aggrid.fillNaModel,
      deleteNaModel: state => state.aggrid.deleteNaModel,
      filterModel: state => state.aggrid.filterModel,
      gridType: state => state.aggrid.gridType
    })
  },
  methods: {
    ...mapMutations("aggrid", ["addNewDeletion"]),
    ...mapActions("aggrid", ["loadDraft"]),
    ...mapActions("aggrid", ["loadDraftList"]),

    deleteSelectedRows() {
      var confirmflag = confirm("선택되어 있는 행(들)을 삭제하시겠습니까?");

      if (confirmflag) {
        let selectedRows = this.gridApi[this.currentGrid].getSelectedRows().map(function(row) {
          return row["ID"];
        });
        this.addNewDeletion(selectedRows);
        this.gridApi[this.currentGrid].refreshInfiniteCache();
      } else {
      }
    },
    deletedLoadedRows() {
      var confirmflag = confirm("로드되어 있는 행(들)을 삭제하시겠습니까?");
    },
    //   Dialog
    openDialog(dialogName) {
      this.$emit("openDialog", dialogName);
    },
    //   Export
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
    getParams() {
      return { columnSeparator: this.getValue("#columnSeparator") };
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
    exportAllData() {
      // 1) Filter Model
      let filterModel;
      if (this.filterModel[this.currentGrid] != undefined) {
        filterModel = this.filterModel[this.currentGrid];
      } else {
        filterModel = {};
      }
      // 2) Delete Model
      let deleteModel;
      if (this.deleteModel[this.currentGrid] != undefined) {
        deleteModel = this.deleteModel[this.currentGrid];
      } else {
        deleteModel = [];
      }
      // 3) Rename Model
      let renameModel;
      if (this.renameModel[this.currentGrid] != undefined) {
        renameModel = this.renameModel[this.currentGrid];
      } else {
        renameModel = [];
      }
      // 3) Type Model
      let typeModel;
      if (this.typeModel[this.currentGrid] != undefined) {
        typeModel = this.typeModel[this.currentGrid];
      } else {
        typeModel = [];
      }
      // 4) fill Na Model

      let fillNaModel;
      if (this.fillNaModel[this.currentGrid] != undefined) {
        fillNaModel = this.fillNaModel[this.currentGrid];
      } else {
        fillNaModel = [];
      }
      // 5) delete Na Model

      let deleteNaModel;
      if (this.deleteNaModel[this.currentGrid] != undefined) {
        deleteNaModel = this.deleteNaModel[this.currentGrid];
      } else {
        deleteNaModel = [];
      }

      let path = "http://localhost:8000/exportAllData";
      // axios
      axios({
        method: "post",
        url: path,
        data: {
          projectName: this.projectName,
          tableName: this.datasetToLoad[this.currentGrid],
          filterModel: filterModel,
          gridType: this.gridType[this.currentGrid],
          columnModel: this.columnModel[this.currentGrid][this.datasetToLoad[this.currentGrid]],
          renameModel: renameModel,
          typeModel: typeModel,
          fillNaModel: fillNaModel,
          deleteNaModel: deleteNaModel,
          deleteModel: deleteModel
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
    }
  },

  mounted() {
    this.loadDraftList();
  }
};
</script>
