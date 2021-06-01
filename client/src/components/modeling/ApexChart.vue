<template>
  <div>
    <apexchart ref="testChart" type="line" height="250" :options="testChartOption"></apexchart>
    <apexchart ref="validChart" type="line" height="250" :options="validChartOption"></apexchart>
  </div>
</template>

<script>
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";
//vuex
import { eventBus } from "@/main";

import { mapState, mapGetters, mapActions } from "vuex";

export default {
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음

  data() {
    return {
      actual: null,
      predictive: null,

      series: [[{ data: [] }]],

      // original

      //mainfirstChartOption
      testChartOption: {
        chart: {
          type: "line",
          toolbar: {
            show: false
          }
          // background: "#f8f8f8"
        },
        title: {
          text: "Test",
          align: "left",
          style: {
            fontSize: "16px",
            fontWeight: "bold"
          }
        },
        colors: [" #03A9F4 ", " #81d4fa", "#00ab08", "#4ded30"],
        markers: {
          size: 3,
          strokeWidth: 0.1,
          strokeColor: "skyblue",
          hover: {
            size: 2,
            strokeColor: "#fff"
          }
        },
        grid: {
          show: false
        },
        legend: {
          //Grouping시 변경
          show: true,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        },
        noData: {
          text: "Loading..."
        },
        xaxis: {
          tickAmount: 5,
          // floating: true,
          labels: {
            offsetX: 0,
            // show: false,
            minHeight: 50,
            rotate: -30,
            rotateAlways: true,
            hideOverlappingLabels: true,
            style: {
              fontSize: "10px",
              fontWeight: 200
            }
          }
        },
        yaxis: {
          decimalsInFloat: 1,
          // floating:true,
          axisTicks: {
            show: true
          },
          axisBorder: {
            show: true
          },
          // floating: true,
          labels: {
            show: true
          }
        }
      },
      validChartOption: {
        chart: {
          type: "line",
          toolbar: {
            show: false
          }
          // background: "#f8f8f8"
        },
        title: {
          text: "Validation",
          align: "left",
          style: {
            fontSize: "16px",
            fontWeight: "bold"
          }
        },
        // colors: ["#E91E63", "#FF9800"],
        colors: ["#00ab08", "#81c147"],
        markers: {
          size: 3,
          strokeWidth: 0.1,

          hover: {
            size: 2,
            strokeColor: "#fff"
          }
        },
        grid: {
          show: false
        },
        legend: {
          //Grouping시 변경
          show: true,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        },
        noData: {
          text: "Loading..."
        },
        xaxis: {
          tickAmount: 5,
          // floating: true,
          labels: {
            offsetX: 0,
            // show: false,
            minHeight: 50,
            rotate: -30,
            rotateAlways: true,
            hideOverlappingLabels: true,
            style: {
              fontSize: "10px",
              fontWeight: 200
            }
          }
        },
        yaxis: {
          decimalsInFloat: 1,
          // floating:true,
          axisTicks: {
            show: true
          },
          axisBorder: {
            show: true
          },
          // floating: true,
          labels: {
            show: true
          }
        }
      }
    };
  },

  created() {},
  mounted() {
    this.$refs.testChart.updateSeries([
      {
        name: "Actual",
        data: this.graphSources["test"]["Actual"]
      },
      {
        name: "Predictive",
        data: this.graphSources["test"]["Predictive"]
      }
    ]);
    this.$refs.validChart.updateSeries([
      {
        name: "Actual",
        data: this.graphSources["valid"]["Actual"]
      },
      {
        name: "Predictive",
        data: this.graphSources["valid"]["Predictive"]
      }
    ]);
  },
  computed: {
    ...mapState({
      graphSources: state => state.modelingResult.graphSources
    })
  },
  methods: {
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[randomIndex[i]]);
      }
    },

    //date methods
    formatDate(dateArray) {
      for (let i = 0; i < dateArray.length; i++) {
        dateArray[i] = new Date(dateArray[i]).getTime();
      }
    },

    //APEX CHART
    resetSeries() {
      this.numOfDragElement = 0;
      this.$refs.testChart[0].updateOptions(
        {
          series: [{}],
          xaxis: {
            categories: []
          }
        },
        false,
        false
      );
      console.log("reset");
    },
    appendSeries(seriesName, dataSet) {
      // for (let i = 0; i < this.$refs.testChart.length; i++) {
      //   this.$refs.testChart[i].appendSeries({
      //     name: seriesName,
      //     data: dataSet
      //   });

      // }
      let newSeries = { name: seriesName, data: dataSet };
      this.series[0].push(newSeries);
    },
    deleteSeries(axisName) {
      // data 초기화
      let indexNumOfAxis = Object.keys(this.dataArrays).indexOf(axisName);
      this.series[0].splice(indexNumOfAxis, 1); //series에서 제거 (그래프 시각적 반영)
      delete this.dataArrays[axisName]; // dataArray에서 제거
      this.axisName.splice(indexNumOfAxis, 1); //axisName에서 제거
      this.resetYaxis();
      console.log(`indexNumOfAxis:${indexNumOfAxis}`);
      // for (let i = 0; i < this.$refs.testChart.length; i++) {
      //   this.$refs.testChart[i].updateSeries([
      //     {
      //       name: axisName,
      //       data: []
      //     }
      //   ]);
      // }

      // this.testChartOption.yaxis.splice(indexNumOfAxis, 1);
    },
    updateSeries(axisName, dataSet) {
      // for (let i = 0; i < this.$refs.testChart.length; i++) {
      //   this.$refs.testChart[i].updateOptions(
      //     {
      //       series: [
      //         {
      //           name: axisName,
      //           data: dataSet
      //         }
      //       ]
      //     },
      //     false,
      //     false
      //   );
      // }
      this.series[0].shift();
      let newSeries = { name: axisName, data: dataSet };
      this.series[0].push(newSeries);
    },
    updateGroupingOption() {
      this.testChartOption.legend["show"] = false;
      this.testChartOption.chart.toolbar["show"] = false;
      // this.testChartOption.xaxis.labels["show"] = false;
      this.testChartOption.yaxis.labels["show"] = false;
      // this.$refs.testChart[0].updateOptions({
      //   yaxis: {
      //     labels: {
      //       show: true
      //     }
      //   }
      // });
    },
    resetYaxis() {
      for (let i = 0; i < this.$refs.testChart.length; i++) {
        this.$refs.testChart[i].updateOptions({
          yaxis: {}
        });
      }
    },
    updateYaxis(axisName, minOfDataset) {
      for (let i = 0; i < this.$refs.testChart.length; i++) {
        this.$refs.testChart[i].updateOptions(
          {
            yaxis: [
              {
                seriesName: axisName[0],
                // tickAmount: 3,
                axisBorder: {
                  color: "#2E93fA"
                },
                labels: {
                  style: {
                    colors: "#2E93fA"
                  }
                },
                title: {
                  text: axisName[0],
                  style: {
                    color: "#2E93fA"
                  }
                }
              },

              {
                seriesName: axisName[1],

                opposite: true,
                // min: minOfDataset,
                labels: {
                  style: {
                    colors: "#00E396"
                  }
                },
                axisBorder: {
                  color: "#00E396"
                },
                title: {
                  text: axisName[1],
                  style: {
                    color: "#00E396"
                  }
                }
              }
            ]
          },
          false,
          false
        );
      }
    },
    updateCategories(newCategories) {
      for (let i = 0; i < this.$refs.testChart.length; i++) {
        this.$refs.testChart[i].updateOptions({
          xaxis: {
            categories: newCategories
          }
        });
      }
    },
    updateGraphType(graphType) {
      this.$refs.testChart.updateOptions({
        chart: {
          type: graphType
        }
      });
    },
    updateSelection() {
      this.$refs.testChart.updateOptions({
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
        this.$refs.testChart.toggleDataPointSelection(0, i);
      }
    },
    resetdataArrays() {
      // console.log("rest");
      this.dataArrays = {};
    },
    resetDateArray() {
      // console.log("rest");
      this.dateArray = [];
    }
  }
};
</script>
<style scoped>
v-col {
  background-color: #000;
  border: 1px solid #000;
}
</style>
