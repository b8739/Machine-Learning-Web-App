<template>
  <div v-if="featureGraphData != undefined" :ref="refName"></div>
</template>
<script>
import { eventBus } from "@/main";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

// import { Plotly } from "vue-plotly";

export default {
  data() {
    return {
      trace: [
        {
          y: [],
          x0: 1,
          // dx: 0,
          // nbinsy: 20,
          type: "bar",
          // opacity: 0.8,
          // ybins: {
          //   start: 0,
          //   end: 0
          //   // size: 20
          // },
          marker: {
            size: 2
            // marker is an object, valid marker keys: #scatter-marker
          },
          line: {
            // color: "rgb(219, 64, 82)",
            width: 1
          }
          // showlegend: true
          // name: this.seriesName
        }
      ],
      layout: {
        // xaxis: { range: null },
        // yaxis: { range: null },
        width: this.graphWidth,
        height: this.graphHeight,
        margin: {
          l: 40,
          r: 40,
          b: 20,
          t: 20,
          pad: 4
        },
        colorway: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],

        bargap: 0.05,
        bargroupgap: 0.2
        // barmode: "overlay"
        // title: "Sampled Results",
        // xaxis: {title: "Value"},
        // yaxis: {title: "Count"}
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
  props: ["seriesName", "graphWidth", "graphHeight", "distribution", "interval"],
  methods: {
    createPlot() {
      this.trace[0].y = this.distribution;
      // this.trace[0].x0 = this.interval.min;
      // this.layout.xaxis.range = [this.interval.min, this.interval.max];
      // this.layout.yaxis.range = [Math.min(this.distribution), Math.max(this.distribution)];

      // this.trace[0].ybins.start = this.interval.min;
      // this.trace[0].ybins.end = this.interval.max;
      let TESTER;
      TESTER = this.$refs[this.seriesName + "Hist"];
      Plotly.newPlot(TESTER, this.trace, this.layout, this.config);
    }
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      featureGraphData: state => state.apexchartGraph.featureGraphData
    }),
    refName() {
      return this.seriesName + "Hist";
    }
  },
  components: {},
  mounted() {
    this.createPlot();
  }
};
</script>
