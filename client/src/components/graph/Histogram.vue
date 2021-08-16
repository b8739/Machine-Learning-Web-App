<template>
  <div>
    <apexchart
      ref="realtimeChart"
      width="250px"
      height="150px"
      type="bar"
      :options="options"
      :series="series"
    >
    </apexchart>
  </div>
</template>

<script>
export default {
  name: "Histogram",
  props: ["interval", "distribution"],
  data() {
    return {
      intervalArray: [],
      options: {
        chart: {
          height: 350,
          type: "bar",
          toolbar: {
            show: false
          },
          animations: {
            enabled: false
          }
        },
        tooltip: {
          enabled: false
          // intersect: true
        },
        dataLabels: {
          enabled: false
        },
        series: [],
        title: {},
        noData: {
          text: "Loading..."
        },
        xaxis: {
          floating: false
        }
      },
      series: []
    };
  },
  watch: {},
  created() {},
  mounted() {
    this.convertToArray(this.interval, this.intervalArray);
    this.intervalArray.sort(); //max보다 min이 앞에 있는 문제 해결
    this.updateCategories(this.intervalArray);
    this.updateSeriesLine(this.distribution);
  },
  methods: {
    convertToArray(jsonObject, targetArray) {
      for (var key in jsonObject) {
        targetArray.push(jsonObject[key]);
        targetArray.reverse();
      }
    },
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
    updateOptions() {
      this.$refs.realtimeChart.updateOptions({
        chart: {
          width: "500px"
        }
      });
    }
  }
};
</script>
