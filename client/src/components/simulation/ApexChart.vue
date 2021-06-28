<template>
  <div class="mt-5">
    <apexchart
      ref="simulationChart"
      type="line"
      height="250"
      :options="simulationChartOption"
    ></apexchart>
  </div>
</template>

<script>
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";
//vuex
import { eventBus } from "@/main";

import { mapState, mapGetters, mapActions, mapMutations } from "vuex";

export default {
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음

  data() {
    return {
      chartStatus: false,
      actual: null,
      predictive: null,

      series: [[{ data: [] }]],

      // original

      //mainfirstChartOption
      simulationChartOption: {
        chart: {
          animation: {
            enabled: false
          },
          type: "line",
          toolbar: {
            show: false
          }
          // background: "#f8f8f8"
        },
        title: {
          text: "Simulation",
          align: "left",
          style: {
            fontSize: "16px",
            fontWeight: "bold"
          }
        },
        colors: [" #03A9F4 ", " #81d4fa", "#00ab08", "#4ded30"],
        markers: {
          size: 1,
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
          show: false,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        },
        noData: {
          text: "Loading..."
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          title: {
            text: "CRIM"
          },
          tickAmount: 5,
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
          title: {
            text: "MEDV"
          },
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

  watch: {
    graphSources: function(data) {
      this.updateChart();
      this.updateCategories(this.graphSources["simulated"]);
    }
  },
  created() {
    this.chartStatus = true;
    this.runSimulation();
  },
  mounted() {
    this.updateChart();
    this.updateCategories(this.graphSources["simulated"]);
  },
  computed: {
    ...mapState({
      graphSources: state => state.simulationResult.graphSources,
      simulationInput: state => state.simulationData.simulationInput,
      simulationMethod: state => state.simulationData.simulationMethod
    })
  },
  methods: {
    ...mapMutations("simulationResult", ["saveGraphSources"]),

    runSimulation() {
      // default
      if (this.simulationMethod == "Default Setting") {
        let path = "http://localhost:5000/simulation_default";
        this.$axios
          .get(path, {
            params: {
              simulationInput: this.simulationInput
            }
          })
          .then(res => {
            this.saveGraphSources(res.data); // 그래프 값 저장
          })
          .catch(error => {
            console.error(error);
          });
      }
      // customzied
      else if (this.simulationMethod == "Customized Setting") {
        console.log("customized");
      }
    },

    updateChart() {
      this.$refs.simulationChart.updateSeries([
        {
          name: "Simulation",
          data: this.graphSources["predicted"]
        }
      ]);
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
      this.$refs.simulationChart.updateOptions({
        xaxis: {
          categories: newCategories,
          tickAmount: 5
        }
      });
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
