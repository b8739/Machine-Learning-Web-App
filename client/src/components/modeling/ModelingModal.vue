<template>
  <v-dialog v-model="dialog" max-width="810">
    <v-container fluid class="pa-0">
      <v-card max-width="900" min-height="700" rounded>
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
          <v-tab>3. Normalization</v-tab>
          <v-tab>4. Snippet</v-tab>
          <v-tab>5. Weights</v-tab>
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
                  <InputColumnList />
                </v-col>
                <v-col cols="6">
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
          <!-- 3.Normalization -->
          <v-tab-item>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-card-subtitle>Normalization</v-card-subtitle>
                </v-col>
              </v-row>
              <v-row v-for="(dataType, index) in dataTypes" :key="index" no-gutters>
                <v-col offset="1" cols="3">
                  <v-card-text class="pt-5">
                    {{ dataType }}
                  </v-card-text>
                </v-col>

                <v-col cols="4">
                  <v-checkbox label="Fit"></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox label="Transform"></v-checkbox>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-card-actions>
                    <v-btn color="primary" @click="tab = 1">Previous</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="tab = 3">Next</v-btn>
                  </v-card-actions></v-col
                >
              </v-row>
            </v-container>
          </v-tab-item>
          <!-- 4.Snippet -->
          <v-tab-item>
            <v-card elevation="0" min-height="393px">
              <v-list outlined selectable>
                <v-list-group :value="true" no-action>
                  <template v-slot:activator>
                    <v-list-item-icon>
                      <v-icon>mdi-arrow-decision-auto</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>Snippets</v-list-item-title>
                    </v-list-item-content>
                  </template>
                  <v-list-item-group v-model="model">
                    <v-list-item
                      v-for="(snippet, index) in snippets"
                      :key="index"
                      @click="snippetClicked(snippet)"
                    >
                      <v-list-item-title v-text="snippet"></v-list-item-title>

                      <v-list-item-icon>
                        <v-icon v-text="icon"></v-icon>
                      </v-list-item-icon>
                    </v-list-item>
                  </v-list-item-group>
                </v-list-group>
              </v-list>
            </v-card>
            <v-card-actions>
              <v-btn color="primary" @click="tab = 2">Previous</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="createModel">Create</v-btn>
            </v-card-actions>
          </v-tab-item>
          <!-- 5.Weights -->
          <v-tab-item> </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </v-dialog>
</template>
<script>
import { eventBus } from "@/main";
import InputColumnList from "@/components/modeling/columnList/InputColumnList.vue";
import TargetColumnList from "@/components/modeling/columnList/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      model: 1,
      tab: null,
      dataTypes: ["X Train Data", "X Test Data", "Y Train Data", "Y Test Data"],
      dialog: false,
      formFields: [1, 2, 3],
      dataInfoLabels: ["Dataset", "Dataset Version", "Subset"],
      dataTypelabels: ["Training", "Validation", "Test"],
      datasetRatio: ["60%", "20%", "20%"],
      snippets: ["XGBoost", "Random Forest", "SVR"],
      hideDetailsProps: {
        "hide-details": true
      },
      chosenSnippet: null
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    })
  },
  methods: {
    ...mapMutations("modelingData", ["saveSnippet"]),
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
