<template>
  <div>
    <apexchart
      ref="realtimeChart"
      width="250px"
      height="180px"
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
  props: ["indexNum", "interval", "distribution"],
  data() {
    return {
      intervalArray: [],
      options: {
        chart: {
          height: 350,
          type: "bar",
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: false
        },
        series: [],
        title: {},
        noData: {
          text: "Loading..."
        }
      },
      series: []
    };
  },
  watch: {
    distribution: function(data) {
      if (data != null) {
        // this.putIntoArray(this.intervalArray);
        this.updateSeriesLine(this.distribution);
      }
    }
    // Interval: function(data) {
    //   if (data != null) {
    //     this.putIntoArray(this.dataValue);
    //     this.updateSeriesLine();
    //   }
    // }
  },
  created() {},
  mounted() {
    // this.putIntoArray(this.intervalArray);
    this.updateSeriesLine(this.distribution);
  },
  methods: {
    // putIntoArray(jsonObject, targetArray) {
    //   for (var key in jsonObject) {
    //     targetArray.push(jsonObject[key]);
    //   }
    // },
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
    }
  }
};
</script>
