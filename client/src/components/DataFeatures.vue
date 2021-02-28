<template>
  <div class="container">
    <!-- 테이블 -->
    <table class="dataTable">
      <tbody>
        <!-- 행 -->
        <tr v-for="(numericColumn, numericIndex) in numericColumns" :key="numericIndex">
          <!-- 열 -->
          <td>{{ numericColumn }}</td>
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
              <span>{{ numeric_quantileJson[numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ numeric_numOfNaJson[numericColumn] }}</span>
            </tr>
          </td>

          <td>
            <Histogram :dataValue="dataSet[numericColumns[numericIndex]]" :indexNum="indexNum" />
          </td>
        </tr>

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
            <tr>
              <span class="info_title">Most Common Value: </span>
              <span>{{ categorical_mostCommon[categoricalColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ categorical_numOfNaJson[categoricalColumn] }}</span>
            </tr>
          </td>

          <td></td>
        </tr>
      </tbody>
    </table>
    <td></td>
  </div>
</template>

<script>
import Histogram from "./Histogram";
// import Histogram from "../components/Histogram";
export default {
  data() {
    return {
      // numeric/categorical columns
      numericColumns: {},
      categoricalColumns: {},
      //summary contents
      numeric_meanJson: {},
      numeric_stdJson: {},
      numeric_quantileJson: {},
      numeric_numOfNaJson: {},
      categorical_mostCommon: {},
      categorical_numOfNaJson: {},
      categoryIndex: 0
    };
  },

  components: {
    Histogram
  },
  props: ["columnsWithoutIndex", "summarizedData", "dataSet", "indexNum", "thisistest"],
  computed: {
    categoryIndexAddOne() {
      return this.categoryIndex++;
    }
  },
  methods: {},
  created() {
    console.log("created");
    this.numeric_meanJson = this.summarizedData[0]["mean"];
    this.numeric_stdJson = this.summarizedData[0]["std"];
    this.numeric_quantileJson = this.summarizedData[0]["quantile"];
    this.numeric_numOfNaJson = this.summarizedData[0]["numOfNA"];
    this.categorical_mostCommon = this.summarizedData[1]["mostCommon"];
    this.categorical_numOfNaJson = this.summarizedData[1]["numOfNA"];
    this.numericColumns = this.summarizedData[2];
    this.categoricalColumns = this.summarizedData[3];
    this.categoryIndex = this.summarizedData[2].length;
  },
  mounted() {
    console.log("mounted");
    // for (const value in this.dataSet) {
    //   // console.log("mounted");
    //   console.log(this.dataSet[value]);
    // }
    console.log(this.dataSet["ID"]);

    //실험
    // console.log(jsonValuesIntoArray(this.dataSet["petal_length"]));
  }
};
</script>
<style>
.container {
  max-width: 1200px;
}
.dataTable {
  text-transform: capitalize;
  font-size: 15px;
  margin: 0 auto;
  margin-top: 100px;
  text-align: center;
  vertical-align: middle;
  transform: translateX(8%);
}
.dataTable tr {
  background-color: #ecf1f6;
}
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  border-right: 0.5px solid rgba(209, 229, 219, 0.8);
  padding: 15px;
}
.dataTable .info_title {
  color: grey;
}
</style>
