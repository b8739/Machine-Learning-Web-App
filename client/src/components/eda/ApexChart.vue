<template>
  <div id="container">
    <button @click="something()">hi</button>
    <v-container>
      <v-row no-gutters v-for="(eachChart, IndexSyncChart) in numOfSyncChart" :key="IndexSyncChart">
        <v-col
          v-for="(eachChart, index) in quantileInfo"
          :key="index"
          cols="12"
          :sm="quantileInfo.length === 1 ? 12 : 3"
        >
          <v-card>
            <v-card-subtitle
              v-if="quantileInfo.length > 1 && IndexSyncChart == 0"
              class="justify-center"
            >
              {{ quantilePrevIndex(index) }} ~ {{ quantileInfo[index] }}
            </v-card-subtitle>
            <apexchart
              ref="edaChart"
              type="line"
              :width="graphWidth"
              :height="numOfSyncChart.length === 2 ? 200 : auto"
              :options="firstGroupingChartOption"
              :series="series[IndexSyncChart]"
            ></apexchart>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
//vuex
import { eventBus } from "@/main";
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
export default {
  name: "ApexChart",

  props: ["graphWidth", "graphHeight", "date", "editModal_hidden", "rawDataset", "seriesName"],
  // legend를 하나만 씀으로 "nameChangeMark" props 로 받지 않음

  data() {
    return {
      removedYaxisName: null,
      series: [[{ data: [] }]],
      numOfDragElement: 0,
      numOfSyncChart: [1],
      quantileInfo: [1],
      // eventbus
      newXaxisInfo: null,
      newYaxisInfo: null,
      graphType: null,
      xGroupInfo: null,
      // original
      dataArrays: {},
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      axisName: [],
      firstMount: true,
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
          type: "datetime",
          // floating: true,
          labels: {
            offsetX: 0,
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

  watch: {
    newXaxisInfo: function(data) {
      if (data != null || data != undefined) {
        // console.log(`newXaxisInfo: ${this.newXaxisInfo["axisPosition"]}`);
        let axisName = this.newXaxisInfo["evt"].added.element;
        let targetObject = this.dataset[axisName];
        // reset
        this.resetdataArrays();
        //preprocess before update graph
        this.randomIndexArray = this.getRandomArray(0, this.indexNum);
        this.putIntoArray(targetObject, this.dateArray, this.randomIndexArray);
        this.updateCategories(this.dateArray);
      }
    },
    newYaxisInfo: function(data) {
      if (data != null || data != undefined) {
        // console.log(`newYaxisInfo: ${this.newYaxisInfo["axisPosition"]}`);
        this.axisName.push(this.newYaxisInfo["evt"].added.element);
        let axisName = this.axisName[this.axisName.length - 1];
        this.dataArrays[axisName] = [];
        let targetObject = this.dataset[axisName];
        this.numOfDragElement = this.newYaxisInfo["numOfDragElement"];

        //yaxis를 처음 추가할 때
        if (this.numOfDragElement == 0) {
          this.putIntoArray(targetObject, this.dataArrays[axisName], this.randomIndexArray);
          this.updateSeries(axisName, this.dataArrays[axisName]);
        }
        //yaxis가 이미 1개 이상 존재할 때
        else {
          this.putIntoArray(targetObject, this.dataArrays[axisName], this.randomIndexArray);
          let gapOfDatasets = Math.abs(
            this.dataArrays[this.axisName[this.axisName.length - 2]][0] - targetObject[0]
          );
          //2개의 데이터셋의 격차가 커서, yaxis를 양쪽으로 나누어야 할 경우
          if (gapOfDatasets >= 10) {
            let minOfDataset = Math.round(
              Math.min.apply(null, this.dataArrays[axisName]) -
                Math.min.apply(null, this.dataArrays[axisName]) * 0.5
            );
            // console.log(minOfDataset);
            this.updateYaxis(this.axisName, minOfDataset);
            this.appendSeries(axisName, this.dataArrays[axisName]);

            //2개의 데이터셋의 격차가 적어서, yaxis를 공유하는 경우
          } else {
            this.appendSeries(axisName, this.dataArrays[axisName]);
          }
          // console.log(this.dataArrays);
        }
      }
    },
    xGroupInfo: function(data) {
      if (data != null || data != undefined) {
        let xGroupName = this.xGroupInfo["evt"].added.element;
        // console.log(`xGroupName: ${xGroupName}`);
        this.updateGroupingOption();
        this.quantileInfo = [];
        this.quantileInfo.push(this.summarizedInfo[0].quantile1[xGroupName]);
        this.quantileInfo.push(this.summarizedInfo[0].quantile2[xGroupName]);
        this.quantileInfo.push(this.summarizedInfo[0].quantile3[xGroupName]);
        this.quantileInfo.push(this.summarizedInfo[0].quantile4[xGroupName]);
      }
    },

    numOfSyncChart: function(data) {
      this.firstGroupingChartOption.xaxis.categories = this.dateArray;
      this.series.push([{ data: [] }]);
      for (let i = 0; i < this.series.length; i++) {
        this.series[i][0].name = this.axisName[i];
        this.series[i][0].data = this.dataArrays[this.axisName[i]];
      }
    },
    graphType: function(data) {
      if (data != null || data != undefined) {
        this.updateGraphType(data);
        console.log(data);
      }
    },

    immediate: true
  },

  created() {
    // eventbus
    eventBus.$on("xaxisBeingDragged", newXaxisInfo => {
      this.newXaxisInfo = newXaxisInfo;
    });
    eventBus.$on("xaxisBeingRemoved", status => {
      this.$refs.edaChart[0].updateOptions({
        chart: {
          width: "500px"
        }
      });
    });
    eventBus.$on("yaxisBeingDragged", newYaxisInfo => {
      this.newYaxisInfo = newYaxisInfo;
    });
    eventBus.$on("yaxisBeingRemoved", removedYaxisName => {
      this.deleteSeries(removedYaxisName.removed.element);
    });

    eventBus.$on("xGroupBeingDragged", xGroupInfo => {
      this.xGroupInfo = xGroupInfo;
    });

    eventBus.$on("xGroupBeingRemoved", xGroupInfo => {
      this.quantileInfo = [1];
    });
    eventBus.$on("graphTypeBeingSent", graphType => {
      this.graphType = graphType;
    });
    eventBus.$on("addSyncBottom", axisInfo => {
      this.numOfSyncChart.push(0);
      let axisName = axisInfo["evt"].added.element;
      this.axisName.push(axisName);
      let targetObject = this.dataset[axisName];
      this.dataArrays[axisName] = [];
      this.putIntoArray(targetObject, this.dataArrays[axisName], this.randomIndexArray);
    });
    eventBus.$on("removeSyncBottom", axisInfo => {
      this.numOfSyncChart.pop();
    });

    //first mount 감지
    if (this.rawDataset != null || this.rawDataset != undefined) {
      let objectLength = Object.keys(this.rawDataset).length;
      if (objectLength != 0) {
        this.firstMount = false;
      }
    }
  },
  // cons
  mounted() {
    //console.log(this.dataset);
  },
  computed: {
    ...mapState({
      dataset: state => state.dataset,
      indexNum: state => state.indexNum,
      summarizedInfo: state => state.summarizedInfo
    })
  },
  methods: {
    something() {
      console.log(Object.keys(this.dataArrays).indexOf(this.axisName[0]));

      // this.makeSyncChart();
      // this.series[0][0].data = [];
      // console.log(this.series);
    },

    makeSyncChart() {
      this.updateCategories(this.dateArray);
    },
    quantilePrevIndex(index) {
      if (index == 0) {
        return 0;
      } else {
        return this.quantileInfo[index - 1];
      }
    },
    putIntoArray(jsonObject, targetArray, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        targetArray.push(jsonObject[randomIndex[i]]);
      }
    },

    //preprocess methods
    randomizeDataset(dataset_unrandomized, dataset_randomized, randomIndex) {
      let tempArray = [];
      for (let i = 0; i < randomIndex.length; i++) {
        tempArray.push(dataset_unrandomized[randomIndex[i]]); //이게 정말 randomize되는것
        // targetArray.push(dataset_unrandomized[i]);
      }
      dataset_randomized.push(tempArray);
    },
    randomizeDate(dataset_unrandomized, dataset_randomized, randomIndex) {
      for (let i = 0; i < randomIndex.length; i++) {
        dataset_randomized.push(dataset_unrandomized[randomIndex[i]]); //이게 정말 randomize되는것
        // targetArray.push(dataset_unrandomized[i]);
      }
    },
    //date methods
    formatDate(dateArray) {
      for (let i = 0; i < dateArray.length; i++) {
        dateArray[i] = new Date(dateArray[i]).getTime();
      }
    },
    //randomize methods
    getCount(datasetLength) {
      return Math.round(datasetLength * 0.02);
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
    resetSeries() {
      this.numOfDragElement = 0;
      this.$refs.edaChart[0].updateOptions(
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
      // for (let i = 0; i < this.$refs.edaChart.length; i++) {
      //   this.$refs.edaChart[i].appendSeries({
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
      // for (let i = 0; i < this.$refs.edaChart.length; i++) {
      //   this.$refs.edaChart[i].updateSeries([
      //     {
      //       name: axisName,
      //       data: []
      //     }
      //   ]);
      // }

      // this.firstGroupingChartOption.yaxis.splice(indexNumOfAxis, 1);
    },
    updateSeries(axisName, dataSet) {
      // for (let i = 0; i < this.$refs.edaChart.length; i++) {
      //   this.$refs.edaChart[i].updateOptions(
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
      // this.$refs.edaChart[0].updateOptions({
      //   yaxis: {
      //     labels: {
      //       show: true
      //     }
      //   }
      // });
    },
    resetYaxis() {
      for (let i = 0; i < this.$refs.edaChart.length; i++) {
        this.$refs.edaChart[i].updateOptions({
          yaxis: {}
        });
      }
    },
    updateYaxis(axisName, minOfDataset) {
      for (let i = 0; i < this.$refs.edaChart.length; i++) {
        this.$refs.edaChart[i].updateOptions(
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
      for (let i = 0; i < this.$refs.edaChart.length; i++) {
        this.$refs.edaChart[i].updateOptions({
          xaxis: {
            categories: newCategories
          }
        });
      }
    },
    updateGraphType(graphType) {
      this.$refs.edaChart.updateOptions({
        chart: {
          type: graphType
        }
      });
    },
    updateSelection() {
      this.$refs.edaChart.updateOptions({
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
        this.$refs.edaChart.toggleDataPointSelection(0, i);
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
