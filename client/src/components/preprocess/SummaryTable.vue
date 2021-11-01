<template>
  <div v-if="columns.length != 0">
    <!-- {{ columnsWithoutID }} -->
    <div class="container">
      <!-- 테이블 -->
      <!-- <div>Original{{ columns }}</div>
      <br />
      <div>Duplicated{{ duplicatedColumns }}</div>
      <br />
      <div>backedUpColumns{{ backedUpColumns }}</div> -->

      <table class="dataTable">
        <draggable tag="table" v-model="duplicatedColumns">
          <!-- 행 -->
          <tbody v-for="(column, columnIndex) in columnsWithoutID" :key="columnIndex">
            <!-- Columns -->
            <component
              :is="distinguishDataType(columnsWithoutID[columnIndex])"
              :column="columnsWithoutID[columnIndex]"
            >
              <!-- slot -->

              <template>
                <!-- 1st column -->
                <td>
                  <v-row>
                    <v-col
                      ><v-text-field
                        v-bind="activateName"
                        :value="column"
                        @change="renameColumns(columnIndex, $event)"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </td>
                <!-- 2nd Column -->
                <td class="secondColumn">
                  <tr>
                    <span v-once class="info_title">Col #: </span>
                    <span v-once> {{ columnIndex }} </span>
                  </tr>
                  <tr>
                    <v-select
                      :items="dataTypes"
                      dense
                      @change="changeColumnType(columnIndex, $event)"
                      :disabled="!editStatus['summaryChangeType']"
                      single-line
                      hide-details="true"
                      height="20"
                      :label="getDataType(columnsWithoutID[columnIndex])"
                    >
                    </v-select>
                  </tr>
                </td>
              </template>
            </component>
          </tbody>
        </draggable>
      </table>
    </div>
    <EditModal />
    <ChangeOrder :duplicatedColumns="duplicatedColumns" />
  </div>
</template>

<script>
import Vue from "vue";
import EditModal from "@/components/modal/EditModal";

import NumericRow from "@/components/tableRow/NumericRow";
import CategoricalRow from "@/components/tableRow/CategoricalRow";
import DateRow from "@/components/tableRow/DateRow";
import draggable from "vuedraggable";
import axios from "axios";
import ChangeOrder from "@/components/changeOrder/ChangeOrder.vue";

