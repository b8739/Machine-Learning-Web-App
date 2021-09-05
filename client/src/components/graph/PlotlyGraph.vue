<template>
  <div v-if="featureGraphData != undefined" :ref="seriesName"></div>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

// import { Plotly } from "vue-plotly";

export default {
  data() {
    return {
      trace: [
        {
          y: [],
          type: "scatter",
          mode: "lines",
          marker: {
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
        width: 238,
        height: 200,
        margin: {
          l: 20,
          r: 20,
          b: 20,
          t: 20,
          pad: 4
        },
        colorway: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],

        yaxis: {
          automargin: true
        }
        // title: {
        //   text: this.seriesName
        // }
      },
      config: {
        showSendToCloud: true,
        displaylogo: false,
        responsive: true,
        showEditInChartStudio: false,
        modeBarButtonsToAdd: [
          {
            name: "color toggler",

            click: function(gd) {
              console.log("hi");
            }
          }
        ],
        modeBarButtonsToRemove: ["sendDataToCloud"]
      }
    };
  },
  props: ["seriesName"],
  methods: {
    createPlot() {
      this.trace[0].y = this.featureGraphData[this.seriesName];
      let TESTER = this.$refs[this.seriesName];
      Plotly.newPlot(TESTER, this.trace, this.layout, this.config);
    }
  },
  computed: {
    ...mapState({
      featureGraphData: state => state.apexchartGraph.featureGraphData
    }),
    dataset() {
      if (this.featureGraphData != undefined) return this.featureGraphData[this.seriesName];
      else return [];
    }
  },
  components: {},
  mounted() {
    this.createPlot();
  }
};
</script>
