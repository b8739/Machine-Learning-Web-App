<template>
  <v-card>
    <v-navigation-drawer v-model="drawer" absolute height="100vh" permanent class="mt-1">
      <!-- :mini-variant.sync="mini" -->
      <v-list-item class="px-2">
        <v-list-item-title>Modeling Setting</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>
      <v-list dense>
        <v-list-group prepend-icon="mdi-database" :value="true" class="my-5">
          <template v-slot:activator>
            <v-list-item-title>Dataset Version</v-list-item-title>
          </template>
          <v-list-item
            link
            v-for="(dataInfo, indexOfDataInfo) in dataInfoLabels"
            :key="indexOfDataInfo"
          >
            <v-list-item-content>
              <v-select
                class="mt-3"
                outlined
                clearable
                hide-details
                dense
                label="Select Datatable"
                :items="gridList"
                item-text="name"
                item-value="id"
                v-model="modelingDataset"
              ></v-select>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>

        <v-divider></v-divider>
        <!-- splitting data -->
        <v-list-group prepend-icon="mdi-arrow-decision-outline" :value="true" class="mt-5">
          <!-- 1st Level -->
          <template v-slot:activator>
            <v-list-item-title>Data Split</v-list-item-title>
          </template>
          <!-- 2nd Level -->
          <v-list-group sub-group :value="true" class="mb-5">
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Extract Validation Set</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item>
              <!-- <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-header> Extract</v-expansion-panel-header>
                  <v-expansion-panel-content> hi</v-expansion-panel-content>
                </v-expansion-panel></v-expansion-panels
              > -->
              <v-container>
                <v-row>
                  <!-- <v-col cols="3"> <v-subheader>Validation:</v-subheader></v-col> -->
                  <v-col>
                    <v-text-field
                      hide-details
                      :rules="[rules.required]"
                      suffix="%"
                      type="number"
                      dense
                      outlined
                      label="Validation"
                      clearable
                      v-model="validationSet"
                    ></v-text-field
                  ></v-col>
                  <!-- <v-col cols="9">
                    <v-row>
                      <v-card-text class="body-2 font-weight-medium pa-0">
                        Total Rows: {{ datasetSize }}</v-card-text
                      >
                    </v-row>
                    <v-row justify="center" align="center">
                      <v-col cols="4" class="px-0"
                        ><v-card-text class="body-2 pa-0">From</v-card-text>
                      </v-col>
                      <v-col cols="8" class="px-0"
                        ><v-text-field
                          v-model="validationStartIndex"
                          hide-details
                          dense
                          label="Start Index"
                        ></v-text-field
                      ></v-col>
                      <v-col cols="4" class="px-0"
                        ><v-card-text class="body-2 pa-0">To</v-card-text></v-col
                      >
                      <v-col cols="8" class="px-0 mb-2"
                        ><v-text-field
                          v-model="validationEndIndex"
                          hide-details
                          dense
                          label="End Index"
                        ></v-text-field
                      ></v-col>
                    </v-row>
                  </v-col> -->
                  <!-- <v-col cols="3">
                    <v-btn fab x-small cursor-pointer @click="addValidationIndex">
                      <v-icon>mdi-plus</v-icon></v-btn
                    >
                  </v-col> -->
                </v-row>
                <!-- <v-row>
                  <v-chip-group>
                    <v-chip
                      v-for="(validationIndex, index) in validationIndexArray"
                      :key="index"
                      close
                      @click:close="validationIndexArray.splice(index, 1)"
                      outlined
                      small
                    >
                      {{ validationIndex.start }}~{{ validationIndex.end }}
                    </v-chip>
                  </v-chip-group>
                </v-row>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      @click="
                        (validationStartIndex = datasetSize - Math.round(datasetSize * 0.2)),
                          (validationEndIndex = datasetSize)
                      "
                      v-bind="attrs"
                      v-on="on"
                      dense
                      small
                      >Default</v-btn
                    >
                  </template>
                  <span>20% from the end of dataset</span>
                </v-tooltip> -->
              </v-container>
            </v-list-item>

            <v-list-item class="pt-2">
              <v-subheader>Preset (Validation)</v-subheader>
              <v-chip-group>
                <v-chip @click="validationSet = 20" label>20%</v-chip>
                <v-chip @click="validationSet = 25" label>25%</v-chip>
              </v-chip-group>
            </v-list-item>
          </v-list-group>
          <v-divider></v-divider>

          <v-list-group sub-group :value="true" class="my-5">
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Training & Test</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item>
              <v-row>
                <!-- <v-col cols=""> <v-subheader>Training:</v-subheader></v-col> -->
                <v-col cols="">
                  <v-text-field
                    :rules="[rules.required]"
                    suffix="%"
                    type="number"
                    dense
                    outlined
                    clearable
                    label="Training"
                    v-model="trainSet"
                  ></v-text-field
                ></v-col>
              </v-row>
            </v-list-item>
            <v-list-item>
              <v-row>
                <!-- <v-col cols="5"> <v-subheader>Test:</v-subheader></v-col> -->
                <v-col cols="">
                  <v-text-field
                    hide-details
                    type="number"
                    :rules="[rules.required]"
                    suffix="%"
                    outlined
                    dense
                    clearable
                    label="Test"
                    v-model="testSet"
                  ></v-text-field
                ></v-col>
              </v-row>
            </v-list-item>

            <v-list-item class="pt-2">
              <v-subheader>Preset (Train:Test)</v-subheader>
              <v-chip-group>
                <v-chip @click="(trainSet = 60), (testSet = 40)" label>60:40</v-chip>
                <v-chip @click="(trainSet = 80), (testSet = 20)" label>80:20</v-chip>
              </v-chip-group>
            </v-list-item>
          </v-list-group>
        </v-list-group>
        <v-dialog v-model="dialog">
          <v-list-item v-for="(dataType, indexOfDataType) in dataTypeLabels" :key="indexOfDataType">
            <!-- <v-list-item-icon>
            <v-icon>{{ items[indexOfDataType].icon }}</v-icon>
          </v-list-item-icon> -->
            <v-list-item-content>
              <v-autocomplete
                outlined
                clearable
                hide-details
                dense
                no-data-text=""
                v-bind="hideDetails(indexOfDataType)"
                :label="dataTypeLabels[indexOfDataType]"
                :placeholder="datasetRatio[indexOfDataType]"
                :items="datasetRatio[indexOfDataType]"
              ></v-autocomplete>
            </v-list-item-content>
          </v-list-item>
        </v-dialog>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>