//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      // duplicatedColumns: [],
      editModalDialog: false,
      sampleForClass: null,
      dataTypes: ["int16", "int32", "int64", "float32", "float64", "string", "datatime64"],

      inactivatedName_props: {
        disabled: true,
        "hide-details": true,
        dense: true
      },
      activatedName_props: {
        disabled: false,
        "hide-details": true,
        dense: true
      },
      clickedIconKey: null,

      // numeric/categorical columns
      categoricalColumns: {},
      //summary contents
      numeric_info: {
        mean: {},
        std: {},
        numOfNA: {},
        quantile_1: {},
        quantile_2: {},
        quantile_3: {},
        quantile_4: {}
      },
      category_info: {
        numOfNA: {},
        nunique: {},
        size: {}
      },

      categoryIndex: 0,
      //editModal
      editModal_hidden: true,
      editModal_dataValue: {},
      editModal_date: {},
      editModal_indexNum: {},
      editModal_darkenBackground: false,
      selectedColumnIndex: null,
      //etc (for dataset parsing)
      show_timeSeriesGraph: false,
      // save flag,
      newDataset: {},
      confirmFlag: false
    };
  },
  components: {
    DateRow,
    NumericRow,
    CategoricalRow,
    ChangeOrder,
    EditModal,

    draggable
  },

  watch: {},

  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      activatedEvent: state => state.preprocessHandler.activatedEvent,
      duplicatedColumns: state => state.summaryTableHandler.duplicatedColumns,
      backedUpColumns: state => state.summaryTableHandler.backedUpColumns
    }),
    ...mapGetters("initialData", ["numericColumns"]),
    columnsWithoutID() {
      let columnsWithoutID = [];
      this.columns.forEach(element => {
        if (element != "ID") {
          columnsWithoutID.push(element);
        }
      });
      return columnsWithoutID;
    },
    activateName() {
      if (this.editStatus["summaryChangeName"]) {
        return this.activatedName_props;
      } else return this.inactivatedName_props;
    },
    renderStatus() {
      if (
        this.summarizedInfo != null &&
        this.columns.length != 0 &&
        this.duplicatedColumns.length != 0
      ) {
        return true;
      }
    },

    numericSummary() {
      let numericColumn = Object.keys(this.summarizedInfo["numeric"]);
      let numericSummary = [];
      numericSummary = Object.keys(this.summarizedInfo["numeric"][numericColumn[0]]);
      return numericSummary;
    },
    categoryIndexAddOne() {
      return this.categoryIndex++;
    }
  },

  methods: {
    ...mapActions("apexchartGraph", ["loadFeatureGraphData"]),
    changeColumnType(index, event) {
      Vue.set(this.duplicatedColumns[index], "datatype", event);

      //       let path = "http://localhost:5000/changeColumnType";
      // this.$axios({
      //   method: "post",
      //   url: path,
      //   data: {
      //     case_name: this.case_name,
      //     duplicatedColumns: this.duplicatedColumns,
      //     tableName: this.tableName,

      //   }
      // }).then(function(res) {
      //   vm.loadCases();
      // });
    },
    openEditModal(column) {
      eventBus.$emit("openEditModal", column);
    },
    updateValues() {
      this.addDuplicatedColumn;
    },
    ...mapActions("initialData", ["loadSummarizedData"]),
    // ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapMutations("initialData", ["changeColumnName_vuex"]),
    ...mapMutations("saveFlag", ["ChangeColumnNameFlag"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),
    ...mapMutations("preprocessHandler", ["resetPreprocessVuex"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),
    ...mapMutations("summaryTableHandler", ["changeColumnOrder"]),
    renameColumns(index, event) {
      Vue.set(this.duplicatedColumns[index], "columnName", event);
    },
    saveClickedIconIndex(column) {
      // v-icon click OFF
      if (this.clickedIconKey == column) {
        this.clickedIconKey = null;
        // category 일 때

        // this.changeColumnName_vue(this.columns[index], index);

        // this.loadFundamentalData("http://localhost:5000/loadData"); //vuex column, dataset, indexnum 변경
        // this.loadSummarizedData();
      } // v-icon click ON
      else {
        this.clickedIconKey = column;
      }
    },

    getDataType(column) {
      return this.summarizedInfo["datatype"][column];
    },
    distinguishDataType(column) {
      if (this.getDataType(column) == "category" || this.getDataType(column) == "string") {
        return "CategoricalRow";
      } else if (
        this.getDataType(column).indexOf("int") == 0 ||
        this.getDataType(column).indexOf("float") == 0
      ) {
        return "NumericRow";
      } else {
        return "DateRow";
      }
    },

    // changeColumnOrder(position, movedColumnName, newIndex) {
    //   const api = "http://localhost:5000/changeColumnOrder";
    //   axios
    //     .get(api, {
    //       params: {
    //         position: position,
    //         movedColumnName: movedColumnName,
    //         newIndex: newIndex
    //       }
    //     })
    //     .then(res => {})
    //     .catch(error => {
    //       console.error(error);
    //     });
    // },
    changeColumnName_vue(newName, columnIndex) {
      let payload = { newName: newName, columnIndex: columnIndex };
      console.log(payload);
      // this.changeColumnName_vuex(payload); //summarizedInfo의 이름까지 변경해야하는 문제 때문에 일단 보류

      // const api = "http://localhost:5000/changeColumnName_vue";
      // axios
      //   .get(api, {
      //     params: {
      //       columnName: columnName,
      //       columnIndex: columnIndex
      //     }
      //   })
      //   .then(res => {})
      //   .catch(error => {
      //     console.error(error);
      //   });
    }
  },
  created() {
    this.selectionTimer = setTimeout(() => {
      this.loadFeatureGraphData();
      this.cloneOriginalArray();
    }, 1000);
    this.resetDataTableVuex();
    this.resetPreprocessVuex();
    this.$root.$refs.SummaryTable = this;

    // draggable

    eventBus.$on("columnOrderUpdated", duplicatedColumns => {
      duplicatedColumns.forEach((element, index) => {
        if (element != this.duplicatedColumns[index]) {
          let payload = { index: index, element: element };
          this.changeColumnOrder(payload);
        }
      });
    });
  },
  mounted() {
    console.log("summarytable mounted");
    // this.selectionTimer = setTimeout(() => {
    //   eventBus.$emit("dfMounted", true);
    // }, 1000);
    // this.$nextTick(function() {
    //   console.log("df mounted");
    //   eventBus.$emit("dfMounted", true);
    // });
  }
};
</script>
<style scoped>
.container {
  max-width: 1200px;
  max-height: 100vh;
  overflow: scroll;
  margin-top: 50px;
}
.dataTable .info_title {
  color: grey;
}

.dataTable {
  text-transform: capitalize;
  font-size: 14px;
  text-align: left;
  vertical-align: middle;
  border-radius: 5px;
  border-style: hidden; /* hide standard table (collapsed) border */
  box-shadow: 0 0 0 1px rgba(104, 102, 102, 0.644);
  /* this draws the table border  */
  /* background-color: #234; */
}
.dataTable td:first-child {
  font-weight: 600;
  font-size: 10px;
}
.dataTable .info_title {
  color: grey;
}
.dataTable td {
  padding: 15px 10px;
  border: 1px solid rgba(104, 102, 102, 0.644);
  border-bottom: none;
}
.secondColumn {
  max-width: 150px;
}
table,
table td,
table th {
  border: 1px solid rgba(104, 102, 102, 0.644);
  border-collapse: collapse;
}
</style>
