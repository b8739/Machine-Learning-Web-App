<template>
  <div class="container">
    <!-- 테이블 -->
    <table class="dataTable">
      <tbody>
        <!-- 행 -->
        <tr v-for="(column, columnIndex) in columns" :key="columnIndex">
          <!-- Columns -->

          <!-- 1st Column -->
          <td>
            <v-row>
              <v-col cols="1"
                ><v-icon x-small class="pt-3" @click="saveClickedIconIndex(columnIndex)"
                  >mdi-pencil</v-icon
                ></v-col
              >
              <v-col
                ><v-text-field
                  v-bind="checkClickedIconIndex(columnIndex)"
                  :value="column"
                  v-model="columns[columnIndex]"
                ></v-text-field
              ></v-col>
            </v-row>
          </td>
          <!-- 2nd Column -->
          <td class="secondColumn">
            <tr>
              <span class="info_title">Col #: </span>
              <span> {{ columnIndex }} </span>
            </tr>
            <tr>
              <v-select
                :items="categoryTypes"
                dense
                single-line
                hide-details="true"
                height="20"
                label="Category"
              >
              </v-select>
            </tr>
          </td>

          <!-- 3rd Column -->
          <!-- category 일 경우: category summary 표시 -->
          <td v-if="distinguishDataType(column)">
            <tr
              v-for="(summary, categorySummaryIndex) in categorySummary"
              :key="categorySummaryIndex"
            >
              <span class="info_title">{{ summary }} </span>
              <span>: {{ summarizedInfo["categorical"][column][summary] }}</span>
            </tr>
          </td>

          <!-- numeric 일 경우: numeric summary 표시 -->
          <td v-else>
            <tr>
              <span class="info_title">Mean </span>
              <span>: {{ summarizedInfo["numeric"][column]["mean"] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num of NA </span>
              <span>: {{ summarizedInfo["numeric"][column]["numOfNA"] }}</span>
            </tr>
            <tr>
              <span class="info_title">StD </span>
              <span>: {{ summarizedInfo["numeric"][column]["std"] }}</span>
            </tr>
            <tr>
              <span class="info_title">Quantile </span>
              <span>: {{ summarizedInfo["numeric"][column]["Q1"] }}, </span>
              <span>{{ summarizedInfo["numeric"][column]["Q2"] }}, </span>
              <span>{{ summarizedInfo["numeric"][column]["Q3"] }}, </span>
              <span>{{ summarizedInfo["numeric"][column]["Q4"] }}, </span>
            </tr>
          </td>

          <!-- 4th Column -->
          <!-- category 일 경우: sample for class 표시 -->
          <td v-if="distinguishDataType(column)">
            <p class="info_title">Samples For Class:</p>
            <v-row
              no-gutters
              v-for="(sample, sampleIndex) in summarizedInfo['sampleForClass'][column]"
              :key="sampleIndex"
            >
              <v-col class="py-0"> {{ sampleIndex }}</v-col>
              <v-spacer></v-spacer>
              <v-col class="py-0">{{ sample }}% </v-col>
              <v-col cols="12" class="pa-0"><v-divider></v-divider></v-col>
            </v-row>
          </td>
          <!-- numeric 일 경우: distribution 표시 -->
          <td v-else>
            <span class="tdTitle">Distribution</span>
            <Histogram
              :distribution="summarizedInfo['distribution'][column]"
              :interval="summarizedInfo['interval'][column]"
              :indexNum="indexNum"
            />
          </td>
          <!-- category 일 경우: -- 표시 -->
          <td v-if="distinguishDataType(column)"></td>
          <!-- numeric 일 경우: Graph 표시 -->
          <td v-else>
            <span class="tdTitle" @click="showTimeSeriesGraph()">Graph</span>
            <TimeSeries
              :rawDataset="dataset[column]"
              :date="dataset['ts']"
              :graphWidth="graphWidth"
              :graphHeight="graphHeight"
              :seriesName="column"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <!-- <EditModal
      :class="{ visibilityHidden: editModal_hidden }"
      :dataValue="editModal_dataValue"
      :date="editModal_date"
      :indexNum="editModal_indexNum"
      :columns="columns"
      @newEditModalStatus="closeEditModal"
      :editModal_hidden="editModal_hidden"
      :selectedColumnIndex="selectedColumnIndex"
    /> -->
    <portal-target name="destination"> </portal-target>
  </div>
</template>

<script>
import TimeSeries from "@/components/charts/TimeSeries";
import Histogram from "@/components/charts/Histogram";
import EditModal from "@/components/modal/EditModal";
import draggable from "vuedraggable";
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      sampleForClass: null,
      categoryTypes: ["Category", "String", "Text", "Time-Series"],
      numericTypes: ["Numeric", "Float", "Int"],

      disabledTextFieldProps: {
        disabled: true,
        "hide-details": true,
        dense: true
      },
      abledTextFieldProps: {
        disabled: false,
        "hide-details": true,
        dense: true
      },
      clickedIconIndex: null,
      totalColumns: [],
      graphWidth: "260px",
      graphHeight: "200px",
      // numeric/categorical columns
      numericColumns: {},
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
      show_timeSeriesGraph: false
    };
  },
  components: {
    TimeSeries,
    EditModal,
    Histogram,
    draggable
  },
  props: ["columnsWithoutIndex"],
  watch: {
    summarizedInfo: function(data) {
      deep: true, this.loadDataSummary();
    }
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      summarizedInfo: state => state.initialData.summarizedInfo
    }),
    ...mapGetters("initialData", ["columns", "indexNum"]),
    categorySummary() {
      let categoricalColumn = Object.keys(this.summarizedInfo["categorical"]);
      let categorySummary = [];
      categorySummary = Object.keys(this.summarizedInfo["categorical"][categoricalColumn[0]]);
      return categorySummary;
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
    ...mapMutations("initialData", ["changeColumnName_vuex"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    distinguishDataType(column) {
      let dataType = this.summarizedInfo["datatype"][column]["type"];
      if (dataType == "category") {
        return true;
      } else if (dataType == "numeric") return false;
    },
    onDragEvent(evt) {
      let movedColumnName = evt.moved.element;
      let oldIndex = evt.moved.oldIndex + 3;
      let newIndex = evt.moved.newIndex + 3;
      //컬럼 left 이동
      if (oldIndex > newIndex) {
        this.changeColumnOrder("left", movedColumnName, newIndex);
      }
      //컬럼 right 이동
      else {
        this.changeColumnOrder("right", movedColumnName, newIndex);
      }
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
    changeColumnName(newName, columnIndex) {
      let payload = { newName: newName, columnIndex: columnIndex };
      console.log(payload);
      this.changeColumnName_vuex(payload);
      // const api = "http://localhost:5000/changeColumnName";
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
    saveClickedIconIndex(index) {
      // v-icon click OFF
      if (this.clickedIconIndex == index) {
        this.clickedIconIndex = null;
        // category 일 때
        if (index < 2 && this.categoricalColumns[index]) {
          console.log(this.columns[index]);
          this.changeColumnName(this.categoricalColumns[index], index);
        }
        //numeric 일 때
        else if (index >= 2 && this.numericColumns[index]) {
          this.changeColumnName(this.numericColumns[index - 2], index);
        }
        // this.loadFundamentalData("http://localhost:5000/loadData"); //vuex column, dataset, indexnum 변경
        // this.loadSummarizedData();
      } // v-icon click ON
      else {
        this.clickedIconIndex = index;
      }
    },
    checkClickedIconIndex(index) {
      if (this.clickedIconIndex == index) {
        return this.abledTextFieldProps;
      } else return this.disabledTextFieldProps;
    },
    openEditModal(dataset, date, indexNum, selectedColumnIndex) {
      this.editModal_hidden = false;
      this.editModal_dataValue = dataset;
      this.editModal_date = date;
      this.editModal_indexNum = indexNum;
      this.selectedColumnIndex = selectedColumnIndex;
    },
    closeEditModal() {
      this.editModal_hidden = true;
      // this.editModal_dataValue = {};
      // this.editModal_date = {};
      // this.editModal_indexNum = {};
    },
    showTimeSeriesGraph() {
      this.show_timeSeriesGraph = !this.show_timeSeriesGraph;
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
    }
  },
  created() {
    this.loadDataSummary();
    this.totalColumns = this.columns;
  },
  mounted() {
    console.log("datafeature mounted");
  }
};
</script>
<style scoped>
.container {
  max-width: 1200px;
  max-height: 100vh;
  overflow: scroll;
}
.dataTable {
  text-transform: capitalize;
  font-size: 14px;
  /* margin: 0 auto; */
  margin-top: 50px;
  text-align: left;
  vertical-align: middle;
  border-collapse: collapse;
  border-radius: 5px;
  border-style: hidden; /* hide standard table (collapsed) border */
  box-shadow: 0 0 0 1px rgba(104, 102, 102, 0.644);
  /* this draws the table border  */
  /* background-color: #234; */
}
.dataTable tr {
  /* background-color: #ecf1f6; */
}
.dataTable .tdTitle {
  display: inline-block;
  text-align: center;
  width: 95%;
}
.dataTable tr:hover {
  /* background-color: #b1e6d2; */
  cursor: pointer;
}
.dataTable tr:hover tr {
  /* background-color: #b1e6d2; */
}
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  padding: 15px 10px;
  border: 1px solid rgba(104, 102, 102, 0.644);
  /* border-bottom: none; */
}
.dataTable .info_title {
  color: grey;
}
.visibilityHidden {
  display: none;
}
.secondColumn {
  max-width: 150px;
}
</style>
