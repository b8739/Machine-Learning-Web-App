<template>
  <div ref="plotlyDist" v-show="viewMode == 'distribution'"></div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
let cloneDeep = require("lodash/cloneDeep");
export default {
  data() {
    return {
      distData: {
        CRIM: [376, 44, 34, 15, 14, 6, 4, 4, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        ZN: [370, 24, 23, 15, 10, 10, 9, 7, 6, 6, 5, 4, 4, 4, 3, 3, 1, 0, 0, 0],
        INDUS: [130, 51, 51, 48, 44, 39, 30, 24, 20, 17, 15, 15, 7, 5, 5, 3, 0, 0, 0, 0],
        CHAS: [469, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        NOX: [60, 53, 49, 45, 44, 41, 37, 32, 26, 24, 20, 16, 15, 14, 13, 8, 7, 0, 0, 0],
        RM: [105, 90, 71, 61, 40, 36, 28, 16, 12, 9, 9, 6, 6, 4, 3, 2, 2, 2, 1, 1],
        AGE: [110, 56, 37, 34, 24, 23, 23, 22, 22, 20, 19, 18, 18, 18, 17, 14, 9, 7, 7, 6],
        DIS: [91, 68, 57, 44, 43, 37, 32, 29, 27, 19, 15, 13, 11, 7, 6, 4, 1, 0, 0, 0],
        RAD: [130, 115, 110, 44, 38, 26, 24, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        TAX: [130, 86, 62, 47, 38, 37, 27, 22, 19, 17, 13, 5, 1, 0, 0, 0, 0, 0, 0, 0],
        PTRATIO: [138, 50, 43, 41, 38, 27, 26, 26, 25, 17, 16, 15, 13, 12, 10, 3, 2, 1, 1, 0],
        B: [364, 48, 23, 10, 10, 7, 7, 6, 5, 4, 3, 3, 3, 3, 2, 2, 2, 1, 1, 0],
        L7TAT: [60, 55, 53, 53, 46, 39, 38, 35, 28, 22, 18, 12, 11, 10, 9, 6, 3, 3, 2, 1],
        MEDV: [79, 75, 68, 46, 39, 38, 20, 19, 19, 16, 16, 15, 14, 12, 9, 6, 5, 5, 2, 1]
      },
      dataFormat: {
        type: "scatter",
        mode: "markers",
        marker: {
          size: 2
        },
        line: {
          width: 1
        }
      },

      data: [
        {
          type: "bar",
          //   mode: "markers",
          marker: {
            size: 2
            // marker is an object, valid marker keys: #scatter-marker
          },
          line: {
            // color: "rgb(219, 64, 82)",
            width: 1
          },

          showlegend: true
        }
      ],
      layout: {
        width: this.graphWidth,
        height: this.graphHeight,
        margin: {
          l: 30,
          r: 20,
          b: 20,
          t: 40,
          pad: 4
        },
        colorway: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],
        xaxis: {
          automargin: true
        },
        yaxis: {
          automargin: true
        },
        title: {
          text: "Distribution (Sample: boston.csv)"
        },
        grid: {
          rows: 7,
          columns: 3,
          pattern: "independent"
        }
      },
      config: {
        showSendToCloud: false,
        displaylogo: false,
        responsive: true,
        showEditInChartStudio: false,

        modeBarButtonsToRemove: ["sendDataToCloud"]
      }
    };
  },
  props: ["graphWidth", "graphHeight", "isEdit"],
  computed: {
    ...mapState({
      projectName: state => state.initialData.projectName,
      viewMode: state => state.aggrid.viewMode
    }),
    plotContainer() {
      return this.$refs["plotlyDist"];
    }
  },
  methods: {
    createPlot() {
      let data = [];
      let axisIndex = 1;
      Object.keys(this.distData).forEach(col => {
        axisIndex++;
        let trace = {
          x: this.distData[col],
          type: "bar",
          name: col
        };

        trace["xaxis"] = "x" + axisIndex;
        trace["yaxis"] = "y" + axisIndex;
        // console.log(trace["xaxis"]);
        data.push(trace);
      });

      Plotly.newPlot(this.plotContainer, data, this.layout, this.config);
    }
  },
  created() {},
  mounted() {
    this.createPlot();
  }
};
</script>
<style scoped></style>
