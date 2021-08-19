<template>
  <tr>
    <!-- 1st Column -->
    <td>
      <v-row>
        <v-col cols="1"
          ><v-icon x-small class="pt-3" @click="saveClickedIconIndex(column)"
            >mdi-pencil</v-icon
          ></v-col
        >
        <v-col><v-text-field v-bind="activateName(column)" :value="column"></v-text-field> </v-col>
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
          single-line
          hide-details="true"
          height="20"
          :label="getDataType(column)"
        >
        </v-select>
      </tr>
    </td>

    <component v-bind:is="distinguishDataType(column)"></component>
  </tr>
</template>
<script>
export default {
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo
    }),
    ...mapGetters("initialData", ["numericColumns"]),
    renderStatus() {
      if (
        this.summarizedInfo != null &&
        this.columns.length != 0 &&
        this.duplicatedColumns.length != 0
      ) {
        return true;
      }
    },
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
    ...mapActions("initialData", ["loadSummarizedData"]),
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
    activateName(column) {
      if (this.clickedIconKey == column) {
        return this.activatedName_props;
      } else return this.inactivatedName_props;
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
    }
  }
};
</script>
<style scoped>
.container {
  max-width: 1200px;
  max-height: 100vh;
  overflow: scroll;
  /* margin: 0 auto; */
  margin-top: 50px;
}
.dataTable {
  text-transform: capitalize;
  font-size: 14px;

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
