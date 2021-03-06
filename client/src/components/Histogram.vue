<template>
  <div>
    <apexchart ref="realtimeChart" width="250" type="bar" :options="options" :series="series">
    </apexchart>
  </div>
</template>

<script>
export default {
  name: "Histogram",
  props: ["dataValue", "indexNum"],
  data() {
    return {
      dataArray: [],
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
    dataValue: function(data) {
      if (data != null) {
        this.putIntoArray(this.dataValue);
        this.updateSeriesLine();
      }
    }
  },
  created() {},
  mounted() {
    this.putIntoArray(this.dataValue);
    this.updateSeriesLine();
  },
  methods: {
    putIntoArray(jsonObject) {
      for (let i = 0; i <= this.indexNum; i++) {
        this.dataArray.push(jsonObject[i]);
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
    }
  }
};
</script>
