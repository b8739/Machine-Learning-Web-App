<template>
  <v-dialog v-model="dialog" width="1000">
    <v-btn @click="rangeStartValues.push(1)">hello</v-btn>
    <v-container fluid class="pa-0">
      <v-card rounded>
        <v-row class="ma-0 ">
          <v-spacer></v-spacer>
          <v-btn x-small min-width="20" min-height="30" @click="closeStepper"
            ><v-icon small>mdi-close</v-icon>
          </v-btn>
        </v-row>
        <v-row justify="center" class="ma-0">
          <v-card-title class="pa-0"> Simulation Wizard</v-card-title>
        </v-row>
        <v-divider></v-divider>
        <v-row justify="center" class="ma-0">
          <v-col cols="8">
            <v-text-field
              hide-details
              outlined
              label="Simulation Name"
              placeholder="Simulation Name"
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
        <v-tabs centered v-model="tab">
          <v-tab>1. Observed Variable</v-tab>
          <v-tab>2. Random Number </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <!-- 1. Input/target -->
          <v-tab-item>
            <v-container>
              <v-row>
                <!-- <v-card-text>Select the input(s) and target features you want to use.</v-card-text> -->
                <v-col cols="12">
                  <InputColumnList />
                </v-col>
                <!-- actions 1-->
                <v-col cols="12">
                  <v-card-actions>
                    <v-btn color="primary" @click="tab = 0">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="stepOneFinished">Next</v-btn>
                  </v-card-actions>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
          <!-- 2.Simulation -->
          <v-tab-item>
            <v-container>
              <v-subheader>
                Set the Range of Random Number
              </v-subheader>
              <v-row class="py-5" justify="center">
                <v-col>
                  <v-card width="100%" min-height="300px" elevation="0">
                    <!-- customized -->

                    <!-- toolbar -->

                    <!-- text-field -->

                    <v-card outlined min-height="550px" class="rangeCard">
                      <v-pagination
                        class="mt-4"
                        v-model="page"
                        :length="paginationLength"
                        circle
                      ></v-pagination>
                      <v-row
                        v-for="(column, columnIndex) in columns"
                        v-show="previousPage - 1 < columnIndex && columnIndex < currentPage"
                        :key="columnIndex"
                        align="center"
                        class="mt-5"
                      >
                        <div style="width:40px">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                class="pl-7"
                                right
                                v-bind="attrs"
                                v-on="on"
                                v-if="isObservedVariable(column)"
                                >mdi-check</v-icon
                              >
                            </template>
                            <span>Observed Variable</span>
                          </v-tooltip>
                        </div>
                        <v-col cols="2" class="pl-0" style="text-align:center">
                          <v-card-text>{{ column }}</v-card-text></v-col
                        >
                        <!-- <v-col cols="2"
                          ><v-select hide-details label="Distribution  (Optional)"></v-select
                        ></v-col> -->

                        <v-col cols="2" align-self="center">
                          <v-text-field
                            @click="
                              openHelper(column);
                              getHelperValues(column);
                              setTargetTextField(columnIndex, 'start');
                            "
                            hide-details
                            label="Range Min"
                            class="mt-0 pt-0"
                            v-model="rangeStartValues[columnIndex]"
                          ></v-text-field>
                        </v-col>

                        <v-icon x-small>mdi-tilde</v-icon>

                        <v-col cols="2">
                          <v-text-field
                            hide-details
                            @click="
                              openHelper(column);
                              getHelperValues(column);
                              setTargetTextField(columnIndex, 'end');
                            "
                            v-model="rangeEndValues[columnIndex]"
                            label="Range Max"
                            class="mt-0 pt-0"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-card
                        max-width="300"
                        min-height="300"
                        color="rgba(80, 79, 79, 0.817)"
                        dark
                        class="rangeHelper"
                        :disabled="helperStatus"
                      >
                        <v-container>
                          <v-row align="center" justify="center">
                            <v-card-text style="text-align:center"
                              >Range Setting Helper</v-card-text
                            >
                            <v-card-text style="text-align:center" class="subheading pt-0">
                              {{ helperColumn }}</v-card-text
                            >
                            <v-tabs
                              centered
                              v-model="tab_method"
                              dark
                              background-color="rgba(80, 79, 79, 0.817)"
                              light
                            >
                              <v-tab class="vtab">Statistics</v-tab>
                              <v-tab class="vtab">Distribution </v-tab>
                            </v-tabs>
                          </v-row>
                          <v-row
                            align="center"
                            justify="center"
                            v-for="(statistic, index) in statistics"
                            :key="index"
                          >
                            <v-col offset="2">
                              <v-tooltip left>
                                <template v-slot:activator="{ on, attrs }">
                                  <v-chip
                                    v-bind="attrs"
                                    v-on="on"
                                    label
                                    outlined
                                    @mouseover="setStatisticValue(statistic)"
                                    @click="setStatisticValue(statistic)"
                                    >{{ statistic }}</v-chip
                                  >
                                </template>
                                <span>Click to Get Value</span>
                              </v-tooltip>
                            </v-col>
                            <v-col cols="">
                              <v-card-text class="py-0">{{
                                helperValues[statistic]
                              }}</v-card-text></v-col
                            >
                          </v-row>
                        </v-container>
                      </v-card>
                    </v-card>
                  </v-card>
                </v-col>
              </v-row>

              <!-- actions 2-->
              <v-row>
                <v-col cols="12">
                  <v-card-actions align-self="end">
                    <v-btn color="primary" @click="tab = 0">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="stepTwoFinished">Run Simulation</v-btn>
                  </v-card-actions></v-col
                >
              </v-row>
            </v-container>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </v-dialog>
