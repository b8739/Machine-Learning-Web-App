<template>
  <div class="mt-5">
    <div v-for="(option, index) in graphOptions" :key="index">
      <apexchart
        :ref="graphNames[index]"
        :type="graphType"
        :height="graphHeight"
        :options="option"
      ></apexchart>
    </div>
  </div>
</template>

<script>
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";
//vuex
import { eventBus } from "@/main";

import { mapState, mapGetters, mapActions } from "vuex";

export default {
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음
  props: ["graphNames", "graphOptions", "graphHeight", "graphType", "graphSource"],
  data() {
    return {
      actual: null,
      predictive: null,

      series: [[{ data: [] }]]

      // original

      //mainfirstChartOption
    };
  },

  watch: {
    graphSource: function(data) {
      this.updateChart();
    },
    chartStatus: function(data) {
      this.updateChart();
    }
  },
  created() {
    this.chartStatus = true;
  },
  mounted() {
    this.updateChart();
  },
  computed: {
    keysOfInstance() {
      return Object.keys(this.graphSource);
    },
    nameOfRefs() {
      return Object.keys(this.$refs);
    }
  },
  methods: {
    updateChart() {
      this.nameOfRefs.forEach((element, index) => {
        this.$refs[element][0].updateSeries([
          {
            name: "Actual",
            data: this.graphSource[this.keysOfInstance[index]]["Actual"]
          },
          {
            name: "Predictive",
            data: this.graphSource[this.keysOfInstance[index]]["Predictive"]
          }
        ]);
      });
    },

    //APEX CHART
    resetSeries() {
      this.numOfDragElement = 0;
      this.$refs.testChart[0].updateOptions(
        {
          series: [{}],
          xaxis: {
            categories: []
          }
        },
        false,
        false
      );
      console.log("reset");
    }
  }
};
</script>
<style scoped>
v-col {
  background-color: #000;
  border: 1px solid #000;
}
</style>
