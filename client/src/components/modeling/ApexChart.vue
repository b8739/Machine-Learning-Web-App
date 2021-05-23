<template>
  <apexchart
    ref="modelingChart"
    type="line"
    height="300"
    :options="firstGroupingChartOption"
  ></apexchart>
</template>

<script>
// randomize function
import * as randomizer from "@/assets/js/randomizer.js";
//vuex
import { eventBus } from "@/main";
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
export default {
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음

  data() {
    return {
      actual: null,
      predictive: null,

      series: [[{ data: [] }]],

      // original

      //mainfirstChartOption
      firstGroupingChartOption: {
        chart: {
          id: "syncChartId",
          group: "syncChartGroup",
          toolbar: {
            //Grouping시 변경
            show: true,
            tools: {
              customIcons: [
                {
                  icon: '<p  width="20">R<p>',
                  index: 6,
                  title: "tooltip of the icon",
                  class: "custom-icon",
                  click: (chart, options, e) => {
                    console.log(options);
                  }
                }
              ]
            }
          },
          sparkline: {
            enabled: false
          },
          type: "line"
        },
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
      // mainoptions
      groupingChartOption: {
        chart: {
          type: "line",
          stacked: false,
          toolbar: {
            show: false,
            autoSelected: "selection"
          },
          //zoom
          zoom: {
            type: "xy",
            enabled: true,
            autoScaleYaxis: true,
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

          events: {
            legendClick: function(chartContext, seriesIndex, config) {
              // console.log(seriesIndex);
              // ...
            },
            // selection events
            selection: (chartContext, { xaxis, yaxis }) => {
              let yaxisObject = { min: null, max: null };
              console.log(xaxis);
              // yaxisObject.min = yaxis[0]["min"];
              // yaxisObject.max = yaxis[0]["max"];
              // this.yaxisWhenSelected = yaxisObject;
              this.xaxisWhenSelected = xaxis;
              this.$emit("xaxis", this.xaxisWhenSelected);
            }
          }
        },
        subtitle: {
          text: undefined,
          align: "center",

          floating: true,
          offsetY: 5,
          style: {
            // fontSize: "12px",
            fontWeight: "normal",
            fontFamily: undefined,
            color: "#9699a2"
          }
        },
        // colors: ['#2E93fA', '#66DA26', '#546E7A', '#E91E63', '#FF9800'],
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
          floating: false,
          labels: {
            offsetX: 0
          },
          type: "datetime",
          labels: {
            // show: false,
            minHeight: 50,
            rotate: -30,
            rotateAlways: true,
            hideOverlappingLabels: false,
            format: "yy/MM/dd",
            style: {
              fontSize: "10px",
              fontWeight: 200
            }
          }
        },
        // mainYaxis
        yaxis: {
          floating: true,
          labels: {
            offsetX: -50
          }
        },
        grid: {
          show: false
        },
        legend: {
          show: false,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        }
      }
    };
  },

  created() {
    eventBus.$on("graphSources", modelResult => {
      this.actual = modelResult["Actual"];
      this.predictive = modelResult["Predictive"];

      this.$refs.modelingChart.updateSeries([
        {
          name: "Actual",
          data: this.actual
        },
        {
          name: "Predictive",
          data: this.predictive
        }
      ]);
    });
  },
  // cons
  mounted() {
    //console.log(this.dataset);
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      indexNum: state => state.initialData.indexNum,
      summarizedInfo: state => state.initialData.summarizedInfo
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
      this.$refs.modelingChart[0].updateOptions(
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
      // for (let i = 0; i < this.$refs.modelingChart.length; i++) {
      //   this.$refs.modelingChart[i].appendSeries({
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
      // for (let i = 0; i < this.$refs.modelingChart.length; i++) {
      //   this.$refs.modelingChart[i].updateSeries([
      //     {
      //       name: axisName,
      //       data: []
      //     }
      //   ]);
      // }

      // this.firstGroupingChartOption.yaxis.splice(indexNumOfAxis, 1);
    },
    updateSeries(axisName, dataSet) {
      // for (let i = 0; i < this.$refs.modelingChart.length; i++) {
      //   this.$refs.modelingChart[i].updateOptions(
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
      this.firstGroupingChartOption.legend["show"] = false;
      this.firstGroupingChartOption.chart.toolbar["show"] = false;
      // this.firstGroupingChartOption.xaxis.labels["show"] = false;
      this.firstGroupingChartOption.yaxis.labels["show"] = false;
      // this.$refs.modelingChart[0].updateOptions({
      //   yaxis: {
      //     labels: {
      //       show: true
      //     }
      //   }
      // });
    },
    resetYaxis() {
      for (let i = 0; i < this.$refs.modelingChart.length; i++) {
        this.$refs.modelingChart[i].updateOptions({
          yaxis: {}
        });
      }
    },
    updateYaxis(axisName, minOfDataset) {
      for (let i = 0; i < this.$refs.modelingChart.length; i++) {
        this.$refs.modelingChart[i].updateOptions(
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
      for (let i = 0; i < this.$refs.modelingChart.length; i++) {
        this.$refs.modelingChart[i].updateOptions({
          xaxis: {
            categories: newCategories
          }
        });
      }
    },
    updateGraphType(graphType) {
      this.$refs.modelingChart.updateOptions({
        chart: {
          type: graphType
        }
      });
    },
    updateSelection() {
      this.$refs.modelingChart.updateOptions({
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
        this.$refs.modelingChart.toggleDataPointSelection(0, i);
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