</template>
<script>
import Vue from "vue";
import { eventBus } from "@/main";
import InputColumnList from "@/components/simulation/columnList/InputColumnList.vue";
import TargetColumnList from "@/components/simulation/columnList/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      // helper
      helperStatus: true,
      helperColumn: null,
      helperValues: [],
      rangeStartValues: [null, null, null, null],
      rangeEndValues: [],
      selectedStatistic: [],
      userInput: null,
      values: [],
      searchInput: "s",
      people: [
        { name: "Sandra Adams", group: "Group 1" },
        { name: "Ali Connors", group: "Group 1" },
        { name: "Trevor Hansen", group: "Group 1" },
        { name: "Tucker Smith", group: "Group 1" }
      ],
      distributionSelected: null,
      // tab
      tab: 1,
      tab_distribution: 0,
      tab_method: 0,

      // vmodel values
      rangeValues: [],

      // page
      page: 1,
      length: 2,
      model: 1,

      statistics: ["Min", "Max", "Mean", "Mode", "Median"],
      distributionType: ["Uniform Distribution", "Normal Distribution"],
      focusedStatistic: null,
      focusedIndex: null,

      focusedTextField: null,
      chipColors: [],
      select: { method: "", explanation: "" },

      dialog: true,
      disabledProps: {
        disabled: true
      },

      hideDetailsProps: {
        "hide-details": true
      },
      chosenAlgorithm: null,
      focusedFeature: null,
      hasSaved: false,
      isEditing: null,

      items: [
        { name: "Min", value: "FL" },
        { name: "Max", value: "GA" },
        { name: "Mean", value: "NE" },
        { name: "Mode", value: "CA" },
        { name: "Median", value: "NY" }
      ]
    };
  },
  watch: {
    e6: function(data) {
      if (data > 2) {
        // this.setUniformDistribution();
      }
    }
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,
      observedVariable: state => state.simulationData.observedVariable,
      summarizedInfo: state => state.initialData.summarizedInfo
    }),

    ...mapGetters("initialData", ["columns"]),
    statistic_items() {
      let array;
      array = [
        { name: "Min" },
        { name: "Max", value: "not yet" },
        { name: "Mean", value: "not yet" },
        { name: "Median", value: "not yet" },
        { name: "Mode", value: "not yet" }
      ];
      return array;
    },
    paginationLength() {
      return Math.ceil(this.columns.length / 5);
    },

    currentPage() {
      return this.page * 5;
    },
    previousPage() {
      return this.currentPage - 5;
    }
  },
  methods: {
    // hello() {
    //   Vue.set(this.rangeStartValues, 0, 1);
    // },
    setStatisticValue(statistic) {
      Vue.set(this.focusedTextField, this.focusedIndex, this.helperValues[statistic]);
    },
    getHelperValues(column) {
      let min = this.summarizedInfo["interval"][column]["min"];
      let max = this.summarizedInfo["interval"][column]["max"];
      let mean = this.summarizedInfo["numeric"][column]["mean"];
      let mode = this.summarizedInfo["numeric"][column]["mode"];
      let median = this.summarizedInfo["numeric"][column]["median"];
      // 배열에 삽입해서 반환
      this.helperValues = { Min: min, Max: max, Mean: mean, Median: median, Mode: mode };
      return this.helperValues;
    },
    setTargetTextField(columnIndex, textFieldType) {
      this.focusedIndex = columnIndex;
      if (textFieldType == "start") {
        this.focusedTextField = this.rangeStartValues;
      } else {
        this.focusedTextField = this.rangeEndValues;
      }
    },
    openHelper(column) {
      this.helperColumn = column;
      this.helperStatus = false; //helper 활성화
    },
    toggleTooltip(event) {
      if (event == "blur") {
        this.tooltipStatus = false;
      } else {
        this.tooltipStatus = true;
      }
    },
    test(columnIndex) {
      console.log(columnIndex);
      this.selectedStatistic[columnIndex] = "Min";
    },
    ...mapMutations("simulationData", ["saveSimulationMethod"]),
    showDistributionSet() {
      if (this.distributionSelected == 0) {
        this.setUniformDistribution();
      } else {
        this.setNormalDistribution();
      }

      this.e6 = 2;
    },
    defineProps(column) {
      // uniform일 경우 (this.distributionSelected == 0),

      //  observed variable 빼고 (column != this.observedVariable) 다 비활성화
      if (column != this.observedVariable) return this.disabledProps;
    },
    isObservedVariable(column) {
      if (column == this.observedVariable) return true;
    },
    // setNormalDistribution() {
    //   this.setNormalLabel();
    //   // 초기화 (push 하기 전)
    //   this.rangeStartValues = [];
    //   this.rangeEndValues = [];
    //   // loop
    //   let index = 0;
    //   this.columns.forEach(element => {
    //     // 관찰 변수일 경우에는 3 시그마 값
    //     // 3시그마 값 계산
    //     if (element == this.observedVariable) {
    //       let mean = this.summarizedInfo["numeric"][element]["mean"];

    //       let std = this.summarizedInfo["numeric"][element]["standard deviation"];
    //       let sigma_3_min = mean - 3 * std;
    //       let sigma_3_max = mean + 3 * std;
    //       // console.log(
    //       //   `mean:${mean},std:${std},sigma_3_min:${sigma_3_min},sigma_3_max:${sigma_3_max},`
    //       // );

    //       // 계산된 3시그마 값 지정
    //       this.rangeStartValues.push(sigma_3_min.toFixed(2));
    //       this.rangeEndValues.push(sigma_3_max.toFixed(2));
    //     }
    //     // 그 외 변수들일 경우에는 min,max 값 적용
    //     else {
    //       // category 일 경우, '일단' category라는 string 값 넣어둠
    //       if (this.summarizedInfo["datatype"]["type"][index] == "category") {
    //         this.rangeStartValues.push(0);
    //         // this.rangeEndValues.push(0);
    //       }
    //       // numeric 일 경우
    //       else {
    //         this.rangeStartValues.push(this.summarizedInfo["numeric"][element]["median"]);
    //         // this.rangeEndValues.push(this.summarizedInfo["interval"][element]["max"]);
    //       }
    //     }
    //     index++;
    //   });
    // },
    // setUniformLabel() {
    //   this.startLabel = [];
    //   this.endLabel = [];
    //   this.columns.forEach(element => {
    //     // 관찰 변수일 경우에는 min max 값 적용
    //     if (element == this.observedVariable) {
    //       this.startLabel.push("Min");
    //       this.endLabel.push("Max");
    //     }
    //     // 그 외 변수들일 경우에는 median 값 적용
    //     else {
    //       this.startLabel.push("Median");
    //       // this.endLabel.push("Median");
    //     }
    //   });
    // },
    // setNormalLabel() {
    //   this.startLabel = [];
    //   this.endLabel = [];
    //   this.columns.forEach(element => {
    //     // 관찰 변수일 경우에는 min max 값 적용
    //     if (element == this.observedVariable) {
    //       this.startLabel.push("3 Sigma Min");
    //       this.endLabel.push("3 Sigma Max");
    //     }
    //     // 그 외 변수들일 경우에는 median 값 적용
    //     else {
    //       // this.startLabel.push("Min");
    //       // this.endLabel.push("Max");
    //     }
    //   });
    // },
    // setUniformDistribution() {
    //   this.setUniformLabel();
    //   // 초기화 (push 하기 전)
    //   this.rangeStartValues = [];
    //   this.rangeEndValues = [];
    //   // loop
    //   let index = 0;
    //   this.columns.forEach(element => {
    //     // 관찰 변수일 경우에는 min max 값 적용
    //     if (element == this.observedVariable) {
    //       this.rangeStartValues.push(this.summarizedInfo["interval"][element]["min"]);
    //       this.rangeEndValues.push(this.summarizedInfo["interval"][element]["max"]);
    //     }
    //     // 그 외 변수들일 경우에는 median 값 적용
    //     else {
    //       // category 일 경우 '일단' category라는 string 값 넣어둠
    //       if (this.summarizedInfo["datatype"]["type"][index] == "category") {
    //         this.rangeStartValues.push(0);
    //         // this.rangeEndValues.push(0);
    //       } else {
    //         this.rangeStartValues.push(this.summarizedInfo["numeric"][element]["median"]);
    //         // this.rangeEndValues.push(this.summarizedInfo["numeric"][element]["median"]);
    //       }
    //     }
    //     index++;
    //   });
    // },
    statisticFocused(statistic) {
      let index = this.columns.indexOf(this.focusedFeature);
      this.focusedStatistic = statistic.toLowerCase();
      if (this.focusedStatistic == "min" || this.focusedStatistic == "max") {
        this.focusedTextField[index] = this.summarizedInfo["interval"][this.focusedFeature][
          this.focusedStatistic
        ];
      } else {
        this.focusedTextField[index] = this.summarizedInfo["numeric"][this.focusedFeature][
          this.focusedStatistic
        ];
        // console.log(this.focusedTextField[index]);
      }
    },

    stepOneFinished() {
      this.tab = 1;
      this.setUniformDistribution();

      eventBus.$emit("simulationColumnChecked", true);
    },
    stepTwoFinished() {
      this.saveSimulationMethod(this.select.method);
      this.$router.push({ name: "simulationResult" });
    },

    algorithmClicked(algorithm) {
      this.chosenAlgorithm = algorithm;
    },
    getItems(index) {
      if (index == 0) {
        return this.tableList;
      }
    },
    hideDetails(index) {
      if (index == 2) {
        return this.hideDetailsProps;
      }
    },
    sendFeatures() {
      this.tab = 2;
      eventBus.$emit("stepTwoFinished", true);
    },
    closeStepper() {
      this.dialog = false;
    },
    createModel() {
      this.dialog = false;
      this.saveAlgorithm(this.chosenAlgorithm);
      this.$router.push({ name: "modeling" });
    }
  },
  components: {
    InputColumnList,
    TargetColumnList
  },
  created() {
    eventBus.$on("openSimulation", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>
<style scoped>
.centered-input input {
  text-align: center;
}
.rangeCard {
  position: relative;
}
.rangeHelper {
  position: absolute;

  top: 90px;
  right: 30px;
  /* background-color: rgba(80, 79, 79, 0.817);:  */
}
.vtab {
  font-size: 5px !important;
}
.v-tabs-bar__content {
  background-color: grey !important;
}
.v-text-field .v-label input {
  text-align: center !important;
}
</style>
