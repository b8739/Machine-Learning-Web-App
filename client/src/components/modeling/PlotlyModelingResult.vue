<template>
  <v-card class="mt-1" elevation="0">
    <v-container>
      <!-- <v-btn @click="test()"></v-btn> -->
      <v-row>
        <div ref="testResult"></div>
      </v-row>
      <v-row>
        <div ref="validResult"></div>
      </v-row>
    </v-container>
  </v-card>
</template>
<script>
export default {
  watch: {
    graphSources: {
      handler: function(data) {
        this.updatePlot();
      },
      deep: true
    }
  },
  props: ["graphSources"],
  computed: {
    testPlot() {
      return this.$refs["testResult"];
    },
    validPlot() {
      return this.$refs["validResult"];
    }
  },
  created() {},
  mounted() {
    this.createPlot();
    this.updatePlot();
  },
  methods: {
    test() {
      console.log(this.$refs["testResult"]);
      this.updatePlot();
    },
    createPlot() {
      Plotly.newPlot(this.testPlot, this.data, this.layout, this.config);
      Plotly.newPlot(this.validPlot, this.data, this.layout, this.config);
    },
    updatePlot() {
      let data = {};
      let colors = {
        test: { Actual: "rgb(65,105,225)", Predictive: "rgb(0,191,255)" },
        valid: { Actual: "rgb(80, 200, 120)", Predictive: "rgb(34, 139, 34)" }
      };
      Object.keys(this.graphSources).forEach(key => {
        //key: test/valid
        data[key] = [];
        Object.keys(this.graphSources[key]).forEach(nestedKey => {
          //nestedKey: actual/predictive
          let trace = {
            y: this.graphSources[key][nestedKey],
            name: key + " " + nestedKey, //key: test/valid,
            type: "scattergl",
            mode: "lines+markers",
            marker: {
              size: 1
            },
            line: {
              color: colors[key][nestedKey],
              width: 1
            },

            showlegend: true
          };
          data[key].push(trace);
        });
        if (key == "test") {
          this.layout["title"] = "Test Result";
          Plotly.react(this.testPlot, data[key], this.layout, this.config);
        } else {
          this.layout["title"] = "Valid Result";
          Plotly.react(this.validPlot, data[key], this.layout, this.config);
        }
      });
    }
  },
  data() {
    return {
      data: [
        {
          // type: "scatter",
          mode: "lines+markers",
          marker: {
            size: 5
            // marker is an object, valid marker keys: #scatter-marker
          },
          line: {
            // color: "rgb(219, 64, 82)",
            width: 1
          },

          showlegend: true
        }
      ],
      layout: {
        width: 800,
        height: 200,
        margin: {
          l: 30,
          r: 20,
          b: 20,
          t: 40,
          pad: 4
        },
        colorway: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],
        xaxis: {
          automargin: true
        },
        yaxis: {
          automargin: true
          // overlaying: "y"
        },
        xaxis2: {
          automargin: true
        },
        yaxis2: {
          automargin: true
          // overlaying: "y"
        },
        title: {
          text: "Modeling Result"
        }
        // grid: {
        //   rows: 2,
        //   columns: 1,
        //   pattern: "independent"
        // }
      },
      config: {
        showSendToCloud: false,
        displaylogo: false,
        responsive: true,
        showEditInChartStudio: false,

        modeBarButtonsToRemove: ["sendDataToCloud"]
      }
    };
  }
};
</script>
