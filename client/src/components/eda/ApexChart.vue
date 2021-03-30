<template>
  <div id="container">
    <apexchart
      ref="edaChart"
      type="line"
      :width="graphWidth"
      :height="graphHeight"
      :options="options"
    ></apexchart>
    <apexchart
      v-show="axisMoreThanOne"
      ref="secondChart"
      type="line"
      :width="graphWidth"
      :height="graphHeight"
      :options="otherOptions"
    >
    </apexchart>
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
      // eventbus
      newXaxisKey: null,
      newYaxisInfo: null,
      graphType: null,
      axisMoreThanOne: false,
      // original
      dataArray: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      firstMount: true,

      options: {
        chart: {
          id: "cc",
          group: "social",
          type: "area",
          toolbar: {
            show: true
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
          toolbar: {
            autoSelected: "selection"
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
          type: "datetime",
          labels: {
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
          labels: {
            minWidth: 40
          }
        },
        legend: {
          show: true,
          showForSingleSeries: true,
          position: "bottom"
        },
        stroke: {
          width: 1
        }
      },
      otherOptions: {
        chart: {
          id: "dd",
          group: "social",
          type: "area",
          toolbar: {
            show: true
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
          toolbar: {
            autoSelected: "selection"
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
          type: "datetime",
          labels: {
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
          labels: {
            minWidth: 40
          }
        },
        legend: {
          show: true,
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
    newXaxisKey: function(data) {
      if (data != null || data != undefined) {
        const axisName = data.added.element;
        let targetObject = this.dataset[axisName];
        // reset
        this.resetSeries();
        //preprocess before update graph
        this.randomIndexArray = this.getRandomArray(0, this.indexNum);
        this.putIntoArray(targetObject, this.dateArray, this.randomIndexArray);
        this.updateCategories("edaChart", this.dateArray);
      }
    },
    newYaxisInfo: function(data) {
      if ((data != null || data != undefined) && this.newYaxisInfo["axisPosition"] == "middle") {
        console.log(this.newYaxisInfo["axisPosition"]);
        let axisName = this.newYaxisInfo["evt"].added.element;
        let targetObject = this.dataset[axisName];
        this.resetSeries();
        //preprocess before update graph
        this.putIntoArray(targetObject, this.dataArray, this.randomIndexArray);
        this.updateYaxis("edaChart", this.dataArray);
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
    eventBus.$on("xaxisBeingDragged", newXaxisKey => {
      this.newXaxisKey = newXaxisKey;
    });
    eventBus.$on("yaxisBeingDragged", newYaxisInfo => {
      this.newYaxisInfo = newYaxisInfo;
      this.checkAxisPosition(this.newYaxisInfo);
    });
    eventBus.$on("graphTypeBeingSent", graphType => {
      this.graphType = graphType;
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
    ...mapState({ dataset: state => state.dataset, indexNum: state => state.indexNum })
  },
  methods: {
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

    updateYaxis(chartRefs, dataSet) {
      console.log(chartRefs);
      this.$refs[chartRefs].updateSeries(
        [
          {
            data: dataSet
          }
        ],
        false,
        true
      );
    },
    updateCategories(chartRefs, newCategories) {
      this.$refs[chartRefs].updateOptions({
        xaxis: {
          categories: newCategories
        }
      });
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
    updateSplitGraphs() {
      this.$refs.edaChart.updateOptions({
        chart: {
          // sync graph info
          id: "ab",
          group: "social",
          //size
          height: "250px"
        }
      });
      this.$refs.secondChart.updateOptions({
        chart: {
          // sync graph info
          id: "cd",
          group: "social",
          //size
          height: "250px"
        }
      });
    },
    checkAxisPosition(newYaxisInfo) {
      switch (newYaxisInfo["axisPosition"]) {
        case "top":
          this.updateSplitGraphs();
          break;
        case "middle":
          break;
        case "bottom":
          this.axisMoreThanOne = true;
          let axisName = newYaxisInfo["evt"].added.element;
          let targetObject = this.dataset[axisName];
          //preprocess before update graph
          this.resetSeries();
          //preprocess before update graph
          this.putIntoArray(targetObject, this.dataArray, this.randomIndexArray);

          this.updateCategories("secondChart", this.dateArray);
          this.updateYaxis("secondChart", this.dataArray);
          this.updateSplitGraphs();

          break;
      }
    },
    toggleDataPointSelection(xaxis) {
      for (let i = xaxis.min; i <= xaxis.max; i++) {
        this.$refs.edaChart.toggleDataPointSelection(0, i);
      }
    },
    resetSeries() {
      // console.log("rest");
      this.dataArray = [];
    }
  }
};
</script>
