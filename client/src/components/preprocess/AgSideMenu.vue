<template>
  <v-navigation-drawer height="100vh" v-model="drawer" absolute :mini-variant.sync="mini">
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
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Versions</v-list-item-title>
        </template>
        <v-list-item>
          <v-select
            :items="draftList"
            item-text="draftName"
            label="Select Draft"
            @input="loadDraft"
          ></v-select>
        </v-list-item>

        <v-list-item @click="openDialog('saveDraft')">
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
        <v-list-item v-for="item in items.rowMenu" :key="item.title" link @click="item.action">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
    <!-- Column -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Edit Column</v-list-item-title>
        </template>
        <v-list-item
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
    <!-- Export -->
    <v-list dense>
      <v-list-group v-model="activeState">
        <template v-slot:activator>
          <v-list-item-title active>Export (Excel)</v-list-item-title>
        </template>
        <v-list-item v-for="item in items.exportMenu" :key="item.title" link @click="item.action">
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
      draftList: [],
      drawer: true,
      mini: false,
      items: {
        rowMenu: [
          { title: "Update Row", icon: "mdi-pencil", action: this.deleteRows },
          { title: "Delete Row", icon: "mdi-delete", action: this.deleteRows }
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
          { title: "Fill NA", icon: "mdi-basket-fill", action: this.openDialog, param: "fillNA" }
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
      gridType: state => state.aggrid.gridType
    })
  },
  methods: {
    ...mapMutations("aggrid", ["addNewDeletion"]),
    ...mapActions("aggrid", ["loadDraft"]),

    deleteRows() {
      let selectedRows = this.gridApi[this.currentGrid].getSelectedRows();
      this.addNewDeletion(selectedRows);
      this.gridApi[this.currentGrid].refreshInfiniteCache();
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
    // draft
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
    }
  },

  mounted() {
    this.loadDraftList();
  }
};
</script>
