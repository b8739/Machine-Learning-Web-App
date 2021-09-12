<template>
  <div ref="edaGraph"></div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
let cloneDeep = require("lodash/cloneDeep");
export default {
  watch: {},
  data() {
    return {
      dataFormat: {
        type: "scatter",
        mode: "lines+markers",
        marker: {
          size: 2
        },
        line: {
          width: 1
        }
      },
      data: [
        {
          type: "scatter",
          mode: "lines+markers",
          marker: {
            size: 2
            // marker is an object, valid marker keys: #scatter-marker
          },
          line: {
            // color: "rgb(219, 64, 82)",
            width: 1
          }
          // xaxis: "x2",
          // yaxis: "y2"
          // showlegend: true
          // name: this.seriesName
        }
      ],
      layout: {
        width: this.graphWidth,
        height: this.graphHeight,
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
        showSendToCloud: false,
        displaylogo: false,
        responsive: true,
        showEditInChartStudio: false,

        modeBarButtonsToRemove: ["sendDataToCloud"]
      }
    };
  },
  props: ["seriesName", "graphWidth", "graphHeight", "isEdit"],
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      featureGraphData: state => state.apexchartGraph.featureGraphData,
      xaxisColumns: state => state.edaHandler.xaxisColumns,
      xaxisEvent: state => state.edaHandler.xaxisEvent,
      yaxisColumns: state => state.edaHandler.yaxisColumns,
      yaxisEvent: state => state.edaHandler.yaxisEvent
    }),
    plotContainer() {
      return this.$refs["edaGraph"];
    }
  },
  methods: {
    createTrace(featureName) {
      let trace = {
        type: "scatter",
        mode: "lines+markers",
        marker: {
          size: 2
        },
        line: {
          width: 1
        }
      };
      // axios
      let path = "http://localhost:5000/loadEditGraphData";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          featureName: featureName,
          tableName: this.tableName
        }
      })
        .then(res => {
          trace["x"] = res.data[featureName];
          this.data.push(trace);
          let layout_update = {
            grid: { rows: 1, columns: 2, pattern: "independent" }
          };
          Plotly.newPlot(this.plotContainer, this.data, this.layout, this.config);
          Plotly.relayout(this.plotContainer, layout_update);
        })
        .catch(error => {
          console.error(error);
        });
      return;
    },

    getOppositeAxis(axisName) {
      if (axisName == "x") return "y";
      else return "x";
    },
    createPlot() {
      //   this.data[0].x.splice(0, this.data[0].x.length);
      //   this.data[0].x = data;

      Plotly.newPlot(this.plotContainer, this.data, this.layout, this.config);
    },
    addNewTrace() {
      let newTrace = cloneDeep(this.dataFormat);
      newTrace["x"] = [[]];
      newTrace["y"] = [[]];
      Plotly.addTraces(this.plotContainer, newTrace);
    },
    deleteTrace(tpIndex) {
      Plotly.deleteTraces(this.plotContainer, tpIndex);
    },
    updatePlot(data, axisType, tpIndex) {
      // let newTrace = {};
      // newTrace[axisType] = [[data]];
      this.data[tpIndex][axisType] = [data];
      // let oppositeAxis = this.getOppositeAxis(axisType);
      // if (this.data[tpIndex][oppositeAxis] != undefined) {
      //   this.data[tpIndex][oppositeAxis] = [this.data[tpIndex][oppositeAxis]];
      // }
      Plotly.restyle(this.plotContainer, this.data[tpIndex], tpIndex);
    },
    loadFullData(featureName, axisType, tpIndex) {
      let path = "http://localhost:5000/loadEditGraphData";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          featureName: featureName,
          tableName: this.tableName
        }
      })
        .then(res => {
          console.log(res.data[featureName]);
          this.updatePlot(res.data[featureName], axisType, tpIndex);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    eventBus.$on("loadAxis", payload => {
      this.loadFullData(payload.featureName, payload.axisType, payload.tpIndex);
    });
    eventBus.$on("addEmptyTrace", status => {
      this.addNewTrace();
    });
    eventBus.$on("deleteTrace", tpIndex => {
      this.deleteTrace(tpIndex);
    });
  },
  mounted() {
    console.log("plotly eda mounted");

    (this.config["modeBarButtonsToAdd"] = [
      {
        name: "Edit in Graph Studio",
        icon: Plotly.Icons.pencil,
        click: () => {
          this.openEditModal(this.seriesName);
        }
      }
    ]),
      (this.config["modeBarButtonsToRemove"] = ["Delete Selected Data"]);

    this.createPlot();
  }
};
</script>
