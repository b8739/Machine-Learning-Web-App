<template>
  <div ref="edaGraph"></div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      data: [
        {
          x: [],
          y: [],
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
      featureGraphData: state => state.apexchartGraph.featureGraphData
    })
  },
  methods: {
    createPlot(data) {
      this.data[0].y.splice(0, this.data[0].y.length);
      this.data[0].y = data;
      let TESTER = this.$refs["edaGraph"];
      Plotly.newPlot(TESTER, this.data, this.layout, this.config);
    },
    updatePlot(data, attrName) {
      this.data[0].y.splice(0, this.data[0].y.length);
      this.data[0].y = [data];
      let TESTER = this.$refs["edaGraph"];
      Plotly.restyle(TESTER, this.data[0]);
    }
  },
  created() {
    eventBus.$on("xaxisBeingDragged", newXaxisInfo => {
      console.log(newXaxisInfo); //evt.added.element
      let featureName = newXaxisInfo.evt.added.element;
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
          this.updatePlot(res.data[featureName]);
        })
        .catch(error => {
          console.error(error);
        });
    });
    eventBus.$on("xaxisBeingRemoved", status => {
      console.log(status);
    });
    eventBus.$on("yaxisBeingDragged", newYaxisInfo => {
      console.log(newYaxisInfo);
    });
    eventBus.$on("yaxisBeingRemoved", removedYaxisName => {
      console.log(removedYaxisName);
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

    this.createPlot([], false);
  }
};
</script>
