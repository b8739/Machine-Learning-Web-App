<template>
  <v-dialog v-model="dialog" max-width="810">
    <v-container fluid class="pa-0">
      <v-card max-width="900" min-height="700" rounded>
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
          <v-tab>2. Distribution Type </v-tab>
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
              <v-stepper v-model="e6" vertical non-linear>
                <v-stepper-step :complete="e6 > 1" step="1" editable>
                  Select Distribution Type
                </v-stepper-step>

                <v-stepper-content step="1">
                  <v-radio-group row v-model="distributionSelected">
                    <v-radio label="Uniform"></v-radio>
                    <v-radio label="Normal"></v-radio>
                  </v-radio-group>

                  <v-btn color="primary" @click="showDistributionSet()">
                    Continue
                  </v-btn>
                  <v-btn text>
                    Cancel
                  </v-btn>
                </v-stepper-content>
                <v-stepper-step :complete="e6 > 2" step="2">
                  Define the Range of Random Number
                </v-stepper-step>
                <v-stepper-content step="2">
                  <v-row class="py-5" justify="center">
                    <v-col>
                      <v-card width="100%" min-height="300px" elevation="0">
                        <!-- customized -->

                        <!-- toolbar -->
                        <v-toolbar outlined elevation="0">
                          <v-spacer></v-spacer>
                          <v-chip-group>
                            <v-chip
                              v-for="(statistic, index) in statistics"
                              :key="index"
                              outlined
                              :color="chipColors[index]"
                              @click="statisticFocused(statistic)"
                              >{{ statistic }}
                            </v-chip>
                          </v-chip-group>
                          <!--  -->
                          <v-spacer></v-spacer>
                        </v-toolbar>

                        <!-- text-field -->

                        <v-card outlined min-height="500px">
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
                            justify="center"
                            align="center"
                            class="mt-5"
                          >
                            <v-col cols="1">
                              <v-icon v-if="isObservedVariable(column)">mdi-eye</v-icon></v-col
                            >
                            <v-col cols="2" class="pr-0">
                              <v-card-text class="font-weight-bold pr-0">{{
                                summarizedInfo["datatype"]["type"][columnIndex].toUpperCase()
                              }}</v-card-text></v-col
                            >
                            <v-col cols="2" class="pl-0" style="text-align:center">
                              <v-card-text>{{ column }}</v-card-text></v-col
                            >
                            <v-col cols="2" align-self="center" class="px-0">
                              <v-text-field
                                class="centered-input"
                                hide-details
                                dense
                                clearable
                                :label="startLabel[columnIndex]"
                                @focus="featureFocused('start', column)"
                                v-model="startValues[columnIndex]"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="1" class="px-0" style="text-align:center">
                              <v-icon x-small>mdi-tilde</v-icon></v-col
                            >
                            <v-col cols="2" align-self="center" class="px-0">
                              <v-text-field
                                v-bind="defineProps(column)"
                                hide-details
                                dense
                                clearable
                                :label="endLabel[columnIndex]"
                                @focus="featureFocused('end', column)"
                                v-model="endValues[columnIndex]"
                              ></v-text-field
                            ></v-col>
                          </v-row>
                        </v-card>
                      </v-card>
                    </v-col>
                  </v-row>

                  <!-- 디버깅 -->
                  <div v-show="false">
                    <p>focusedFeature: {{ focusedFeature }}</p>
                    <p>focusedStatistic: {{ focusedStatistic }}</p>
                    <p>startValues: {{ startValues }}</p>
                  </div>
                </v-stepper-content>
              </v-stepper>

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
import { eventBus } from "@/main";
import InputColumnList from "@/components/simulation/columnList/InputColumnList.vue";
import TargetColumnList from "@/components/simulation/columnList/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      distributionSelected: null,
      // tab
      tab: 0,
      tab_distribution: 0,
      // stepper
      e6: 1,
      step: 1,

      // vmodel values
      startValues: [],
      endValues: [],
      // vmodel labels
      startLabel: [],
      endLabel: [],
      // page
      page: 1,
      length: 2,
      model: 1,
      statistics: ["Min", "Max", "Mean", "Median"],
      distributionType: ["Uniform Distribution", "Normal Distribution"],
      focusedStatistic: null,
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
      focusedFeature: null
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
    setNormalDistribution() {
      this.setNormalLabel();
      // 초기화 (push 하기 전)
      this.startValues = [];
      this.endValues = [];
      // loop
      let index = 0;
      this.columns.forEach(element => {
        // 관찰 변수일 경우에는 3 시그마 값
        // 3시그마 값 계산
        if (element == this.observedVariable) {
          let mean = this.summarizedInfo["numeric"][element]["mean"];

          let std = this.summarizedInfo["numeric"][element]["standard deviation"];
          let sigma_3_min = mean - 3 * std;
          let sigma_3_max = mean + 3 * std;
          // console.log(
          //   `mean:${mean},std:${std},sigma_3_min:${sigma_3_min},sigma_3_max:${sigma_3_max},`
          // );

          // 계산된 3시그마 값 지정
          this.startValues.push(sigma_3_min.toFixed(2));
          this.endValues.push(sigma_3_max.toFixed(2));
        }
        // 그 외 변수들일 경우에는 min,max 값 적용
        else {
          // category 일 경우, '일단' category라는 string 값 넣어둠
          if (this.summarizedInfo["datatype"]["type"][index] == "category") {
            this.startValues.push(0);
            // this.endValues.push(0);
          }
          // numeric 일 경우
          else {
            this.startValues.push(this.summarizedInfo["numeric"][element]["median"]);
            // this.endValues.push(this.summarizedInfo["interval"][element]["max"]);
          }
        }
        index++;
      });
    },
    setUniformLabel() {
      this.startLabel = [];
      this.endLabel = [];
      this.columns.forEach(element => {
        // 관찰 변수일 경우에는 min max 값 적용
        if (element == this.observedVariable) {
          this.startLabel.push("Min");
          this.endLabel.push("Max");
        }
        // 그 외 변수들일 경우에는 median 값 적용
        else {
          this.startLabel.push("Median");
          // this.endLabel.push("Median");
        }
      });
    },
    setNormalLabel() {
      this.startLabel = [];
      this.endLabel = [];
      this.columns.forEach(element => {
        // 관찰 변수일 경우에는 min max 값 적용
        if (element == this.observedVariable) {
          this.startLabel.push("3 Sigma Min");
          this.endLabel.push("3 Sigma Max");
        }
        // 그 외 변수들일 경우에는 median 값 적용
        else {
          // this.startLabel.push("Min");
          // this.endLabel.push("Max");
        }
      });
    },
    setUniformDistribution() {
      this.setUniformLabel();
      // 초기화 (push 하기 전)
      this.startValues = [];
      this.endValues = [];
      // loop
      let index = 0;
      this.columns.forEach(element => {
        // 관찰 변수일 경우에는 min max 값 적용
        if (element == this.observedVariable) {
          this.startValues.push(this.summarizedInfo["interval"][element]["min"]);
          this.endValues.push(this.summarizedInfo["interval"][element]["max"]);
        }
        // 그 외 변수들일 경우에는 median 값 적용
        else {
          // category 일 경우 '일단' category라는 string 값 넣어둠
          if (this.summarizedInfo["datatype"]["type"][index] == "category") {
            this.startValues.push(0);
            // this.endValues.push(0);
          } else {
            this.startValues.push(this.summarizedInfo["numeric"][element]["median"]);
            // this.endValues.push(this.summarizedInfo["numeric"][element]["median"]);
          }
        }
        index++;
      });
    },
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

    featureFocused(type, column) {
      this.focusedFeature = column;
      this.focusedStatistic = null;
      if (type == "start") {
        this.focusedTextField = this.startValues;
      } else {
        this.focusedTextField = this.endValues;
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
    // 일단 임의 값 넣어두기
    this.columns.forEach(element => {
      // 관찰 변수일 경우에는 min max 값 적용

      this.startLabel.push("");
      this.endLabel.push("");
    });
  }
};
</script>
<style scoped>
.centered-input input {
  text-align: center;
}
</style>
