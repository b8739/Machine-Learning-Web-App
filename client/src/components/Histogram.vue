<template>
  <div id="chart">
    <apexchart
      ref="realtimeChart"
      type="area"
      width="500"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
export default {
  name: "Histogram",
  props: ["dataValue", "indexNum", "date"],
  data() {
    return {
      dataArray: [],
      dateArray: [],
      xaxis: {},
      options: {
        chart: {
          selection: {
            xaxis: {
              min: undefined,
              max: undefined
            },
            enabled: true
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
        title: {
          text: "Distribution"
        },
        markers: {
          size: 4,
          // colors: "blue",
          strokeWidth: 0.1,
          strokeColor: "skyblue",
          hover: {
            size: 6,
            strokeColor: "#fff"
          }
        },
        noData: {
          text: "Loading..."
        },
        xaxis: {
          type: "datatime"
        }
      },
      series: []
    };
  },
  watch: {
    dataValue: function(data) {
      if (data != null) {
        this.putIntoArray(this.dataValue, this.dataArray);
        this.updateSeriesLine();
      }
    },
    date: function(data) {
      if (data != null) {
        this.putIntoArray(this.date, this.dateArray);
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
    putIntoArray(jsonObject, targetArray) {
      for (let i = 0; i <= this.indexNum; i++) {
        targetArray.push(jsonObject[i]);
      }
    },
    updateSeriesLine() {
      this.$refs.realtimeChart.updateSeries(
        [
          {
            data: this.dataArray
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
