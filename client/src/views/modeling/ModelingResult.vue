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

            <v-btn @click="dialog = true" small color="info">
              Save Model<v-icon right>mdi-content-save</v-icon>
            </v-btn>

            <v-btn small color="success" @click="modifyModeling" class="ml-1">
              Modify Modeling
              <v-icon right small>
                mdi-transit-connection
              </v-icon>
            </v-btn>
            <v-btn disabled @click="runSimulation" class="ml-1" color="orange" dark small>
              Run Simulation
              <v-icon right small>
                mdi-chart-bell-curve-cumulative
              </v-icon>
            </v-btn>
          </v-toolbar>
          <!-- <ApexChart
            :graphNames="graphNames"
            :graphHeight="graphHeight"
            :graphType="graphType"
            :graphSource="graphSources"
          >
          </ApexChart> -->
          <PlotlyModelingResult :graphSources="graphSources" />
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
              <v-btn @click="saveModel" color="blue darken-1" text>
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
// import ApexChart from "@/components/modeling/ApexChart.vue";
import ModelingSummary from "@/components/modeling/ModelingSummary.vue";
import ModelingResultSide from "@/components/modeling/ModelingResultSide.vue";
import SaveChange from "@/components/save/SaveChange.vue";
import PlotlyModelingResult from "@/components/modeling/PlotlyModelingResult.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
// window.disable = function disable(id, disabled) {
//   document.querySelector(id).disabled = disabled;
// };

// window.setValue = function setValue(id, value) {
//   document.querySelector(id).value = value;
// };

