<template>
  <div>
    <Header></Header>

    <v-container fluid>
      <v-row>
        <v-col cols="2">
          <ModelingResultSide />
        </v-col>

        <v-col cols="10">
          <v-toolbar elevation="1" dense>
            <v-spacer></v-spacer>

            <v-btn disabled @click="dialog = true" small color="info">
              Save Model<v-icon right>mdi-content-save</v-icon>
            </v-btn>

            <v-btn small color="success" @click="modifyModeling" class="ml-1">
              Modify Modeling
              <v-icon right small>
                mdi-transit-connection
              </v-icon>
            </v-btn>
            <v-btn @click="runSimulation" class="ml-1" color="orange" dark small>
              Run Simulation
              <v-icon right small>
                mdi-chart-bell-curve-cumulative
              </v-icon>
            </v-btn>
          </v-toolbar>
          <ApexChart
            :graphNames="graphNames"
            :graphOptions="graphOptions"
            :graphHeight="graphHeight"
            :graphType="graphType"
            :graphSource="graphSources"
          >
          </ApexChart>
          <ModelingSummary />
        </v-col>
      </v-row>
      <!-- dialog -->
      <v-dialog v-model="dialog" persistent max-width="400px">
        <v-card>
          <v-container fluid>
            <span class="headline">Name of Case</span>
            <!-- 최상단 메뉴 탭 -->

            <v-text-field v-model="case_name" placeholder="Case 1" required></v-text-field>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="dialog = !dialog" color="gray darken-1" text>
                Close
              </v-btn>
              <v-btn @click="saveModel" color="blue darken-1" @click.once="eventHandler" text>
                Confirm
              </v-btn>
            </v-card-actions>
          </v-container>
        </v-card>
      </v-dialog>
      <SaveChange />
    </v-container>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import ApexChart from "@/components/modeling/ApexChart.vue";
import ModelingSummary from "@/components/modeling/ModelingSummary.vue";
import ModelingResultSide from "@/components/modeling/ModelingResultSide.vue";
import SaveChange from "@/components/save/SaveChange.vue";
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

  components: { ApexChart, ModelingSummary, SaveChange, ModelingResultSide },
  computed: {
    ...mapState({
      graphSources: state => state.modelingData.graphSources,
      modelingSummary: state => state.modelingData.modelingSummary
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
    ...mapMutations("modelingData", ["saveCaseList"]),
    ...mapMutations("modelingData", ["saveGraphSources"]),
    ...mapMutations("modelingData", ["saveModelingSummary"]),
    modifyModeling() {
      let modelingParameter = [500, 0.08, 0.3, 0.04, 0.75, 0.5, 7];
      this.$router.push({ name: "modelingProcess" });
    },
    runSimulation() {
      this.$router.push({ name: "simulations" });
    },
    getPos(e) {
      let obj = e.target;
      this.left = obj.getBoundingClientRect().left;
      this.top = obj.getBoundingClientRect().top;
    },
    loadCases() {
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    },
    saveModel() {
      let vm = this;
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/saveModel";
      axios({
        method: "post",
        url: path,
        data: {
          case_name: this.case_name,
          modelingOption: this.modelingOption,
          algorithm: this.algorithm,
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
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/changeCase";
      this.$axios
        .get(path, {
          params: {
            //algorithmProp 전송
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
    // console.log("created");
    // let caseNameFromUrl = this.$route.params.case;
    // console.log(caseNameFromUrl);
    // if (caseNameFromUrl != "") {
    //   this.changeCase(caseNameFromUrl);
    // }
    // eventBus.$on("changeCase", caseNameFromUrl => {
    //   this.changeCase(caseNameFromUrl);
    // });
  },
  mounted() {}
};
</script>

<style scoped>
.resultContainer {
  /* width: 1000px; */
  height: 1000px;
}
</style>
