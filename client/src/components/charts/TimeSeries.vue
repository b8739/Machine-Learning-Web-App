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
export default {
  name: "TimeSeries",
  props: ["graphWidth", "graphHeight", "indexNum", "dataValue", "date", "editModal_hidden"],
  data() {
    return {
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      yaxisWhenSelected: {},
      firstMount: true,
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
            beforeZoom: (chartContext, { xaxis }) => {
              this.updateSelection();
              console.log(xaxis);
              this.xaxisWhenZoomed = xaxis;
              this.$emit("xaxis", this.xaxisWhenZoomed);
              this.toggleDataPointSelection(xaxis);
              return {
                xaxis: {
                  min: 0
                }
              };
            },
            // selection events
            selection: (chartContext, { xaxis, yaxis }) => {
              this.yaxisWhenSelected = yaxis;
              // console.log(this.yaxisWhenSelected);
              this.$emit("yaxis", this.yaxisWhenSelected);
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
          type: "datatime"
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
      if (data == true) {
        this.resetSeries();
      }
    },
    dataValue: function(data) {
      if (data != null) {
        this.randomIndexArray = this.getRandomArray(0, this.indexNum);
        this.putIntoArray(this.dataValue, this.dataArray, this.randomIndexArray);
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
    // console.log("create");
    if (this.dataValue != null || this.dataValue != undefined) {
      let objectLength = Object.keys(this.dataValue).length;
      if (objectLength != 0) {
        this.firstMount = false;
      }
    }
  },
  mounted() {
    // console.log("mount");
    if (this.firstMount == false) {
      this.randomIndexArray = this.getRandomArray(0, this.indexNum);
      this.putIntoArray(this.dataValue, this.dataArray, this.randomIndexArray);
      this.updateSeriesLine(this.dataArray);
      this.putIntoArray(this.date, this.dateArray, this.randomIndexArray);
      this.updateCategories(this.dateArray);
    }
  },

  methods: {
    //PREPROCESS
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = randomIndex[0]; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[i]);
      }
    },
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
    updateSeriesLine(dataArray) {
      this.$refs.realtimeChart.updateSeries(
        [
          {
            data: dataArray
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
      console.log("reset");
    }
  }
};
</script>
