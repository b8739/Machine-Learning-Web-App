<template>
  <v-dialog v-model="dialog" max-width="700">
    <v-container fluid class="pa-0">
      <v-card max-width="800" min-height="700" rounded>
        <v-row class="ma-0">
          <v-spacer></v-spacer>
          <v-btn x-small min-width="20" min-height="30" @click="closeStepper"
            ><v-icon small>mdi-close</v-icon>
          </v-btn>
        </v-row>
        <v-row justify="center" class="ma-0">
          <v-card-title class="pa-0"> Modeling Wizard</v-card-title>
        </v-row>
        <v-divider></v-divider>
        <v-row justify="center" class="ma-0">
          <v-col cols="8">
            <v-text-field
              hide-details
              outlined
              label="Experiment Name"
              placeholder="Experiment Name"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-tabs centered v-model="tab">
          <v-tab>1. Dataset</v-tab>
          <v-tab>2. Input/target</v-tab>
          <v-tab>3. Snippet</v-tab>
          <v-tab>4. Weights</v-tab>
        </v-tabs>
        <!-- 1. dataset -->
        <v-tabs-items v-model="tab">
          <v-tab-item>
            <v-row justify="center" no-gutters dense>
              <v-col cols="7"><v-card-text>Select the data you want to use</v-card-text></v-col>
              <v-col
                cols="7"
                v-for="(formField, indexOfFormFields) in formFields"
                :key="indexOfFormFields"
              >
                <v-autocomplete
                  outlined
                  clearable
                  dense
                  :label="dataInfoLabels[indexOfFormFields]"
                  :items="getItems(indexOfFormFields)"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row justify="center" no-gutters dense>
              <v-col cols="1"><v-divider vertical></v-divider></v-col>
              <v-col cols="6">
                <v-autocomplete
                  v-for="(formField, indexOfFormFields) in formFields"
                  :key="indexOfFormFields"
                  outlined
                  clearable
                  dense
                  no-data-text=""
                  v-bind="hideDetails(indexOfFormFields)"
                  :label="dataTypelabels[indexOfFormFields]"
                  :placeholder="datasetRatio[indexOfFormFields]"
                  :items="datasetRatio[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-col cols="10">
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="tab = 1">Next</v-btn>
              </v-card-actions>
            </v-col>
          </v-tab-item>
          <!-- 2. Input/target -->
          <v-tab-item>
            <v-container>
              <v-row>
                <v-card-text>Select the input(s) and target features you want to use.</v-card-text>
                <v-col cols="6">
                  <v-card-subtitle>Input</v-card-subtitle>
                  <InputColumnList />
                </v-col>
                <v-col cols="6">
                  <v-card-subtitle>Target</v-card-subtitle>
                  <TargetColumnList />
                </v-col>
                <v-col cols="12">
                  <v-card-actions>
                    <v-btn color="primary" @click="tab = 0">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="sendFeatures">Next</v-btn>
                  </v-card-actions>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
          <!-- 3.Snippet -->
          <v-tab-item>
            <v-card elevation="0" min-height="393px">
              <v-list outlined dense>
                <v-list-group>
                  <template v-slot:activator>
                    <v-list-item-icon>
                      <v-icon>mdi-arrow-decision-auto</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Select Problem Type</v-list-item-title>
                  </template>
                  <v-list-item v-for="(snippet, index) in snippets" :key="index">
                    {{ snippet }}
                  </v-list-item>
                </v-list-group>
              </v-list>
            </v-card>
            <v-card-actions>
              <v-btn color="primary" @click="tab = 2">Previous</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="createModel">Create</v-btn>
            </v-card-actions>
          </v-tab-item>
          <!-- 3.Weights -->
          <v-tab-item> </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </v-dialog>
</template>
<script>
import { eventBus } from "@/main";
import InputColumnList from "@/components/modeling/InputColumnList.vue";
import TargetColumnList from "@/components/modeling/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      tab: null,
      dialog: false,
      formFields: [1, 2, 3],
      dataInfoLabels: ["Dataset", "Dataset Version", "Subset"],
      dataTypelabels: ["Training", "Validation", "Test"],
      datasetRatio: ["80%", "0%", "20%"],
      snippets: ["XGBoost", "Random Forest", "SVR"],
      hideDetailsProps: {
        "hide-details": true
      }
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    })
  },
  methods: {
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
      eventBus.$emit("createModel", true);
    }
  },
  components: {
    InputColumnList,
    TargetColumnList
  },
  created() {
    eventBus.$on("openModeling", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>
