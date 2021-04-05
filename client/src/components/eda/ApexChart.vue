<template>
  <div id="container">
    <v-layout row>
      <v-flex xs8>
        <v-layout row>
          <v-flex>
            <apexchart
              ref="edaChart"
              type="line"
              :width="graphWidth"
              :height="graphHeight"
              :options="options"
            ></apexchart>
          </v-flex>
          <!-- <v-flex v-show="multipleXaxis">
            <apexchart
              ref="thirdChart"
              type="line"
              :width="graphWidth"
              :height="graphHeight"
              :options="options"
            >
            </apexchart>
          </v-flex> -->
        </v-layout>
      </v-flex>
      <!-- <v-flex xs8 v-show="multipleYaxis"
        ><apexchart
          ref="secondChart"
          type="line"
          :width="graphWidth"
          :height="graphHeight"
          :options="options"
        >
        </apexchart
      ></v-flex> -->
    </v-layout>
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
      newXaxisInfo: null,
      newYaxisInfo: null,
      graphType: null,
      multipleYaxis: false,
      multipleXaxis: false,
      // original
      dataArray: [],
      dataArray2: [],
      randomIndexArray: [],
      dateArray: [],
      xaxisWhenZoomed: {},
      xaxisWhenSelected: {},
      firstMount: true,
      options: {
        chart: {
          id: "cc",
          group: "social",
          type: "line",
          stacked: false,
          toolbar: {
            show: true,
            autoSelected: "selection",
            tools: {
              download: false,
              customIcons: [
                {
                  icon: '<p  width="20"> G<p>',
                  index: 6,
                  title: "tooltip of the icon",
                  class: "custom-icon",
                  click: function(chart, options, e) {
                    console.log(chart);
                  }
                }
              ]
            }
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
      }
    };
  },
  watch: {
    newXaxisInfo: function(data) {
      if ((data != null || data != undefined) && this.newXaxisInfo["axisPosition"] == "middle") {
        // console.log(`newXaxisInfo: ${this.newXaxisInfo["axisPosition"]}`);
        let axisName = this.newXaxisInfo["evt"].added.element;
        let targetObject = this.dataset[axisName];
        // reset
        this.resetDataArray();
        //preprocess before update graph
        this.randomIndexArray = this.getRandomArray(0, this.indexNum);
        this.putIntoArray(targetObject, this.dateArray, this.randomIndexArray);
        this.updateCategories("edaChart", this.dateArray);
      }
    },
    newYaxisInfo: function(data) {
      if ((data != null || data != undefined) && this.newYaxisInfo["axisPosition"] == "middle") {
        // console.log(`newYaxisInfo: ${this.newYaxisInfo["axisPosition"]}`);

        let axisName = this.newYaxisInfo["evt"].added.element;
        let targetObject = this.dataset[axisName];
        this.resetDataArray();
        //preprocess before update graph
        this.putIntoArray(targetObject, this.dataArray, this.randomIndexArray);
        this.updateYaxis("edaChart", axisName, this.dataArray);
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
      this.checkXaxisPosition(this.newXaxisInfo);
    });
    eventBus.$on("yaxisBeingDragged", newYaxisInfo => {
      this.newYaxisInfo = newYaxisInfo;
      this.checkYaxisPosition(this.newYaxisInfo);
    });
    eventBus.$on("graphTypeBeingSent", graphType => {
      this.graphType = graphType;
    });
    eventBus.$on("yaxisBeingRemoved", status => {
      // console.log(status);
      this.multipleYaxis = status;
      //false
      // this.$refs.secondChart.resetDataArray();
      this.$refs.edaChart.updateOptions({
        chart: {
          height: "500px"
        }
      });
    });
    eventBus.$on("xaxisBeingRemoved", status => {
      // console.log(status);
      this.multipleXaxis = status;
      //false
      // this.$refs.secondChart.resetDataArray();
      this.$refs.edaChart.updateOptions({
        chart: {
          width: "500px"
        }
      });
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

    updateYaxis(chartRefs, columnName, dataSet) {
      // console.log(chartRefs);
      this.$refs[chartRefs].updateSeries(
        [
          {
            name: columnName,
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
    updateVerticalSplitGraphs() {
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
    updateHorizontalSplitGraphs() {
      this.$refs.edaChart.updateOptions({
        chart: {
          id: "ab",
          group: "social1",

          width: "300px"
        }
      });
      this.$refs.thirdChart.updateOptions({
        chart: {
          id: "ef",
          group: "social1",

          width: "300px"
        },
        xaxis: {
          type: "numeric"
        }
      });
      // this.graphWidth = "250px";
    },
    checkYaxisPosition(newYaxisInfo) {
      switch (newYaxisInfo["axisPosition"]) {
        case "top":
          this.updateVerticalSplitGraphs();
          break;
        case "middle":
          break;
        case "bottom":
          this.multipleYaxis = true;
          let axisName = newYaxisInfo["evt"].added.element;
          let targetObject = this.dataset[axisName];
          //preprocess before update graph
          this.resetDataArray();
          //preprocess before update graph
          this.putIntoArray(targetObject, this.dataArray2, this.randomIndexArray);

          this.updateCategories("secondChart", this.dateArray);
          this.updateYaxis("secondChart", axisName, this.dataArray2);
          this.updateVerticalSplitGraphs();

          break;
      }
    },
    checkXaxisPosition(newXaxisInfo) {
      switch (newXaxisInfo["axisPosition"]) {
        case "left":
          // this.updateHorizontalSplitGraphs();
          break;
        case "middle":
          break;
        case "right":
          this.updateHorizontalSplitGraphs();
          this.multipleXaxis = true;

          let axisName = newXaxisInfo["evt"].added.element;
          let targetObject = this.dataset[axisName];
          // reset
          this.resetDateArray();
          //preprocess before update graphs
          this.putIntoArray(targetObject, this.dateArray, this.randomIndexArray);
          break;
      }
    },
    toggleDataPointSelection(xaxis) {
      for (let i = xaxis.min; i <= xaxis.max; i++) {
        this.$refs.edaChart.toggleDataPointSelection(0, i);
      }
    },
    resetDataArray() {
      // console.log("rest");
      this.dataArray2 = [];
    },
    resetDateArray() {
      // console.log("rest");
      this.dateArray = [];
    }
  }
};
</script>
