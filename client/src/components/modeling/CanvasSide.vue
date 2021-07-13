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
                <v-list-item-title>Validation</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item>
              <v-btn outlined small> Select Validation Data </v-btn>
            </v-list-item>
          </v-list-group>
          <v-list-group sub-group :value="true">
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>Training & Test</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item>
              <v-col cols="5"> <v-subheader>Training:</v-subheader></v-col>
              <v-text-field suffix="%" dense outlined clearable hide-details></v-text-field>
            </v-list-item>
            <v-list-item>
              <v-col cols="5"> <v-subheader>Test:</v-subheader></v-col>
              <v-text-field suffix="%" outlined dense clearable hide-details></v-text-field>
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
      dialog: false,
      drawer: true,
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
      mini: true
    };
  },
  computed: {
    ...mapState({
      tableList: state => state.initialData.tableList
    })
  },
  methods: {
    ...mapMutations("modelingData", ["saveAlgorithm"]),
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
      this.$router.push({ name: "modelingProcess" });
    }
  }
};
</script>
<style scoped>
.v-list-item__icon {
  /* margin-top: 0 !important; */
}
</style>
