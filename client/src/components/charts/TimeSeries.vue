<template>
  <div id="chart">
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
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";

//vuex
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
export default {
  name: "TimeSeries",
  props: ["graphWidth", "graphHeight", "date", "editModal_hidden", "rawDataset", "seriesName"],
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음
  data() {
    return {
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      firstMount: true,
      // datasetByName: [], legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음
      dateByName: [],
      options: {
        // chart
        chart: {
          type: "area",
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
          type: "datetime",
          labels: {
            minHeight: 50,
            rotate: -30,
            rotateAlways: true,
            hideOverlappingLabels: false,
            format: "yy/MM/dd",
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
    editModal_hidden: function(data) {
      console.log(data);
      if (data == true) {
        this.resetSeries();
      }
    },
    rawDataset: function(data) {
      if (data != null) {
        this.randomIndexArray = randomizer.getRandomArray(0, this.indexNum);
        this.putIntoArray(this.rawDataset, this.dataArray, this.randomIndexArray);
        this.updateSeriesLine(this.dataArray, this.seriesName);
      }
    },
    date: function(data) {
      if (data != null) {
        this.putIntoArray(this.date, this.dateArray, this.randomIndexArray);
        this.updateCategories(this.dateArray);
      }
    },
    immediate: true
  },

  created() {
    if (this.rawDataset != null || this.rawDataset != undefined) {
      let objectLength = Object.keys(this.rawDataset).length;
      if (objectLength != 0) {
        this.firstMount = false;
      }
    }
  },
  // cons
  mounted() {
    //console.log(this.dataset);
    if (this.firstMount == false) {
      this.randomIndexArray = randomizer.getRandomArray(0, this.indexNum);
      this.putIntoArray(this.rawDataset, this.dataArray, this.randomIndexArray);
      this.updateSeriesLine(this.dataArray, this.seriesName);
      this.putIntoArray(this.date, this.dateArray, this.randomIndexArray);
      this.updateCategories(this.dateArray);
    }
  },
  computed: {
    ...mapState({ dataset: state => state.dataset, indexNum: state => state.indexNum })
  },
  methods: {
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[randomIndex[i]]);
      }
    },
    divideDatasetByName(datasetByName, nameChangeMark) {
      let tempArray = [];
      let startIndex = 0;
      //name별 data분류, index는 가져온 상황
      for (const value in nameChangeMark) {
        for (let i = startIndex; i < nameChangeMark[value]; i++) {
          tempArray.push(this.rawDataset[i]);
        }
        startIndex = nameChangeMark[value];
        datasetByName.push(tempArray);
        tempArray = [];
      }
    },
    divideDateByName(dateByName, nameChangeMark) {
      let tempArray = [];
      let startIndex = 0;
      //name별 data분류, index는 가져온 상황
      for (let i = startIndex; i < nameChangeMark[0]; i++) {
        dateByName.push(this.date[i]);
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
      // console.log("rest");
      this.dataArray = [];
      this.datasetByName = [];
    }
  }
};
</script>
