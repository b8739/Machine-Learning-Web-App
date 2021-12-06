<template>
  <v-dialog v-model="dialog" width="1000px">
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
          <v-tab :disabled="isObVariableChecked == false">2. Create Samples </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <!-- 1. Input/target -->
          <v-tab-item>
            <!-- <v-card-subtitle class="red--text"
              >현재는 관찰변수로 CRIM만 지정 가능합니다.</v-card-subtitle
            > -->
            <v-container>
              {{ obVariable }}
              <!-- {{ finalObVariables }} -->
              <v-row>
                <!-- <v-card-text>Select the input(s) and target features you want to use.</v-card-text> -->
                <v-col cols="12">
                  <v-row v-for="(column, columnIndex) in inputs" :key="columnIndex">
                    <v-col>
                      <v-subheader>{{ column }}</v-subheader></v-col
                    >
                    <v-col>
                      <v-checkbox v-model="obVariable[column]" hide-details dense></v-checkbox
                    ></v-col>
                  </v-row>
                </v-col>
                <!-- actions 1-->
                <v-col cols="12">
                  <v-card-actions>
                    <v-btn color="primary" @click="tab = 0">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="obVariableChecked()">Next</v-btn>
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
                ><v-col cols="2"> <v-select disabled label="Mode"></v-select></v-col>
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
                              :key="columnIndex"
                              v-show="previousPage - 1 < columnIndex && columnIndex < currentPage"
                            >
                              <!-- 1. Observe -->
                              <td>
                                <v-tooltip bottom>
                                  <template v-slot:activator="{ on, attrs }">
                                    <v-row align="center" justify="center">
                                      <v-col cols="1">
                                        <v-icon v-bind="attrs" v-on="on">mdi-check</v-icon>
                                        <!-- v-if="isObservedVariable(column)" -->
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
                                    <v-radio-group dense hide-details>
                                      <!-- <v-radio :label="radio"></v-radio> -->
                                    </v-radio-group>
                                  </v-col>
                                </v-row>
                              </td>

                              <!-- 3. Distribution (Enter the Value/Normal Distribution) -->
                              <td>
                                <v-row justify="center" align="center">
                                  <v-col offset="3" class="px-0">
                                    <v-radio-group dense hide-details>
                                      <!-- <v-radio :label="radio"></v-radio> -->
                                    </v-radio-group>
                                  </v-col>
                                </v-row>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
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
                    <v-btn color="primary">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary">Run Simulation</v-btn>
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

export default {
  data() {
    return {
      dialog: false,
      obVariable: {},
      // tab
      tab: 0,
      inputs: ["CRIM", "ZN"],
      targets: ["CRIM", "ZN"],
      // page
      page: 1,
      length: 2,
      model: 1,
      columns: [1, 2, 3]
    };
  },

  computed: {
    finalObVariables() {
      let vm = this;
      return Object.keys(this.obVariable).map(function(col) {
        if (vm.obVariable[col]) {
          return col;
        }
      });
    },
    isObVariableChecked() {
      if (this.finalObVariables.length > 1) {
        return true;
      } else return false;
    },
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
    obVariableChecked() {
      this.tab = 1;
    },
    closeModal() {
      this.dialog = false;
    }
  },
  created() {
    eventBus.$on("openSimulation", caseID => {
      // this.getCaseFeatures(caseID);
      this.dialog = true;
    });
  }
};
</script>
