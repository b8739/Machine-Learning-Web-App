<template>
  <v-card>
    <v-navigation-drawer v-model="drawer" absolute height="1000px" permanent>
      <!-- :mini-variant.sync="mini" -->
      <v-list-item class="px-2">
        <v-list-item-title>Modeling Setting</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-group prepend-icon="mdi-database" :value="true">
          <template v-slot:activator>
            <v-list-item-title>Dataset</v-list-item-title>
          </template>
          <v-list-item
            link
            v-for="(dataInfo, indexOfDataInfo) in dataInfoLabels"
            :key="indexOfDataInfo"
          >
            <v-list-item-content>
              <v-autocomplete
                class="mt-3"
                outlined
                clearable
                hide-details
                dense
                :label="dataInfoLabels[indexOfDataInfo]"
                :items="getItems(indexOfDataInfo)"
              ></v-autocomplete>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>

        <v-divider></v-divider>
        <!-- splitting data -->
        <v-list-group prepend-icon="mdi-arrow-decision-outline" :value="true">
          <!-- 1st Level -->
          <template v-slot:activator>
            <v-list-item-title>Data Split</v-list-item-title>
          </template>
          <!-- 2nd Level -->
          <v-list-group sub-group :value="true">
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
                <v-row justify="center" align="center">
                  <v-col cols="9">
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
                  </v-col>
                  <v-col cols="3">
                    <v-btn fab x-small cursor-pointer @click="addValidationIndex">
                      <v-icon>mdi-plus</v-icon></v-btn
                    >
                  </v-col>
                </v-row>
                <v-row>
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
                </v-tooltip>
              </v-container>
            </v-list-item>
          </v-list-group>
          <v-list-group sub-group :value="true">
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Training & Test</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item>
              <v-row>
                <v-col cols=""> <v-subheader>Training:</v-subheader></v-col>
                <v-col cols="7">
                  <v-text-field
                    :rules="[rules.required]"
                    suffix="%"
                    dense
                    outlined
                    clearable
                    v-model="trainSet"
                  ></v-text-field
                ></v-col>
              </v-row>
            </v-list-item>
            <v-list-item>
              <v-row>
                <v-col cols="5"> <v-subheader>Test:</v-subheader></v-col>
                <v-col cols="7">
                  <v-text-field
                    :rules="[rules.required]"
                    suffix="%"
                    outlined
                    dense
                    clearable
                    v-model="testSet"
                  ></v-text-field
                ></v-col>
              </v-row>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item>
              <v-subheader>Example Ratios (Train:Test)</v-subheader>
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
      validationEndIndex: null,
      validationStartIndex: null,
      validationIndexArray: [],
      dialog: false,
      drawer: true,
      trainSet: null,
      testSet: null,
      dataInfoLabels: ["Dataset"],
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
      datasetSize: state => state.initialData.datasetSize,
      columns: state => state.initialData.columns
    }),
    ...mapGetters("initialData", ["indexNum"]),
    splitRatio() {
      return { validation: this.validationIndexArray, train: this.trainSet, test: this.testSet };
    }
  },
  methods: {
    ...mapMutations("modelingData", ["saveSplitRatio"]),
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
    saveRequest() {
      this.saveSplitRatio(this.splitRatio);
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
  created() {
    eventBus.$on("saveRequest_canvasSide", status => {
      this.saveRequest();
    });
  }
};
</script>
<style scoped>
.v-list-item__icon {
  /* margin-top: 0 !important; */
}
</style>
