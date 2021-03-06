<template>
  <div id="chart">
    <apexchart
      ref="realtimeChart"
      type="area"
      width="250px"
      height="180px"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
export default {
  name: "TimeSeries",
  props: ["indexNum", "dataValue", "date"],
  data() {
    return {
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxis: {},
      options: {
        chart: {
          toolbar: {
            show: false
          },
          type: "area",
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
          events: {
            zoomed: function(chartContext, { xaxis, yaxis }) {
              // console.log(xaxis);
              // console.log(yaxis);
            },
            beforeZoom: (chartContext, { xaxis }) => {
              this.updateSelection();
              this.xaxis = xaxis;
              this.$emit("xaxis", this.xaxis);
              this.toggleDataPointSelection(xaxis);
              return {
                xaxis: {
                  min: 0
                }
              };
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
            size: 1,
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
    // indexNum: function(data) {
    //   if (data != null) {
    //     // console.log(this.indexNum);

    //   }
    // },
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
    }
  },

  created() {},
  mounted() {
    // this.putIntoArray(this.dataValue);
    // this.updateSeriesLine();
  },

  methods: {
    //PREPROCESS
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = randomIndex[0]; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[i]);
      }
    },
    getCount(datasetLength) {
      return Math.round(datasetLength * 0.4);
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
    updateSeriesLine(dataValue) {
      this.$refs.realtimeChart.updateSeries(
        [
          {
            data: dataValue
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
    }
  }
};
</script>
