<template>
  <div class="container">
    <!-- 테이블 -->
    <table class="dataTable">
      <tbody>
        <!-- 행 -->
        <tr
          v-for="(numericColumn, numericIndex) in numericColumns"
          :key="numericIndex"
          @click="openEditModal(dataSet[numericColumns[numericIndex]], dataSet['Date'], indexNum)"
        >
          <!-- 1st column -->
          <td>{{ numericColumn }}</td>
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
              <span>{{ numeric_quantileJson[numericColumn] }}</span>
            </tr>
            <tr>
              <span class="info_title">Num. of NA: </span>
              <span>{{ numeric_numOfNaJson[numericColumn] }}</span>
            </tr>
          </td>

          <!-- 4th column -->
          <td>
            <Histogram
              :dataValue="dataSet[numericColumns[numericIndex]]"
              :date="dataSet['Date']"
              :indexNum="indexNum"
            />
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
    <EditModal
      :class="{ visibilityHidden: editModal_hidden }"
      :dataValue="editModal_dataValue"
      :date="editModal_date"
      :indexNum="editModal_indexNum"
    />
    <portal-target name="destination"> </portal-target>
  </div>
</template>

<script>
import Histogram from "./Histogram";
import EditModal from "./EditModal";
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
      categoryIndex: 0,
      //editModal
      editModal_hidden: true,
      editModal_dataValue: {},
      editModal_date: {},
      editModal_indexNum: {}
    };
  },

  components: {
    Histogram,
    EditModal
  },
  props: ["columnsWithoutIndex", "summarizedData", "dataSet", "indexNum"],
  computed: {
    categoryIndexAddOne() {
      return this.categoryIndex++;
    }
  },
  methods: {
    openEditModal(dataSet, date, indexNum) {
      this.editModal_hidden = false;
      this.editModal_dataValue = dataSet;
      this.editModal_date = date;
      this.editModal_indexNum = indexNum;
    }
  },
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
<style scoped>
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
.dataTable tr:hover {
  background-color: #b1e6d2;
  cursor: pointer;
}
.dataTable tr:hover tr {
  background-color: #b1e6d2;
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
.visibilityHidden {
  display: none;
}
</style>
