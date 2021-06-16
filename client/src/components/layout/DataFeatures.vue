<template>
  <div class="container">
    <!-- 테이블 -->
    <table class="dataTable">
      <tbody>
        <!-- 행 -->

        <!-- category start -->
        <tr v-for="(categoricalColumn, categoryIndex) in categoricalColumns" :key="categoryIndex">
          <!-- 열 -->
          <td>
            <v-row>
              <v-col cols="1"
                ><v-icon x-small class="pt-3" @click="saveClickedIconIndex(categoryIndex)"
                  >mdi-pencil</v-icon
                ></v-col
              >
              <v-col
                ><v-text-field
                  v-bind="checkClickedIconIndex(categoryIndex)"
                  :value="categoricalColumn"
                  v-model="categoricalColumns[categoryIndex]"
                ></v-text-field
              ></v-col>
            </v-row>
          </td>
          <td>
            <tr>
              <span class="info_title">Col #: </span>
              <span> {{ categoryIndex }} </span>
            </tr>
            <tr>
              <!-- <span class="info_title">Type: </span> -->
              <!-- <span> Categorical </span> -->

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

          <td>
            <!-- <tr>
              <span class="info_title">Most Common Value: </span>
              <span>{{ categorical_mostCommon[categoricalColumn] }}</span>
            </tr> -->
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ category_info["numOfNA"][categoricalColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Size:</span>
              <span>{{ category_info["size"][categoricalColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Unique Values:</span>
              <span>{{ category_info["nunique"][categoricalColumn] }}</span>
            </tr>
          </td>

          <td>
            <span class="info_title">Samples For Class:</span>
          </td>
        </tr>

        <tr v-for="(numericColumn, numericIndex) in numericColumns" :key="numericIndex">
          <!-- 1st column -->
          <td
            @click="
              openEditModal(
                dataset[numericColumns[numericIndex]],
                dataset['ts'],
                indexNum,
                numericIndex
              )
            "
          >
            <v-row>
              <v-col cols="1" class="pt-5">
                <v-icon x-small @click="saveClickedIconIndex(numericIndex + 2)"
                  >mdi-pencil</v-icon
                ></v-col
              >
              <v-col>
                <v-text-field
                  v-bind="checkClickedIconIndex(numericIndex + 2)"
                  :value="numericColumn"
                  v-model="numericColumns[numericIndex]"
                ></v-text-field
              ></v-col>
            </v-row>
          </td>
          <!-- 2nd column -->
          <td>
            <tr>
              <span class="info_title">Col #: </span>
              <span> {{ numericIndex + 2 }} </span>
            </tr>
            <tr>
              <!-- <span class="info_title">Type: </span>
              <span> Numeric </span> -->
              <v-select
                :items="numericTypes"
                dense
                single-line
                hide-details="true"
                height="20"
                label="Numeric"
              >
              </v-select>
            </tr>
          </td>

          <!-- 3rd column -->
          <td>
            <tr>
              <span class="info_title">Mean: </span>
              <span>{{ numeric_info["mean"][numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Standard Deviation: </span>
              <span>{{ numeric_info["std"][numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Quantile: </span>
              <span>{{ numeric_info["quantile_1"][numericColumn] }}, </span>
              <span>{{ numeric_info["quantile_2"][numericColumn] }}, </span>
              <span>{{ numeric_info["quantile_3"][numericColumn] }}, </span>
              <span>{{ numeric_info["quantile_4"][numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ numeric_info["numOfNA"][numericColumn] }}</span>
            </tr>
          </td>

          <!-- 4th column -->
          <td>
            <span class="tdTitle">Distribution</span>
            <Histogram
              :distribution="summarizedInfo['distribution'][numericIndex]"
              :interval="summarizedInfo['interval'][numericIndex]"
              :indexNum="indexNum"
            />
          </td>
          <!-- 5th column -->
          <td>
            <span class="tdTitle" @click="showTimeSeriesGraph()">Graph</span>
            <TimeSeries
              :rawDataset="dataset[numericColumns[numericIndex]]"
              :date="dataset['ts']"
              :graphWidth="graphWidth"
              :graphHeight="graphHeight"
              :seriesName="numericColumns[numericIndex]"
            />
          </td>
        </tr>
        <!-- v-if="show_timeSeriesGraph" -->
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
      indexNum: state => state.initialData.indexNum,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo
    }),

    categoryIndexAddOne() {
      return this.categoryIndex++;
    }
  },
  methods: {
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["changeColumnName_vuex"]),
    ...mapActions("initialData", ["loadFundamentalData"]),

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
    changeColumnName(columnName, columnIndex) {
      const api = "http://localhost:5000/changeColumnName";
      axios
        .get(api, {
          params: {
            columnName: columnName,
            columnIndex: columnIndex
          }
        })
        .then(res => {})
        .catch(error => {
          console.error(error);
        });
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
        this.loadFundamentalData("http://localhost:5000/loadData"); //vuex column, dataset, indexnum 변경
        this.loadSummarizedData();
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
      // numeric
      for (const key in this.numeric_info) {
        this.numeric_info[key] = this.summarizedInfo["summary"]["numeric"][key];
      }
      // category
      for (const key in this.category_info) {
        this.category_info[key] = this.summarizedInfo["summary"]["category"][key];
      }
      this.numericColumns = this.summarizedInfo["columns"]["numeric"];
      this.categoricalColumns = this.summarizedInfo["columns"]["category"];
    }
  },
  created() {
    this.loadDataSummary();
    this.totalColumns = this.columns;
  },
  mounted() {
    console.log("datafeature mounted");
    // for (const value in this.dataSet) {
    //   // console.log("mounted");
    //   console.log(this.dataSet[value]);
    //
    //실험
    // console.log(jsonValuesIntoArray(this.dataSet["petal_length"]));
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
</style>
