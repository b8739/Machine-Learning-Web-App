<template>
  <div>
    <div class="container">
      <!-- 테이블 -->
      <div>Duplicated{{ duplicatedColumns }}</div>
      <div>Original{{ columns }}</div>

      <table class="dataTable">
        <draggable tag="table" v-model="duplicatedColumns" @change="onDragEvent">
          <!-- 행 -->
          <tbody v-for="(column, columnIndex) in duplicatedColumns" :key="columnIndex">
            <!-- Columns -->
            <component
              :is="distinguishDataType(columns[columnIndex])"
              :column="columns[columnIndex]"
            >
              <!-- slot -->
              <!-- 1st column -->
              <template>
                <td>
                  <v-row>
                    <!-- <v-col cols="1"
                      ><v-icon
                        v-show="editStatus[preprocessStatus]"
                        x-small
                        class="pt-3"
                        @click="saveClickedIconIndex(columns[columnIndex])"
                        >mdi-pencil</v-icon
                      ></v-col
                    > -->
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
                      :items="categoryTypes"
                      dense
                      :disabled="!editStatus['summaryChangeType']"
                      single-line
                      hide-details="true"
                      height="20"
                      :label="getDataType(column)"
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
  </div>
</template>

<script>
import Vue from "vue";
import NumericRow from "@/components/tableRow/NumericRow";
import CategoricalRow from "@/components/tableRow/CategoricalRow";
import DateRow from "@/components/tableRow/DateRow";
import draggable from "vuedraggable";
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      duplicatedColumns: [],
      editModalDialog: false,
      sampleForClass: null,
      categoryTypes: ["Category", "String", "Text", "Time-Series"],
      numericTypes: ["Numeric", "Float", "Int"],

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

    draggable
  },

  watch: {
    summarizedInfo: function(data) {
      deep: true, this.loadDataSummary();
    }
  },

  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      activatedEvent: state => state.preprocessHandler.activatedEvent
    }),
    ...mapGetters("initialData", ["numericColumns"]),
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
    ...mapActions("initialData", ["loadSummarizedData"]),
    // ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapMutations("initialData", ["changeColumnName_vuex"]),
    ...mapMutations("saveFlag", ["ChangeColumnNameFlag"]),
    renameColumns(columnIndex, event) {
      Vue.set(this.duplicatedColumns, columnIndex, event);
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
      if (this.getDataType(column) == "category") {
        return "CategoricalRow";
      } else if (this.getDataType(column) == "numeric") return "NumericRow";
      else {
        return "DateRow";
      }
    },
    onDragEvent(evt) {
      // let movedColumnName = evt.moved.element;
      // let oldIndex = evt.moved.oldIndex + 3;
      // let newIndex = evt.moved.newIndex + 3;
      // //컬럼 left 이동
      // if (oldIndex > newIndex) {
      //   this.changeColumnOrder("left", movedColumnName, newIndex);
      // }
      // //컬럼 right 이동
      // else {
      //   this.changeColumnOrder("right", movedColumnName, newIndex);
      // }
    },
    changeColumnOrder(position, movedColumnName, newIndex) {
      const api = "http://localhost:5000/changeColumnOrder";
      axios
        .get(api, {
          params: {
            position: position,
            movedColumnName: movedColumnName,
            newIndex: newIndex
          }
        })
        .then(res => {})
        .catch(error => {
          console.error(error);
        });
    },
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
    },

    loadDataSummary() {
      // // numeric
      // for (const key in this.numeric_info) {
      //   this.numeric_info[key] = this.summarizedInfo["numeric"][key];
      // }
      // // category
      // for (const key in this.category_info) {
      //   this.category_info[key] = this.summarizedInfo["categorical"][key];
      // }
      // this.sampleForClass = this.summarizedInfo["sampleForClass"];
    },
    duplicateColumns() {
      this.duplicatedColumns.splice(0, this.duplicatedColumns.length);
      this.columns.forEach(element => {
        this.duplicatedColumns.push(element);
      });
    }
  },
  created() {
    this.$root.$refs.dataFeatures = this;
    this.loadDataSummary();
    this.selectionTimer = setTimeout(() => {
      this.duplicateColumns();
    }, 1000);
    // draggable

    eventBus.$on("columnOrderUpdated", duplicatedColumns => {
      this.duplicatedColumns.splice(0, this.duplicatedColumns.length);
      duplicatedColumns.forEach(element => {
        this.duplicatedColumns.push(element);
      });
    });
  },
  mounted() {
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