<script>
import { eventBus } from "@/main";
import InputColumnList from "@/components/modeling/columnList/InputColumnList.vue";
import TargetColumnList from "@/components/modeling/columnList/TargetColumnList.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      datasetInfo: {},

      // validationEndIndex: null,
      // validationStartIndex: null,
      validationIndexArray: [],
      dialog: false,
      drawer: true,

      dataInfoLabels: ["Draft"],
      dataTypeLabels: ["Training", "Test", "Validation"],
      datasetRatio: ["60%", "20%", "20%"],
      algorithms: ["XGBoost", "Random Forest", "SVR"],
      normalization_items: ["Standard Scaler"],
      hideDetailsProps: {
        "hide-details": true
      },
      chosenAlgorithm: null,
      items: [
        { title: "Home", icon: "mdi-home-city" },
        { title: "My Account", icon: "mdi-account" },
        { title: "Users", icon: "mdi-account-group-outline" }
      ],
      mini: true,
      // textfiled rules
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList,
      draftList: state => state.aggrid.draftList,
      datasetSize: state => state.initialData.datasetSize,
      columns: state => state.initialData.columns,
      gridList: state => state.aggrid.gridList
    }),
    ...mapGetters("initialData", ["indexNum"]),
    modelingDataset: {
      get() {
        return this.$store.state.modelingData.modelingDataset;
      },
      set(value) {
        this.saveDatasetInfo(value);
      }
    },
    testSet: {
      get() {
        return this.$store.state.modelingData.splitRatio.test;
      },
      set(value) {
        this.setRatioValue({ target: "test", value: value });
      }
    },
    trainSet: {
      get() {
        return this.$store.state.modelingData.splitRatio.train;
      },
      set(value) {
        this.setRatioValue({ target: "train", value: value });
      }
    },
    validationSet: {
      get() {
        return this.$store.state.modelingData.splitRatio.validation;
      },
      set(value) {
        this.setRatioValue({ target: "validation", value: value });
      }
    }
  },
  methods: {
    ...mapMutations("modelingData", ["saveSplitRatio"]),
    ...mapMutations("modelingData", ["saveDatasetInfo"]),

    ...mapMutations("modelingData", ["setRatioValue"]),
    ...mapActions("aggrid", ["loadDraftList"]),
    ...mapActions("aggrid", ["loadDraft"]),

    addValidationIndex() {
      this.validationIndexArray.push({
        start: this.validationStartIndex,
        end: this.validationEndIndex
      });
      this.validationStartIndex = null;
      this.validationEndIndex = null;
    },
    algorithmClicked(algorithm) {
      this.chosenAlgorithm = algorithm;
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
    }
  },
  created() {},
  mounted() {
    // this.loadDraftList();
    this.loadDraft(this.projectName);
  }
};
</script>
<style scoped>
.v-list-item__icon {
  /* margin-top: 0 !important; */
}
</style>
