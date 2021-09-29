<template>
  <!-- <div style="width:700px">layout:{{ layout }}</div> -->
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
          this.updatePlot(featureName, res.data[featureName], axisType, tpIndex);
        })
        .catch(error => {
          console.error(error);
        });
    },
    renderGroupingGraph(groupingData) {
      Object.keys(groupingData).forEach((element, index) => {
        console.log(index);
        // Data 1이 있는 상태에서 시작하므로, 1은 존재하는 것 재활용하고 없을 때 새로 만듦
        if (this.data[index] == undefined) {
          this.addNewTrace();
        }
        // Data Setting
        this.data[index]["x"] = groupingData[element][0];
        this.data[index]["y"] = groupingData[element][1];
        this.data[index]["name"] = element;
        // Layout Setting (Axis 분리)
        if (index != 0) {
          ["x", "y"].forEach(element => {
            //layout
            let axisNum = element + "axis" + parseInt(index + 1);
            this.layout[axisNum] = {};
            // this.layout[axisNum]["overlaying"] = axisType;
            this.layout[axisNum]["automargin"] = true;
            this.layout[axisNum]["title"] = {};
            Vue.set(this.data[index], element + "axis", element + parseInt(index + 1));
          });
        }
      });
      // let fullAxis = this.getAxisName(axisType) + this.getAxisNumber(tpIndex);
      // this.layout[fullAxis] = this.getFontFormat(featureName, axisType, tpIndex);
      Plotly.update(this.plotContainer, this.data, this.layout);
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
        automargin: true,
        title: {
          //
          text: featureName,
          // standoff: 20,
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
      this.layout[axisNum] = this.getFontFormat(featureName, axisType, tpIndex);
      // changeoverlay
      this.layout[axisNum]["overlaying"] = axisType;
      // this.changeOverlay("Data 1", tpIndex);

      // this.layout[axisNum] = {};
      // this.layout[axisNum]["overlaying"] = axisType;
      // this.layout[axisNum]["automargin"] = true;
      // this.layout[axisNum]["title"] = {};
      // this.layout[axisNum]["title"]["text"] = featureName;
      // this.layout[axisNum]["title"]["font"] = {
      //   size: 14,
      //   color: "#7f7f7f"
      // };

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
      console.log(value);
      let xaxis = "xaxis" + (parseInt(tpIndex) + 1);
      let yaxis = "yaxis" + (parseInt(tpIndex) + 1);
      // undefined일 때만 initialize (안그러면 getfontformat에서 세팅한 layout를 초기화해버리게됨)
      if (this.layout[xaxis] == undefined && this.layout[yaxis] == undefined) {
        this.layout[xaxis] = {};
        this.layout[yaxis] = {};
      }

      if (value == "Data 1") {
        this.layout[xaxis]["overlaying"] = "x";
        this.layout[yaxis]["overlaying"] = "y";
      } else if (value == "None") {
        Vue.delete(this.layout[xaxis], "overlaying");
        Vue.delete(this.layout[yaxis], "overlaying");
      } else {
        let axisIndex = value.substring(5);
        this.layout[xaxis]["overlaying"] = "x" + axisIndex;
        this.layout[yaxis]["overlaying"] = "y" + axisIndex;
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
    eventBus.$on("applyGroupBy", payload => {
      let groupLength = Object.keys(payload.data).length;
      if (payload.groupby == "x") {
        this.changeGridInfo(1, groupLength);
      } else {
        this.changeGridInfo(groupLength, 1);
      }
      this.renderGroupingGraph(payload.data);
      console.log(payload.data);
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
