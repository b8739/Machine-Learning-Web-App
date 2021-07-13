<template>
  <v-dialog v-model="dialog" width="1000">
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

                      <v-simple-table>
                        <template v-slot:default>
                          <thead>
                            <tr>
                              <th>Observe</th>
                              <th>Feature Name</th>
                              <th>Method</th>
                              <th style="width:200px">Range Min</th>
                              <th style="width:200px">Range Max</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                              v-for="(column, columnIndex) in columns"
                              v-show="previousPage - 1 < columnIndex && columnIndex < currentPage"
                              :key="columnIndex"
                            >
                              <td>
                                <div style="width:50px">
                                  <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                      <v-icon
                                        class="ml-7"
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
                              </td>
                              <td>
                                <v-col cols="" class="pl-0" style="text-align:center">
                                  <v-card-text>{{ column }}</v-card-text></v-col
                                >
                              </td>
                              <td>
                                <v-col cols="" class="px-0">
                                  <v-radio-group hide-details v-model="radioModel[columnIndex]">
                                    <v-radio
                                      v-for="(radio, radioIndex) in radioLabels"
                                      :key="radioIndex"
                                      :label="radio"
                                      @change="radio_nd(column, columnIndex)"
                                    ></v-radio> </v-radio-group
                                ></v-col>
                              </td>
                              <td>
                                <v-col cols="" align-self="center">
                                  <v-text-field
                                    :disabled="radioModel[columnIndex] == 1"
                                    style="text-align:right"
                                    @click="
                                      openHelper(column, columnIndex);
                                      getHelperValues(column);
                                      setTargetTextField(columnIndex, 'start');
                                    "
                                    hide-details
                                    label="Min"
                                    class="mt-0 pt-0"
                                    v-model="rangeValues['start'][columnIndex]"
                                  ></v-text-field>
                                </v-col>
                              </td>

                              <td>
                                <v-col cols="">
                                  <v-text-field
                                    :disabled="radioModel[columnIndex] == 1"
                                    hide-details
                                    @click="
                                      openHelper(column, columnIndex);
                                      getHelperValues(column);
                                      setTargetTextField(columnIndex, 'end');
                                    "
                                    v-model="rangeValues['end'][columnIndex]"
                                    label="Max"
                                    class="mt-0 pt-0"
                                  ></v-text-field>
                                </v-col>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>

                      <!-- range helper -->
                      <v-navigation-drawer v-model="drawer" absolute bottom temporary>
                        <v-card
                          max-width="250"
                          min-height="300"
                          color="rgba(80, 79, 79, 0.817)"
                          dark
                          class=""
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
import NormalDistribution from "normal-distribution";
import { eventBus } from "@/main";
import InputColumnList from "@/components/simulation/columnList/InputColumnList.vue";
import TargetColumnList from "@/components/simulation/columnList/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      // drawer
      drawer: false,
      // radio
      radioModel: [],
      // range helper
      helperStatus: true,
      helperColumn: null,
      helperValues: [],
      // range values(v-model)
      rangeValues: { start: [], end: [] },
      selectedStatistic: [],
      userInput: null,
      values: [],

      distributionSelected: null,
      // tab
      tab: 1,
      tab_rangeMethod: 0,

      // page
      page: 1,
      length: 2,
      model: 1,

      // v-for
      numericStatistics: ["Min", "Max", "Mean", "Mode", "Median"],
      categoryStatistics: ["Mode", "Median"],
      distribution_info: ["Min", "Max"],
      radioLabels: ["Manually", "Normal Distribution"],
      chipColors: [],

      // focused info
      focusedIndex: null,
      focusedTextField: null,

      select: { method: "", explanation: "" },

      dialog: true,
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
      randomRange: state => state.initialData.randomRange
    }),

    ...mapGetters("initialData", ["columns"]),
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
    // hello() {
    //   Vue.set(this.rangeValues['start'], 0, 1);
    // },
    ...mapActions("initialData", ["loadRandomData"]),
    ...mapMutations("simulationData", ["saveSimulationMethod"]),
    radio_nd(column, columnIndex) {
      this.helperColumn = column;
      Vue.set(this.rangeValues["start"], columnIndex, this.randomRange[this.helperColumn]["min"]);
      Vue.set(this.rangeValues["end"], columnIndex, this.randomRange[this.helperColumn]["max"]);
    },
    isObservedVariable(column) {
      if (column == this.observedVariable) return true;
    },
    getDataType(columnIndex) {
      return this.summarizedInfo["datatype"]["type"][columnIndex];
    },
    isNumeric() {
      let dataType = this.getDataType(this.helperColumnIndex);
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
        this.focusedTextField = this.rangeValues["start"];
      } else {
        this.focusedTextField = this.rangeValues["end"];
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
      this.tab = 1;
      eventBus.$emit("simulationColumnChecked", true);
    },
    stepTwoFinished() {
      // this.saveSimulationMethod(this.select.method);
      this.$router.push({ name: "simulationResult" });
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
    eventBus.$on("openSimulation", dialogStatus => {
      this.dialog = dialogStatus;
    });
    // radio button default 를 0으로
    this.columns.forEach(element => {
      this.radioModel.push(0);
    });
    //rand range
    this.loadRandomData();
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
</style>
