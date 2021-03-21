<template>
  <div id="chart">
    <apexchart
      ref="realtimeChart"
      type="area"
      :width="graphWidth"
      :height="graphHeight"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
//vuex
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
export default {
  name: "TimeSeries",
  props: ["graphWidth", "graphHeight", "date", "editModal_hidden", "nameChangeMark", "rawDataset"],
  data() {
    return {
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      firstMount: true,
      datasetByName: [],
      dateByName: [],
      options: {
        chart: {
          type: "area",
          toolbar: {
            show: true
          },
          //zoom
          zoom: {
            enabled: true,
            autoScaleXaxis: false,
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
          toolbar: {
            autoSelected: "selection"
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
        this.randomIndexArray = this.getRandomArray(0, this.indexNum);
        this.putIntoArray(this.rawDataset, this.dataArray, this.randomIndexArray);
        this.updateSeriesLine(this.dataArray);
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
  // conss
  mounted() {
    if (this.firstMount == false) {
      this.randomIndexArray = this.getRandomArray(0, this.indexNum);
      this.putIntoArray(this.rawDataset, this.dataArray, this.randomIndexArray);
      this.updateSeriesLine(this.dataArray);
      this.putIntoArray(this.date, this.dateArray, this.randomIndexArray);
      this.updateCategories(this.dateArray);
    }
  },
  computed: {
    ...mapState({ indexNum: state => state.indexNum })
  },
  methods: {
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = randomIndex[0]; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[i]);
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
    //preprocess methods
    randomizeDataset(dataset_unrandomized, dataset_randomized, randomIndex) {
      let tempArray = [];
      for (let i = 0; i < randomIndex.length; i++) {
        tempArray.push(dataset_unrandomized[randomIndex[i]]); //이게 정말 randomize되는것
        // targetArray.push(dataset_unrandomized[i]);
      }
      dataset_randomized.push(tempArray);
    },
    randomizeDate(dataset_unrandomized, dataset_randomized, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        dataset_randomized.push(dataset_unrandomized[randomIndex[i]]); //이게 정말 randomize되는것
        // targetArray.push(dataset_unrandomized[i]);
      }
    },
    //date methods
    formatDate(dateArray) {
      for (let i = 0; i < dateArray.length; i++) {
        dateArray[i] = new Date(dateArray[i]).getTime();
      }
    },
    //randomize methods
    getCount(datasetLength) {
      return Math.round(datasetLength * 0.1);
    },
    getRandom(min, max) {
      return Math.floor(Math.random() * (max - min + 1) + min);
    },

    getRandomArray(min, max) {
      let count = this.getCount(max);
      // console.log(max * 5);
      // const count = 150 * 0.5;
      if (max - min + 1 < count) return;

      // 배열 생성
      let randomArray = [];

      while (1) {
        let index = this.getRandom(min, max);

        // 중복 여부 체크
        if (randomArray.indexOf(index) > -1) {
          continue;
        }

        randomArray.push(index);
        // 원하는 배열 갯수 만족 시 종료
        if (randomArray.length == count) {
          break;
        }
      }

      // 정렬
      let sortedRandomArray = randomArray.sort(function(a, b) {
        return a - b;
      });

      return sortedRandomArray;
    },
    //APEX CHART
    updateSeriesLine(dataSet) {
      this.$refs.realtimeChart.updateSeries(
        [
          {
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
