<template>
  <v-dialog v-model="dialog" width="1000px">
    <!-- <v-btn @click="ndTest()"></v-btn> -->
    <!-- <v-btn @click="rangeValues['start'].push(1)">hello</v-btn> -->
    <v-container fluid class="pa-0">
      <v-card rounded>
        <v-row class="ma-0 ">
          <v-spacer></v-spacer>
          <v-btn x-small min-width="20" min-height="30" @click="closeModal"
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
          <v-tab :disabled="stepOneFlag != true">2. Create Samples </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <!-- 1. Input/target -->
          <v-tab-item>
            <!-- <v-card-subtitle class="red--text"
              >현재는 관찰변수로 CRIM만 지정 가능합니다.</v-card-subtitle
            > -->
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
                    <v-btn color="primary" @click="stepOneFinished()">Next</v-btn>
                  </v-card-actions>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
          <!-- 2.Simulation -->
          <v-tab-item>
            <v-container class="px-10">
              <v-subheader>
                Create Sample Values
              </v-subheader>
              <v-row align="center">
                <v-col cols="4">
                  <v-subheader> If leave Fixed Value blank, regard it as </v-subheader></v-col
                ><v-col cols="2">
                  <v-select
                    disabled
                    :items="numericStatistics"
                    label="Mode"
                    v-model="fixedValueDefault"
                  ></v-select
                ></v-col>
              </v-row>
              <v-row class="py-5" justify="center">
                <v-col>
                  <v-card width="100%" min-height="300px" elevation="0">
                    <v-card outlined min-height="400" class="rangeCard">
                      <!-- table -->
                      <v-simple-table>
                        <template>
                          <thead>
                            <tr>
                              <th class="thStyle">Observe</th>
                              <th class="thStyle">Feature Name</th>
                              <th class="thStyle">Sample Type</th>
                              <th class="thStyle">Distribution Type</th>
                              <th class="thStyle" style="width:300px">Range</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                              v-for="(column, columnIndex) in inputs"
                              v-show="previousPage - 1 < columnIndex && columnIndex < currentPage"
                              :key="columnIndex"
                            >
                              <!-- 1. Observe -->
                              <td>
                                <v-tooltip bottom>
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-row align="center" justify="center">
                                      <v-col cols="1">
                                        <v-icon
                                          v-bind="attrs"
                                          v-on="on"
                                          v-if="isObservedVariable(column)"
                                          >mdi-check</v-icon
                                        >
                                      </v-col>
                                    </v-row>
                                  </template>
                                  <span>Observed Variable</span>
                                </v-tooltip>
                              </td>
                              <!-- 2. Feature 명 -->
                              <td>
                                <v-col cols="" class="pl-0" style="text-align:center">
                                  <v-card-text>{{ column }}</v-card-text></v-col
                                >
                              </td>
                              <!-- 3. Samples (Fixed/Random) -->
                              <td justify="center" align="center">
                                <v-row>
                                  <v-col offset="2" class="px-0">
                                    <v-radio-group
                                      dense
                                      hide-details
                                      v-model="samplesRadioModel[columnIndex]"
                                    >
                                      <v-radio
                                        v-for="(radio, radioIndex) in samplesRadioLabel"
                                        :key="radioIndex"
                                        :label="radio"
                                        @change="sampleChange(radioIndex, columnIndex)"
                                      ></v-radio>
                                    </v-radio-group>
                                  </v-col>
                                </v-row>
                              </td>

                              <!-- 3. Distribution (Enter the Value/Normal Distribution) -->
                              <td>
                                <v-row justify="center" align="center">
                                  <v-col offset="3" class="px-0">
                                    <v-radio-group
                                      dense
                                      hide-details
                                      v-model="distributionRadioModel[columnIndex]"
                                    >
                                      <v-radio
                                        v-for="(radio, radioIndex) in distributionRadioLabel"
                                        :key="radioIndex"
                                        :label="radio"
                                        :disabled="samplesRadioModel[columnIndex] == 0"
                                        @change="distributionChange(radioIndex, columnIndex)"
                                      ></v-radio>
                                    </v-radio-group>
                                  </v-col>
                                </v-row>
                              </td>
                              <!-- 4. Range -->
                              <td>
                                <!-- RangedFixed -->
                                <v-row
                                  v-if="samplesRadioModel[columnIndex] == 0"
                                  justify="center"
                                  align="center"
                                >
                                  <v-col cols="6">
                                    <v-text-field
                                      clearable
                                      hide-details
                                      dense
                                      label="Fixed Value"
                                      v-model="fixedValues[columnIndex]"
                                      @click="
                                        openHelper(column, columnIndex);
                                        getHelperValues(column);
                                        setTargetTextField(columnIndex, 'fixed');
                                      "
                                    ></v-text-field>
                                  </v-col>
                                </v-row>
                                <!-- RangedRandom -->
                                <v-row justify="center" align="center" v-else>
                                  <v-col cols="" align-self="center" class="">
                                    <v-text-field
                                      hide-details
                                      label="Min"
                                      class="mt-0"
                                      v-model="rangeValues['start'][columnIndex]"
                                      clearable
                                      dense
                                      style="text-align:right"
                                      @click="
                                        openHelper(column, columnIndex);
                                        getHelperValues(column);
                                        setTargetTextField(columnIndex, 'start');
                                      "
                                    ></v-text-field>
                                  </v-col>
                                  <v-col cols="" class="">
                                    <v-text-field
                                      clearable
                                      dense
                                      hide-details
                                      v-model="rangeValues['end'][columnIndex]"
                                      label="Max"
                                      class="mt-0"
                                      @click="
                                        openHelper(column, columnIndex);
                                        getHelperValues(column);
                                        setTargetTextField(columnIndex, 'end');
                                      "
                                    ></v-text-field>
                                  </v-col>
                                </v-row>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>

                      <!-- range helper -->
                      <v-navigation-drawer
                        :hide-overlay="true"
                        v-model="drawer"
                        stateless
                        absolute
                        bottom
                        temporary
                        overlay-opacity="0.1"
                      >
                        <v-card
                          width="100%"
                          height="100%"
                          color="rgba(80, 79, 79, 0.817)"
                          dark
                          class=""
                          :disabled="helperStatus"
                        >
                          <v-container
                            ><v-row justify="end">
                              <v-btn
                                @click="drawer = !drawer"
                                color="rgba(80, 79, 79, 0.817)"
                                dark
                                x-small
                                light
                                >X</v-btn
                              ></v-row
                            >
                            <v-row align="center" justify="center">
                              <v-card-text style="text-align:center"
                                >Range Setting Helper</v-card-text
                              >
                              <v-card-text style="text-align:center" class="subheading pt-0">
                                {{ helperColumn }}</v-card-text
                              >
                              <v-tabs
                                centered
                                v-model="tab_rangeMethod"
                                dark
                                background-color="rgba(80, 79, 79, 0.817)"
                                light
                              >
                                <v-tab class="vtab">Statistics</v-tab>
                                <!-- <v-tab class="vtab">Normal Distribution </v-tab> -->
                              </v-tabs>
                              <v-container>
                                <v-tabs-items v-model="tab_rangeMethod">
                                  <!-- Statistics -->
                                  <v-tab-item>
                                    <!-- numeric -->
                                    <div v-if="isNumeric()">
                                      <v-row
                                        align="center"
                                        justify="center"
                                        v-for="(statistic, index) in numericStatistics"
                                        :key="index"
                                      >
                                        <v-col offset="2">
                                          <v-tooltip left open-delay="250">
                                            <template v-slot:activator="{ on, attrs }">
                                              <v-chip
                                                v-bind="attrs"
                                                v-on="on"
                                                label
                                                dark
                                                outlined
                                                @mouseover="setStatisticValue(statistic)"
                                                @click="setStatisticValue(statistic), closeHelper()"
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
                                    </div>
                                    <!-- category -->
                                    <div v-else>
                                      <v-row
                                        align="center"
                                        justify="center"
                                        v-for="(statistic, index) in categoryStatistics"
                                        :key="index"
                                      >
                                        <v-col offset="2">
                                          <v-tooltip left open-delay="250">
                                            <template v-slot:activator="{ on, attrs }">
                                              <v-chip
                                                dark
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
                                          <v-card-text class="py-0">0</v-card-text></v-col
                                        >
                                      </v-row>
                                    </div>
                                  </v-tab-item>
                                  <!-- Distribution -->
                                  <v-tab-item class="transparent-body">
                                    <v-row
                                      align="center"
                                      justify="center"
                                      v-for="(info, index) in distribution_info"
                                      :key="index"
                                    >
                                      <v-col offset="2">
                                        <v-tooltip left open-delay="250">
                                          <template v-slot:activator="{ on, attrs }">
                                            <v-chip
                                              v-bind="attrs"
                                              v-on="on"
                                              label
                                              outlined
                                              dark
                                              @mouseover="setDistributionValue(info.toLowerCase())"
                                              @click="setDistributionValue(info.toLowerCase())"
                                              >{{ info }}</v-chip
                                            >
                                          </template>
                                          <span>Click to Get Value</span>
                                        </v-tooltip>
                                      </v-col>
                                      <v-col cols="">
                                        <v-card-text class="py-0" v-if="helperColumn != null">
                                          {{ randomRange[helperColumn][info.toLowerCase()] }}
                                        </v-card-text></v-col
                                      >
                                    </v-row>
                                  </v-tab-item>
                                </v-tabs-items>
                              </v-container>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-navigation-drawer>
                    </v-card>
                    <v-pagination
                      class="mt-4 mb-4"
                      v-model="page"
                      :length="paginationLength"
                      circle
                    ></v-pagination>
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
      inputs: null,
      targets: null,
      stepOneFlag: null,
      fixedValueDefault: null,
      // drawer
      drawer: false,
      // radio
      distributionRadioModel: [],
      distributionRadioLabel: ["Uniform", "Normal"],
      samplesRadioModel: [],
      samplesRadioLabel: ["Fixed Value", "Random Value"],
      // range helper
      helperStatus: true,
      helperColumn: null,
      helperValues: [],
      // range values(v-model)
      rangeValues: { start: [], end: [] },
      fixedValues: [],
      selectedStatistic: [],
      userInput: null,
      values: [],

      distributionSelected: null,
      // tab
      tab: 0,
      tab_rangeMethod: 0,

      // page
      page: 1,
      length: 2,
      model: 1,

      // v-for
      numericStatistics: ["Min", "Max", "Mean", "Mode", "Median"],
      categoryStatistics: ["Mode", "Median"],
      distribution_info: ["Min", "Max"],

      chipColors: [],

      // focused info
      focusedIndex: null,
      focusedTextField: null,

      select: { method: "", explanation: "" },

      dialog: false,
      disabledProps: {
        disabled: true
      },

      hideDetailsProps: {
        "hide-details": true
      }
    };
  },
  watch: {},
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,
      observedVariable: state => state.simulationData.observedVariable,
      summarizedInfo: state => state.initialData.summarizedInfo,
      randomRange: state => state.initialData.randomRange,
      columns: state => state.initialData.columns
    }),

    // ...mapGetters("initialData", ["columns"]),
    // page
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
    ...mapMutations("simulationResult", ["saveGraphSources"]),
    ...mapActions("initialData", ["loadRandomData"]),
    ...mapMutations("simulationData", ["saveSimulationMethod"]),
    sampleChange(radioIndex, columnIndex) {
      //Random value
      if (radioIndex == 1) {
        Vue.set(this.distributionRadioModel, columnIndex, 0);
      } else {
        Vue.set(this.distributionRadioModel, columnIndex, null);
      }
    },
    // hello() {
    //   Vue.set(this.rangeValues['start'], 0, 1);
    // },

    distributionChange(radioIndex, columnIndex) {
      if (radioIndex == 1) {
        this.helperColumn = this.columns[columnIndex];
        Vue.set(this.rangeValues["start"], columnIndex, this.randomRange[this.helperColumn]["min"]);
        Vue.set(this.rangeValues["end"], columnIndex, this.randomRange[this.helperColumn]["max"]);
      } else {
        Vue.set(this.rangeValues["start"], columnIndex, null);
        Vue.set(this.rangeValues["end"], columnIndex, null);
      }
    },
    isObservedVariable(column) {
      if (column == this.observedVariable) return true;
    },
    getDataType(column) {
      return this.summarizedInfo["datatype"][column];
    },
    isNumeric() {
      let dataType = this.getDataType(this.helperColumn);
      if (dataType == "numeric") {
        return true;
      } else return false;
    },
    openHelper(column, columnIndex) {
      this.helperColumn = column;
      this.helperColumnIndex = columnIndex;
      this.helperStatus = false; //helper 활성화
      this.drawer = true; //helper 활성화
    },
    closeHelper() {
      this.drawer = false;
    },
    getHelperValues(column) {
      // category
      if (this.summarizedInfo["datatype"][column] == "category") {
        this.helperValues = { Median: 0, Mode: 0 };
        return this.helperValues;
      }
      // numeric
      else {
        let min = this.summarizedInfo["interval"][column]["min"];
        let max = this.summarizedInfo["interval"][column]["max"];
        let mean = this.summarizedInfo["numeric"][column]["mean"];
        let mode = this.summarizedInfo["numeric"][column]["mode"];
        let median = this.summarizedInfo["numeric"][column]["median"];
        // 배열에 삽입해서 반환
        this.helperValues = { Min: min, Max: max, Mean: mean, Median: median, Mode: mode };
        return this.helperValues;
      }
    },
    setTargetTextField(columnIndex, textFieldType) {
      // 대상 index 설정
      this.focusedIndex = columnIndex;
      // 대상 field 설정 (range start/ ranged end/fixed)
      if (textFieldType == "start") {
        this.focusedTextField = this.rangeValues["start"];
      } else if (textFieldType == "end") {
        this.focusedTextField = this.rangeValues["end"];
      } else {
        this.focusedTextField = this.fixedValues;
      }
    },
    setStatisticValue(statistic) {
      Vue.set(this.focusedTextField, this.focusedIndex, this.helperValues[statistic]);
    },
    setDistributionValue(info) {
      Vue.set(this.focusedTextField, this.focusedIndex, this.randomRange[this.helperColumn][info]);
    },

    toggleTooltip(event) {
      if (event == "blur") {
        this.tooltipStatus = false;
      } else {
        this.tooltipStatus = true;
      }
    },

    stepOneFinished() {
      this.stepOneFlag = true;
      this.tab = 1;
      eventBus.$emit("simulationColumnChecked", true);
    },
    stepTwoFinished() {
      let rangeInfo = {};

      this.samplesRadioModel.forEach((element, index) => {
        let featureName = this.columns[index];
        let rangeMin = this.rangeValues["start"][index];
        let rangeMax = this.rangeValues["end"][index];
        //fixed value
        if (element == 0) {
          //fixed value (null)
          if (this.fixedValues[index] == null) {
            if ("numeric" == this.summarizedInfo["datatype"][featureName]) {
              rangeInfo[featureName] = {
                method: "fixed",
                interval: { fixedValue: this.summarizedInfo["numeric"][featureName]["mode"] }
              };
            } else {
              rangeInfo[featureName] = {
                method: "fixed",
                interval: { fixedValue: 0 }
              };
            }
          }
          //fixed value (has value)
          else {
            rangeInfo[featureName] = {
              method: "fixed",
              interval: { fixedValue: this.fixedValues[index] }
            };
          }
        }
        //random value
        else {
          rangeInfo[featureName] = { interval: { min: rangeMin, max: rangeMax } };
          if (this.distributionRadioModel[index] == 0) rangeInfo[featureName]["method"] = "uniform";
          else rangeInfo[featureName]["method"] = "normal";
        }
        delete rangeInfo["MEDV"];
      });
      console.log(rangeInfo);
      // axios
      let path = "http://localhost:5000/runSimulation";

      this.$axios({
        method: "post",
        url: path,
        data: {
          observedVariable: this.observedVariable,
          rangeInfo: rangeInfo,
          target: this.targets[0]
        }
      })
        .then(res => {
          this.saveGraphSources(res.data); // 그래프 값 저장
          eventBus.$emit("updateChart", true);
          console.log(res);
        })
        .catch(error => {
          console.error(error);
        });

      // customzied
      this.$router.push({ name: "simulationResult" });
    },
    getCaseFeatures(caseID) {
      // axios
      let path = "http://localhost:5000/getCaseFeatures";

      this.$axios({
        method: "post",
        url: path,
        data: {
          caseID: caseID
        }
      })
        .then(res => {
          // console.log(res.data);
          this.inputs = res.data.inputs;
          this.targets = res.data.targets;
        })
        .catch(error => {
          console.error(error);
        });
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
    closeModal() {
      this.dialog = false;
    }
  },
  components: {
    InputColumnList,
    TargetColumnList
  },
  created() {
    eventBus.$on("openSimulation", caseID => {
      // this.getCaseFeatures(caseID);
      this.dialog = true;
    });
    // radio button default 를 0으로
    this.columns.forEach(element => {
      this.samplesRadioModel.push(0);
    });
    //rand range
    // this.loadRandomData();
  }
};
</script>
<style scoped>
.centered-input input {
  text-align: center !important;
}
.rangeCard {
  position: relative;
}
.rangeHelper {
  position: absolute;

  top: 120px;
  right: -200px;
  /* background-color: rgba(80, 79, 79, 0.817);:  */
}
.vtab {
  font-size: 5px !important;
}
.v-tabs-bar__content {
  background-color: grey !important;
}
.v-tabs-items {
  background: transparent !important;
}
.thStyle {
  text-align: center !important;
}
</style>
