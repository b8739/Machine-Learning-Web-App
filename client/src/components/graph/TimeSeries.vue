<template>
  <div id="chart">
    <!-- <v-btn @click="rerender()">rerender</v-btn> -->
    <apexchart
      ref="realtimeChart"
      type="line"
      :width="graphWidth"
      :height="graphHeight"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import Vue from "vue";
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";

//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  name: "TimeSeries",
  props: ["graphWidth", "graphHeight", "seriesName"],

  data() {
    return {
      newDataset: [],
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      firstMount: true,

      dateByName: [],
      options: {
        // chart
        chart: {
          type: "line",
          toolbar: {
            show: true,
            autoSelected: "selection",

            tools: {
              download: false,
              customIcons: [
                {
                  icon: '<p  width="20"> G<p>',
                  index: 6,
                  title: "tooltip of the icon",
                  class: "custom-icon",
                  click: function(chart, options, e) {
                    console.log(options);
                  }
                }
              ]
            }
          },
          //zoom
          zoom: {
            type: "xy",
            enabled: true,
            autoScaleYaxis: true,
            zoomedArea: {
              fill: {
                color: "#90CAF9",
                opacity: 0.4
              },
              stroke: {
                color: "#0D47A1",
                opacity: 0.4,
                width: 1
              }
            }
          },
          //selection
          selection: {
            enabled: true,
            type: "xy",
            fill: {
              color: "black",
              opacity: 0.1
            },
            stroke: {
              width: 5,
              dashArray: 3,
              color: "black",
              opacity: 0.4
            }
          },

          events: {
            // zoom events
            // beforeZoom: (chartContext, { xaxis }) => {
            //   this.updateSelection();
            //   this.xaxisWhenZoomed = xaxis;
            //   this.$emit("xaxis", this.xaxisWhenZoomed);
            //   this.toggleDataPointSelection(xaxis);
            //   return {
            //     xaxis: {
            //       min: 0
            //     }
            //   };
            // },
            legendClick: function(chartContext, seriesIndex, config) {
              // console.log(seriesIndex);
              // ...
            },
            // selection events
            selection: (chartContext, { xaxis, yaxis }) => {
              let yaxisObject = { min: null, max: null };
              console.log(xaxis);
              // yaxisObject.min = yaxis[0]["min"];
              // yaxisObject.max = yaxis[0]["max"];
              // this.yaxisWhenSelected = yaxisObject;
              this.xaxisWhenSelected = xaxis;
              this.$emit("xaxis", this.xaxisWhenSelected);
            }
          }
        },
        states: {
          active: {
            allowMultipleDataPointsSelection: true,
            filter: {
              type: "darken",
              value: 0.35
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        series: [],
        title: {},
        markers: {
          size: 1,
          strokeWidth: 0.1,
          strokeColor: "skyblue",
          hover: {
            size: 2,
            strokeColor: "#fff"
          }
        },
        noData: {
          text: "Loading..."
        },
        xaxis: {
          // type: "datetime",
          tickAmount: 5,
          labels: {
            minHeight: 50,
            rotate: -30,
            rotateAlways: true,
            hideOverlappingLabels: false,

            style: {
              fontSize: "10px",
              fontWeight: 200
            }
          }
        },
        legend: {
          show: true,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        }
      },
      series: []
    };
  },
  watch: {
    // seriesName: function(data) {
    //   console.log("seriesname change");
    //   this.$refs.realtimeChart.updateSeries({
    //     name: seriesName
    //   });
    // },
    editModal_hidden: function(data) {
      console.log(data);
      if (data == true) {
        this.resetSeries();
      }
    },
    // newDataset: function(data) {
    //          this.resetSeries();
    //   if (data != null) {

    //     this.randomIndexArray = randomizer.getRandomArray(0, this.dataset.length);
    //     randomizer.randomizeDataset(this.newDataset, this.dataArray, this.randomIndexArray);
    //     this.updateSeriesLine(this.dataArray, this.seriesName);
    //   }
    // },

    // date: function(data) {
    //   if (data != null) {
    //     this.convertToArray(this.date, this.dateArray, this.randomIndexArray);
    //     this.updateCategories(this.dateArray);
    //   }
    // },
    immediate: true
  },

  created() {
    this.dataset.forEach(element => {
      this.newDataset.push(element[this.seriesName]);
    });
  },
  mounted() {
    this.resetSeries();
    if (this.apexChartDataset[this.seriesName] != null) {
      this.updateSeriesLine(this.apexChartDataset[this.seriesName], this.seriesName);
    } else {
      if (this.newDataset != null) {
        this.randomIndexArray = randomizer.getRandomArray(0, this.dataset.length - 1);
        randomizer.randomizeDataset(this.newDataset, this.dataArray, this.randomIndexArray);
        this.updateSeriesLine(this.dataArray, this.seriesName);
        let payload = { featureName: this.seriesName, dataset: this.dataArray };
        // vuex에 저장
        this.setApexChartDataset(payload);
      }
    }
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      apexChartDataset: state => state.apexchartGraph.apexChartDataset
    }),
    ...mapGetters("initialData", ["indexNum"])
  },
  methods: {
    ...mapMutations("apexchartGraph", ["setApexChartDataset"]),
    rerender() {
      this.updateSeriesLine(this.dataArray, this.seriesName);
    },
    convertToArray(jsonObject, targetArray, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[randomIndex[i]]);
      }
    },
    //date methods
    formatDate(dateArray) {
      for (let i = 0; i < dateArray.length; i++) {
        dateArray[i] = new Date(dateArray[i]).getTime();
      }
    },
    //APEX CHART
    updateSeriesLine(dataSet, seriesName) {
      this.$refs.realtimeChart.updateSeries(
        [
          {
            name: seriesName,
            data: dataSet
          }
        ],
        false,
        true
      );
    },
    updateCategories(newCategories) {
      this.$refs.realtimeChart.updateOptions({
        xaxis: {
          categories: newCategories
        }
      });
    },
    updateSelection() {
      this.$refs.realtimeChart.updateOptions({
        chart: {
          selection: {
            xaxis: {
              min: undefined,
              max: undefined
            }
          }
        }
      });
    },
    toggleDataPointSelection(xaxis) {
      for (let i = xaxis.min; i <= xaxis.max; i++) {
        this.$refs.realtimeChart.toggleDataPointSelection(0, i);
      }
    },
    resetSeries() {
      this.dataArray = [];
      this.dateArray = [];
    }
  }
};
</script>
