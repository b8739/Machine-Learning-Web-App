<template>
  <div>
    <ApexChart
      :graphNames="graphNames"
      :graphOptions="graphOptions"
      :graphHeight="graphHeight"
      :graphType="graphType"
      :graphSource="graphSources"
    >
    </ApexChart>
    <ModelingSummary />
  </div>
</template>
<script>
import { eventBus } from "@/main";
import ApexChart from "@/components/modeling/ApexChart.vue";
import ModelingSummary from "@/components/modeling/ModelingSummary.vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      case_name: "",

      dialog: false,

      left: null,
      top: null,
      graphHeight: 250,
      graphType: "line",
      testChart: "testChart",
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

  components: { ApexChart, ModelingSummary },
  computed: {
    ...mapState({
      graphSources: state => state.modelingResult.graphSources,
      modelingSummary: state => state.modelingResult.modelingSummary
    }),

    graphNames() {
      let graphNames = ["testChart", "validChart"];
      return graphNames;
    },
    graphOptions() {
      let graphOptions = [];
      graphOptions.push(this.testChartOption);
      graphOptions.push(this.validChartOption);
      return graphOptions;
    }
  },
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    getPos(e) {
      let obj = e.target;
      this.left = obj.getBoundingClientRect().left;
      this.top = obj.getBoundingClientRect().top;
    },
    loadCases() {
      let path = "http://localhost:5000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    },
    saveModel() {
      let vm = this;
      let path = "http://localhost:5000/saveModel";
      axios({
        method: "post",
        url: path,
        data: {
          case_name: this.case_name,
          modelingOption: this.modelingOption,
          snippet: this.snippet,
          graphSources: JSON.stringify(this.graphSources),
          modelingSummary: JSON.stringify(this.modelingSummary)
        }
      }).then(function(res) {
        vm.loadCases();
      });

      this.dialog = !this.dialog;
    },
    changeCase(case_name) {
      // changecase
      let path = "http://localhost:5000/changeCase";
      this.$axios
        .get(path, {
          params: {
            //snippetProp 전송
            case_name: case_name
          }
        })
        .then(res => {
          this.saveGraphSources(res.data[0]); // 그래프 값 저장
          this.saveModelingSummary(res.data[1]); // 테이블 값 저장
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    console.log("created");
    let caseNameFromUrl = this.$route.params.case;
    console.log(caseNameFromUrl);
    if (caseNameFromUrl != "") {
      this.changeCase(caseNameFromUrl);
    }
    eventBus.$on("changeCase", caseNameFromUrl => {
      this.changeCase(caseNameFromUrl);
    });
  },
  mounted() {}
};
</script>

<style scoped></style>