export default {
  data() {
    return {
      // graphSources: {
      //   test: {
      //     Actual: [
      //       3.53501,
      //       0.06127,
      //       0.02009,
      //       0.06642,
      //       0.1415,
      //       0.01778,
      //       1.15172,
      //       0.06466,
      //       0.08387,
      //       0.0136,
      //       0.57834,
      //       0.22188,
      //       0.08308,
      //       0.0837,
      //       0.09512,
      //       0.09068,
      //       0.12744,
      //       0.04011,
      //       0.03427,
      //       0.35809,
      //       0.17004,
      //       0.04417,
      //       0.10469,
      //       0.09164,
      //       0.13117,
      //       0.62739,
      //       0.22876,
      //       0.02177,
      //       0.11747,
      //       0.03578,
      //       8.71675,
      //       2.77974,
      //       0.0459,
      //       0.01096,
      //       0.25387,
      //       0.37578,
      //       0.05425,
      //       0.21719,
      //       0.06664,
      //       0.03659,
      //       0.06162,
      //       1.27346,
      //       24.3938,
      //       0.12579,
      //       0.07165,
      //       0.09604,
      //       0.09744,
      //       0.05561,
      //       0.21038,
      //       3.67822,
      //       1.42502,
      //       0.67191,
      //       0.06888,
      //       0.03113,
      //       0.51183,
      //       2.36862,
      //       0.75026,
      //       0.40771,
      //       0.62976,
      //       8.64476,
      //       0.0456,
      //       1.22358,
      //       1.35472,
      //       1.25179,
      //       0.10328,
      //       0.03049,
      //       0.19073,
      //       0.7857,
      //       1.20742,
      //       0.16902,
      //       0.33045,
      //       0.0315,
      //       3.32105,
      //       1.6566,
      //       0.12204,
      //       0.0536,
      //       0.97617,
      //       0.06899,
      //       13.5222,
      //       0.24103,
      //       0.04297
      //     ],
      //     Predictive: [
      //       1.4750136137008667,
      //       0.11434689164161682,
      //       0.09992307424545288,
      //       0.12043128907680511,
      //       0.15073370933532715,
      //       0.05973346531391144,
      //       1.1352380514144897,
      //       0.07828368246555328,
      //       0.12358345091342926,
      //       0.1673056185245514,
      //       0.4254905581474304,
      //       0.18148918449878693,
      //       0.1016649603843689,
      //       0.10259310901165009,
      //       0.19104765355587006,
      //       0.06584496796131134,
      //       0.14102214574813843,
      //       0.11915408074855804,
      //       0.08405637741088867,
      //       0.331322580575943,
      //       0.18325884640216827,
      //       0.07775814831256866,
      //       0.25851932168006897,
      //       0.14278361201286316,
      //       0.23196709156036377,
      //       0.5887865424156189,
      //       0.6811234354972839,
      //       0.10788421332836151,
      //       0.1673033982515335,
      //       0.1541662961244583,
      //       6.584686756134033,
      //       5.121878623962402,
      //       0.07182461023330688,
      //       0.08195865154266357,
      //       2.763989210128784,
      //       0.48443084955215454,
      //       0.11042614281177521,
      //       0.169077068567276,
      //       0.16023743152618408,
      //       0.06509026885032654,
      //       0.1334017515182495,
      //       1.8980985879898071,
      //       19.775888442993164,
      //       0.15689881145954132,
      //       0.2077314257621765,
      //       0.1442195177078247,
      //       0.21032561361789703,
      //       0.07775814831256866,
      //       0.09081217646598816,
      //       5.279122352600098,
      //       1.9442003965377808,
      //       0.7257851958274841,
      //       0.11296160519123077,
      //       0.07196119427680969,
      //       0.4979420006275177,
      //       4.745657444000244,
      //       0.8527435064315796,
      //       0.40902674198150635,
      //       0.5696673393249512,
      //       10.84353256225586,
      //       0.16382628679275513,
      //       1.8047058582305908,
      //       0.968411922454834,
      //       1.0075234174728394,
      //       0.1418834924697876,
      //       0.06584496796131134,
      //       0.11718092858791351,
      //       0.6058735847473145,
      //       1.9754319190979004,
      //       0.18871204555034637,
      //       0.39943820238113403,
      //       0.07317635416984558,
      //       3.741844654083252,
      //       2.315239429473877,
      //       0.23648995161056519,
      //       0.06347183138132095,
      //       1.0024664402008057,
      //       0.2046067714691162,
      //       7.071352005004883,
      //       0.1721973568201065,
      //       0.07786713540554047
      //     ]
      //   },
      //   valid: {
      //     Actual: [
      //       14.2362,
      //       9.59571,
      //       24.8017,
      //       41.5292,
      //       67.9208,
      //       20.7162,
      //       11.9511,
      //       7.40389,
      //       14.4383,
      //       51.1358,
      //       14.0507,
      //       18.811,
      //       28.6558,
      //       45.7461,
      //       18.0846,
      //       10.8342,
      //       25.9406,
      //       11.8123,
      //       11.0874,
      //       7.02259,
      //       12.0482,
      //       7.05042,
      //       8.79212,
      //       15.8603,
      //       12.2472,
      //       37.6619,
      //       7.36711,
      //       9.33889,
      //       8.49213,
      //       10.0623,
      //       6.44405,
      //       5.58107,
      //       13.9134,
      //       11.1604,
      //       14.4208,
      //       15.1772,
      //       13.6781,
      //       9.39063,
      //       22.0511,
      //       9.72418,
      //       5.66637,
      //       9.96654,
      //       12.8023,
      //       0.6718,
      //       6.28807,
      //       9.92485,
      //       9.32909,
      //       7.52601,
      //       6.71772,
      //       5.44114,
      //       5.09017,
      //       8.24809,
      //       9.51363,
      //       4.75237,
      //       4.66883,
      //       8.20058,
      //       7.75223,
      //       6.80117,
      //       4.81213,
      //       3.69311,
      //       6.65492,
      //       5.82115,
      //       7.83932,
      //       3.1636,
      //       3.77498,
      //       4.42228,
      //       15.5757,
      //       13.0751,
      //       4.34879,
      //       4.03841,
      //       3.56868,
      //       4.64689,
      //       8.05579,
      //       6.39312,
      //       4.87141,
      //       15.0234,
      //       10.233,
      //       14.3337,
      //       5.82401,
      //       5.70818,
      //       5.73116,
      //       2.81838,
      //       2.37857,
      //       3.67367,
      //       5.69175,
      //       4.83567,
      //       0.15086,
      //       0.18337,
      //       0.20746,
      //       0.10574,
      //       0.11132,
      //       0.17331,
      //       0.27957,
      //       0.17899,
      //       0.2896,
      //       0.26838,
      //       0.23912,
      //       0.17783,
      //       0.22438,
      //       0.06263
      //     ],
      //     Predictive: [
      //       13.63236141204834,
      //       7.5011515617370605,
      //       9.411554336547852,
      //       12.041006088256836,
      //       24.95077133178711,
      //       11.922842025756836,
      //       7.535979747772217,
      //       8.689306259155273,
      //       7.212059497833252,
      //       8.70391845703125,
      //       6.167574405670166,
      //       8.500643730163574,
      //       5.4565510749816895,
      //       13.274991035461426,
      //       13.28915786743164,
      //       10.618098258972168,
      //       12.049568176269531,
      //       5.55453634262085,
      //       5.372960090637207,
      //       7.767951965332031,
      //       3.8109066486358643,
      //       6.760197639465332,
      //       5.498610496520996,
      //       13.197315216064453,
      //       5.91288948059082,
      //       7.015376091003418,
      //       8.849571228027344,
      //       13.337194442749023,
      //       6.3398237228393555,
      //       6.431990146636963,
      //       4.298509120941162,
      //       6.084371089935303,
      //       7.486965179443359,
      //       7.050756454467773,
      //       7.57991361618042,
      //       10.191617965698242,
      //       10.443941116333008,
      //       8.09819507598877,
      //       7.088591575622559,
      //       6.176950931549072,
      //       7.064368724822998,
      //       6.589043617248535,
      //       9.082027435302734,
      //       8.018542289733887,
      //       7.714718818664551,
      //       8.27632999420166,
      //       9.08206558227539,
      //       6.749241828918457,
      //       6.38132905960083,
      //       6.677430629730225,
      //       4.722476482391357,
      //       6.661498069763184,
      //       6.587671756744385,
      //       6.017727375030518,
      //       6.911299705505371,
      //       5.9076361656188965,
      //       6.278268337249756,
      //       5.845678806304932,
      //       4.722761631011963,
      //       4.296401500701904,
      //       5.770448684692383,
      //       3.6838669776916504,
      //       6.318109512329102,
      //       3.3110909461975098,
      //       5.309591770172119,
      //       6.139886379241943,
      //       4.6404523849487305,
      //       5.611473560333252,
      //       6.634988307952881,
      //       4.362786769866943,
      //       3.870828866958618,
      //       3.7739956378936768,
      //       7.3882737159729,
      //       8.762588500976562,
      //       6.464482307434082,
      //       7.44786262512207,
      //       8.227473258972168,
      //       3.820603609085083,
      //       6.239065647125244,
      //       3.652679443359375,
      //       4.031508445739746,
      //       3.5017449855804443,
      //       3.4097812175750732,
      //       3.3197782039642334,
      //       3.7597086429595947,
      //       3.382676601409912,
      //       3.413907051086426,
      //       4.525973796844482,
      //       4.373840808868408,
      //       3.8255326747894287,
      //       3.342780351638794,
      //       0.3815896809101105,
      //       0.42506977915763855,
      //       0.36671051383018494,
      //       0.4701548218727112,
      //       0.3726366460323334,
      //       0.3844582736492157,
      //       0.3919958472251892,
      //       0.408307284116745,
      //       0.18443448841571808
      //     ]
      //   }
      // },
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

  components: { ModelingSummary, SaveChange, ModelingResultSide, PlotlyModelingResult },
  computed: {
    ...mapState({
      modelingRequest: state => state.modelingData.modelingRequest,
      modelingDataset: state => state.modelingData.modelingDataset,
      graphSources: state => state.modelingData.graphSources,
      modelingSummary: state => state.modelingData.modelingSummary,

      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName
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
      let path = "http://localhost:5000/loadCases";
      this.$axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    },
    saveModel() {
      let vm = this;
      let path = "http://localhost:5000/saveModel";
      this.$axios({
        method: "post",
        url: path,
        data: {
          projectName: this.projectName,
          modelingDataset: this.modelingDataset,

          case_name: this.case_name,
          inputs: this.modelingRequest.inputs,

          targets: this.modelingRequest.targets,
          parameters: this.modelingRequest.algorithm.parameters,

          algorithm: this.modelingRequest.algorithm.name,
          modelingSummary: this.modelingSummary,

          graphSources: this.graphSources
        }
      }).then(function(res) {
        alert(res.data);
        vm.loadCases();
      });

      this.dialog = !this.dialog;
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
