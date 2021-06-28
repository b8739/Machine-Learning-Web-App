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
            ></v-text-field>
          </v-col>
        </v-row>
        <v-tabs centered v-model="tab">
          <v-tab>1. Input/target</v-tab>
          <v-tab>2. Simulation Method</v-tab>
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
              <v-row class="py-5">
                <v-col>
                  <v-card width="100%" min-height="300px" elevation="0">
                    <v-select
                      v-model="select"
                      :items="items"
                      return-object
                      label="Randomize Methods"
                      persistent-hint
                      dense
                      :hint="`${select.explanation}`"
                      item-text="method"
                    ></v-select>
                    <div v-if="select.method == 'Customized Setting'">
                      <v-row
                        v-for="(column, index) in columns"
                        :key="index"
                        justify="center"
                        class="mt-5"
                      >
                        <v-col cols="2">
                          <v-card-text>{{ column }}</v-card-text></v-col
                        >
                        <v-col cols="2">
                          <v-text-field hide-details dense clearable outlined></v-text-field
                        ></v-col>
                        <v-icon x-small>mdi-tilde</v-icon>
                        <v-col cols="2">
                          <v-text-field hide-details dense clearable outlined></v-text-field
                        ></v-col>
                      </v-row>
                    </div>
                  </v-card>
                </v-col>
              </v-row>

              <!-- actions 2-->
              <v-row>
                <v-col cols="12">
                  <v-card-actions align-self="end">
                    <v-btn color="primary" @click="tab = 0">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="stepTwoFinished">Next</v-btn>
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
      model: 1,

      tab: 0,
      select: { method: "", explanation: "" },
      items: [
        {
          method: "Default Setting",
          explanation: "Y 변수에는 (설명), X 그룹의 변수들은 (설명)"
        },
        {
          method: "Customized Setting",
          explanation: "사용자가 직접 난수 (Random Number)가 생성될 구간을 설정합니다."
        }
      ],
      dialog: false,

      hideDetailsProps: {
        "hide-details": true
      },
      chosenSnippet: null
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    }),
    ...mapGetters("initialData", ["columns"])
  },
  methods: {
    ...mapMutations("simulationData", ["saveSimulationMethod"]),
    stepOneFinished() {
      this.tab = 1;
      eventBus.$emit("simulationColumnChecked", true);
    },
    stepTwoFinished() {
      this.saveSimulationMethod(this.select.method);
      this.$router.push({ name: "simulationResult" });
    },

    snippetClicked(snippet) {
      this.chosenSnippet = snippet;
    },
    getItems(index) {
      if (index == 0) {
        return this.tableList;
      }

      // else if (indexOfFormFields == 1) {
      //   return ;
      // } else if (indexOfFormFields == 2) {
      //   return ;
      // } else if (indexOfFormFields == 3) {
      //   return ;
      // } else {
      //   return ;
      // }
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
      this.saveSnippet(this.chosenSnippet);
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
