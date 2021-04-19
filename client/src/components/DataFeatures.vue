<template>
  <div class="container">
    <!-- 테이블 -->
    <table class="dataTable">
      <tbody>
        <!-- 행 -->
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
            {{ numericColumn }}
          </td>
          <!-- 2nd column -->
          <td>
            <tr>
              <span class="info_title">Col #: </span>
              <span> {{ numericIndex }} </span>
            </tr>
            <tr>
              <span class="info_title">Type: </span>
              <span> Numeric </span>
            </tr>
          </td>

          <!-- 3rd column -->
          <td>
            <tr>
              <span class="info_title">Mean: </span>
              <span>{{ numeric_meanJson[numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Standard Deviation: </span>
              <span>{{ numeric_stdJson[numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Quantile: </span>
              <span>{{ numeric_quantile1[numericColumn] }}, </span>
              <span>{{ numeric_quantile2[numericColumn] }}, </span>
              <span>{{ numeric_quantile3[numericColumn] }}, </span>
              <span>{{ numeric_quantile4[numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ numeric_numOfNaJson[numericColumn] }}</span>
            </tr>
          </td>

          <td>
            <span class="tdTitle">Distribution</span>
            <Histogram
              :distribution="summarizedInfo[4][numericIndex]"
              :interval="summarizedInfo[5][numericIndex]"
              :indexNum="indexNum"
            />
          </td>
          <!-- 4th column -->
          <td>
            <span class="tdTitle" @click="showTimeSeriesGraph()">Time Series Graph</span>
            <TimeSeries
              :rawDataset="dataset[numericColumns[numericIndex]]"
              :date="dataset['ts']"
              :indexNum="indexNum"
              :graphWidth="graphWidth"
              :graphHeight="graphHeight"
              :seriesName="numericColumns[numericIndex]"
            />
          </td>
        </tr>
        <!-- v-if="show_timeSeriesGraph" -->
        <!-- category start -->
        <tr v-for="(categoricalColumn, categoryIndex) in categoricalColumns" :key="categoryIndex">
          <!-- 열 -->
          <td>{{ categoricalColumn }}</td>
          <td>
            <tr>
              <span class="info_title">Col #: </span>
              <span> {{ categoryIndexAddOne }} </span>
            </tr>
            <tr>
              <span class="info_title">Type: </span>
              <span> Categorical </span>
            </tr>
          </td>

          <td>
            <!-- <tr>
              <span class="info_title">Most Common Value: </span>
              <span>{{ categorical_mostCommon[categoricalColumn] }}</span>
            </tr> -->
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ categorical_numOfNaJson[categoricalColumn] }}</span>
            </tr>
          </td>

          <td></td>
        </tr>
      </tbody>
    </table>
    <EditModal
      :class="{ visibilityHidden: editModal_hidden }"
      :dataValue="editModal_dataValue"
      :date="editModal_date"
      :indexNum="editModal_indexNum"
      :columns="columns"
      @newEditModalStatus="closeEditModal"
      :editModal_hidden="editModal_hidden"
      :selectedColumnIndex="selectedColumnIndex"
    />
    <portal-target name="destination"> </portal-target>
  </div>
</template>

<script>
import TimeSeries from "./charts/TimeSeries";
import Histogram from "./charts/Histogram";
import EditModal from "./modal/EditModal";
//vuex
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
import { mapMutations } from "vuex";

import { eventBus } from "@/main";

export default {
  data() {
    return {
      graphWidth: "260px",
      graphHeight: "200px",
      // numeric/categorical columns
      numericColumns: {},
      categoricalColumns: {},
      //summary contents
      numeric_meanJson: {},
      numeric_stdJson: {},
      // numeric_quantileJson: {},
      numeric_numOfNaJson: {},
      // quantile
      numeric_quantile1: null,
      numeric_quantile2: null,
      numeric_quantile3: null,
      numeric_quantile4: null,
      categorical_mostCommon: {},
      categorical_numOfNaJson: {},
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
    Histogram
  },
  props: ["columnsWithoutIndex"],

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
    ...mapMutations("initialData", ["setHadLoaded"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    // divideArrayByName(jsonObject) {
    //   let tempArray;
    //   let name;
    //   for (const key in jsonObject) {
    //     name = jsonObject["Name"];
    //     tempArray.push(jsonObject[key]);
    //   }
    // },
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
    }
  },

  created() {
    this.numeric_meanJson = this.summarizedInfo[0]["mean"];
    this.numeric_stdJson = this.summarizedInfo[0]["std"];

    this.numeric_quantile1 = this.summarizedInfo[0]["quantile1"];
    this.numeric_quantile2 = this.summarizedInfo[0]["quantile2"];
    this.numeric_quantile3 = this.summarizedInfo[0]["quantile3"];
    this.numeric_quantile4 = this.summarizedInfo[0]["quantile4"];

    this.numeric_numOfNaJson = this.summarizedInfo[0]["numOfNA"];

    // this.categorical_mostCommon = this.summarizedInfo[1]["mostCommon"];
    this.categorical_numOfNaJson = this.summarizedInfo[1]["numOfNA"];

    this.numericColumns = this.summarizedInfo[2];
    this.categoricalColumns = this.summarizedInfo[3];
    this.categoryIndex = this.summarizedInfo[2].length;
  },
  mounted() {
    // for (const value in this.dataSet) {
    //   // console.log("mounted");
    //   console.log(this.dataSet[value]);
    // }
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
  font-size: 15px;
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
  padding: 15px;
  border: 1.5px solid rgba(104, 102, 102, 0.644);
}
.dataTable .info_title {
  color: grey;
}
.visibilityHidden {
  display: none;
}
</style>
