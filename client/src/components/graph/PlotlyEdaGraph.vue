<template>
  <div ref="edaGraph"></div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
let cloneDeep = require("lodash/cloneDeep");
export default {
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
          text: "EDA Graph"
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
    createPlot() {
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
    updatePlot(featureName, data, axisType, tpIndex) {
      // 입력하는 축의 데이터 (ex. x)
      this.data[tpIndex][axisType] = [data];
      // 반대 축 데이터도 다시 입력해주어야 초기화가 안됨 (ex. y)
      let oppositeAxis = this.getOppositeAxis(axisType);
      if (this.data[tpIndex][oppositeAxis] != undefined) {
        this.data[tpIndex][oppositeAxis] = [this.data[tpIndex][oppositeAxis]];
      }
      this.data[tpIndex]["name"] = `Data ${tpIndex + 1}`;
      let fullAxis = this.getAxisName(axisType) + this.getAxisNumber(tpIndex);
      this.layout[fullAxis] = this.getFontFormat(featureName, axisType, tpIndex);
      Plotly.update(this.plotContainer, this.data[tpIndex], this.layout, tpIndex);

      // Plotly.restyle(this.plotContainer, this.data[tpIndex], tpIndex);
    },
    loadFullData(featureName, axisType, tpIndex) {
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadEditGraphData";
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
          this.updatePlot(featureName, res.data[featureName], axisType, tpIndex);
        })
        .catch(error => {
          console.error(error);
        });
    },
    getOppositeAxis(axisName) {
      if (axisName == "x") return "y";
      else return "x";
    },
    getAxisName(axisType) {
      if (axisType == "x") {
        return "xaxis";
      } else {
        return "yaxis";
      }
    },
    getAxisNumber(tpIndex) {
      if (tpIndex == 0) {
        return "";
      } else return tpIndex;
    },
    getFontFormat(featureName, axisType, tpIndex) {
      let axisInfo = {
        title: {
          automargin: true,
          text: featureName,
          font: {
            size: 14,
            color: "#7f7f7f"
          }
        }
      };
      return axisInfo;
    },
    changeAxis(selectedAxis, axisType, tpIndex, featureName) {
      console.log(featureName);
      let axis = this.getAxisName(axisType);
      this.data[tpIndex][axis] = selectedAxis;
      this.data[tpIndex]["x"] = [this.data[tpIndex]["x"]];
      this.data[tpIndex]["y"] = [this.data[tpIndex]["y"]];

      let axisNum = axis + (parseInt(tpIndex) + 1);
      this.layout[axisNum] = {};
      this.layout[axisNum]["overlaying"] = axisType;
      this.layout[axisNum]["automargin"] = true;
      this.layout[axisNum]["title"] = {};
      this.layout[axisNum]["title"]["text"] = featureName;
      this.layout[axisNum]["title"]["font"] = {
        size: 14,
        color: "#7f7f7f"
      };

      Plotly.update(this.plotContainer, this.data[tpIndex], this.layout, tpIndex);
    },
    changeGridInfo(rows, columns) {
      // grid: { rows: 2, columns: 2, pattern: "independent" },

      this.layout["grid"] = {};
      this.layout["grid"]["rows"] = rows;
      this.layout["grid"]["columns"] = columns;
      this.layout["grid"]["pattern"] = "independent";
      Plotly.relayout(this.plotContainer, this.layout);
    },
    changeOverlay(value, tpIndex) {
      let xaxis = "xaxis" + (parseInt(tpIndex) + 1);
      let yaxis = "yaxis" + (parseInt(tpIndex) + 1);
      // this.layout[xaxis] = {};
      // this.layout[yaxis] = {};
      if (value) {
        this.layout[xaxis]["overlaying"] = "x";
        this.layout[yaxis]["overlaying"] = "y";
      } else {
        Vue.delete(this.layout[xaxis], "overlaying");
        Vue.delete(this.layout[yaxis], "overlaying");
      }
      Plotly.relayout(this.plotContainer, this.layout);
    },
    removeAxis(axisType, tpIndex) {
      Vue.delete(this.data[tpIndex], axisType);
      let oppositeAxis = this.getOppositeAxis(axisType);
      if (this.data[tpIndex][oppositeAxis] != undefined) {
        this.data[tpIndex][oppositeAxis] = [this.data[tpIndex][oppositeAxis]];
      }
      Plotly.restyle(this.plotContainer, this.data[tpIndex], tpIndex);
    }
  },
  created() {
    eventBus.$on("loadAxis", payload => {
      this.loadFullData(payload.featureName, payload.axisType, payload.tpIndex);
    });
    eventBus.$on("changeAxis", payload => {
      this.changeAxis(payload.selectedAxis, payload.axisType, payload.tpIndex, payload.featureName);
    });
    eventBus.$on("changeGridInfo", grid => {
      this.changeGridInfo(grid.rows, grid.columns);
    });
    eventBus.$on("changeOverlay", payload => {
      this.changeOverlay(payload.value, payload.tpIndex);
    });
    eventBus.$on("removeAxis", payload => {
      this.removeAxis(payload.axisType, payload.tpIndex);
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
<style scoped></style>
