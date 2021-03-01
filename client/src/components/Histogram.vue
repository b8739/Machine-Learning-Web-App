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
      options: {
        chart: {
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
            beforeZoom: function(chartContext, { xaxis }) {
              return {
                xaxis: {
                  min: 0
                }
              };
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
      console.log("data감지");
      if (data != null) {
        this.putIntoArray(this.dataValue, this.dataArray);
        this.updateSeriesLine();
      }
    },
    date: function(data) {
      if (data != null) {
        this.putIntoArray(this.date, this.dateArray);
        this.updateOptions(this.dateArray);
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
    updateOptions(newCategories) {
      this.$refs.realtimeChart.updateOptions({
        xaxis: {
          categories: newCategories
        }
      });
    }
  }
};
</script>
