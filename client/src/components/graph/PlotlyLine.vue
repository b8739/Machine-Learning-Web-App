<template>
  <div>
    <!-- {{ selectedData }} -->
    <!-- <v-btn @click="check"></v-btn> -->
    <div v-if="featureGraphData != undefined" :ref="refName"></div>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

// import { Plotly } from "vue-plotly";

export default {
  watch: {
    seriesName: function(newValue, oldValue) {
      this.createEditPlot();
    },
    featureGraphData: function(val, oldValue) {
      if (val != null) {
        this.createPlot(this.featureGraphData[this.seriesName], false);
      }
    }
  },
  data() {
    return {
      selectedData: [],
      data: [
        {
          y: [],
          type: "scatter",
          mode: "lines+markers",
          marker: {
            size: 1
            // marker is an object, valid marker keys: #scatter-marker
          },
          line: {
            // color: "rgb(219, 64, 82)",
            width: 0.6
          },
          opacity: 0.9
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
        // xaxis: {
        //   type: "date"
        // },
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

        modeBarButtonsToRemove: ["sendDataToCloud"],
        modeBarButtonsToAdd: [
          {
            name: "Delete Selected Data",
            icon: {
              path:
                "M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
            },
            click: () => {
              if (this.selectedData.length != 0) {
                this.selectedData.forEach(element => {
                  Vue.set(this.data[0].y, element, null);
                });

                this.data[0].y = [this.data[0].y]; //array로 wrap
                let TESTER = this.$refs[this.refName];
                // Plotly.react(TESTER, this.data, this.config);
                Plotly.restyle(TESTER, this.data[0]);
              }
              eventBus.$emit("deleteData", this.selectedData);
            }
          }
        ]
      }
    };
  },
  props: ["seriesName", "graphWidth", "graphHeight", "isEdit"],
  methods: {
    ...mapMutations("dataTableHandler", ["setCheckedRows"]),
    ...mapMutations("dataTableHandler", ["pushCheckedRows"]),
    ...mapMutations("preprocessHandler", ["setEditMode"]),
    check() {
      console.log(this.$refs);
    },
    createPlot(data, isEdit) {
      this.data[0].y.splice(0, this.data[0].y.length);
      this.data[0].y = data;
      let TESTER = this.$refs[this.refName];

      Plotly.newPlot(TESTER, this.data, this.layout, this.config);
    },
    createEditPlot() {
      let vm = this;
      let path = "http://localhost:5000/loadEditGraphData";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          featureName: this.seriesName,
          tableName: this.tableName
        }
      })
        .then(res => {
          this.createPlot(res.data[this.seriesName], true);
          this.$refs[this.refName].on("plotly_selected", function(eventData) {
            vm.setEditMode(true);
            vm.selectedData = [];

            eventData.points.forEach(element => {
              vm.selectedData.push(element.pointIndex);
            });
            vm.setCheckedRows([]);
            vm.selectedData.forEach(element => {
              vm.pushCheckedRows(element);
            });
          });
        })
        .catch(error => {
          console.error(error);
        });
    },
    openEditModal(column) {
      eventBus.$emit("openEditModal", column);
    }
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      featureGraphData: state => state.apexchartGraph.featureGraphData
    }),
    refName() {
      if (this.isEdit == false) {
        return this.seriesName;
      } else return this.seriesName + "_edit";
    }
  },
  components: {},
  created() {
    if (this.isEdit == false) {
      eventBus.$on("deleteData", selectedData => {
        selectedData.forEach(element => {
          Vue.set(this.data[0].y, element, null);
        });

        this.data[0].y = [this.data[0].y]; //array로 wrap
        let TESTER = this.$refs[this.refName];

        Plotly.restyle(TESTER, this.data[0]);
      });
    }
  },
  mounted() {
    if (this.isEdit == false) {
      (this.config["modeBarButtonsToAdd"] = [
        {
          name: "Edit in Graph Studio",
          icon: Plotly.Icons.pencil,
          click: () => {
            this.openEditModal(this.seriesName);
          }
        }
      ]),
        (this.config["modeBarButtonsToRemove"] = [
          "pan2d",
          "select2d",
          "lasso2d",
          "zoomIn2d",
          "zoom2d",
          "autoScale2d",
          "resetScale2d",
          "zoomOut2d",
          "Delete Selected Data"
        ]);
    } else {
      this.config["displayModeBar"] = true;
      this.createEditPlot();
    }
  }
};
</script>
