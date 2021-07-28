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
import { eventBus } from "@/main";

export default {
  name: "TimeSeries",
  props: ["graphWidth", "graphHeight", "seriesName", "dialog"],

  data() {
    return {
      selectionTimer: null,
      xaxisMin: null,
      yaxisMin: null,
      xaxisMax: null,
      yaxisMax: null,
      testArray: [],
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
            show: false,
            autoSelected: "zoom",
            // "<i class='fas fa-trash' style='padding-left:5px; width:20px''></i>"
            tools: {
              download: false,
              customIcons: [
                {
                  icon:
                    "<span class='material-icons' style=font-size:20px;padding-top:3px;padding-left:2px>delete</span>",
                  index: 6,
                  title: "tooltip of the icon",

                  class: "custom-icon",

                  click: (chart, options, e) => {
                    eventBus.$emit("deleteDataFromGraph", this.seriesName);
                    this.createNewDataset();
                    this.renderDataset();
                  }
                }
              ]
            }
          },
          tooltip: {
            intersect: true
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
            // xaxis: {
            //   min: 0,
            //   max: 5
            // },
            // yaxis: {
            //   min: 0,
            //   max: 5
            // }
          },

          events: {
            legendClick: function(chartContext, seriesIndex, config) {
              // console.log(seriesIndex);
              // ...
            },
            // selection events
            selection: (chartContext, { xaxis, yaxis }) => {
              this.dataSelected(xaxis, yaxis);
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
        yaxis: {
          decimalsInFloat: 2
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
    dialog: function(data) {
      if (data) {
        console.log(true);
        this.$refs.realtimeChart.updateOptions({
          chart: {
            toolbar: {
              show: true
            }
          }
        });
      }
    },

    immediate: true
  },

  created() {
    this.createNewDataset();
  },
  mounted() {
    // this.renderDataset();
    // this.resetOriginalState();
    if (this.firstMount) {
      this.renderDataset();

      // console.log("timeseries mounted");
      // s;
      this.firstMount = !this.firstMount;
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
    createNewDataset() {
      this.newDataset = [];
      this.dataset.forEach(element => {
        this.newDataset.push(element[this.seriesName]);
      });
    },
    dataSelected(xaxis, yaxis) {
      this.testArray = [];
      this.xaxisMin = Math.floor(xaxis.min);
      this.xaxisMax = Math.floor(xaxis.max);
      this.yaxisMin = Math.floor(yaxis.min);
      this.yaxisMax = Math.floor(yaxis.max);

      for (let i = this.xaxisMin; i < this.xaxisMax; i++) {
        let index = this.randomIndexArray[i];
        let dataValue = this.newDataset[index];
        if (dataValue >= this.yaxisMin && dataValue <= this.yaxisMax) {
          this.testArray.push(i);
        }
      }
      if (this.selectionTimer == null) {
        this.selectionTimer = setTimeout(() => {
          eventBus.$emit("dataSelected", this.testArray);
        }, 1);
      }
      let timer = setTimeout(() => {
        this.selectionTimer = null;
      }, 2000);
    },
    renderDataset() {
      this.resetSeries();
      if (this.newDataset != null) {
        this.randomIndexArray = randomizer.getRandomArray(0, this.dataset.length - 2);
        randomizer.randomizeDataset(this.newDataset, this.dataArray, this.randomIndexArray);
        this.updateSeriesLine(this.dataArray, this.seriesName);
        let payload = { featureName: this.seriesName, dataset: this.dataArray };
        // vuex에 저장
        this.setApexChartDataset(payload);
      }
      // dialog(edit modal)일때만 toolbar 활성화
      if (this.dialog) {
        this.$refs.realtimeChart.updateOptions({
          chart: {
            toolbar: {
              show: true
            }
          }
        });
      }
    },
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
    resetOriginalState() {
      this.$refs.realtimeChart.resetSeries();
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
