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
        <v-card-text class="pt-0" v-show="mini == false">Choose Dataset</v-card-text>
        <v-list-item
          link
          v-for="(dataInfo, indexOfDataInfo) in dataInfoLabels"
          :key="indexOfDataInfo"
        >
          <v-list-item-icon>
            <v-icon> mdi-database</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-autocomplete
              outlined
              clearable
              dense
              :label="dataInfoLabels[indexOfDataInfo]"
              :items="getItems(indexOfDataInfo)"
            ></v-autocomplete>
          </v-list-item-content>
        </v-list-item>
        <!-- splitting data -->
        <v-card-text v-show="mini == false">Splitting Dataset</v-card-text>
        <v-list-item v-for="(dataType, indexOfDataType) in dataTypeLabels" :key="indexOfDataType">
          <v-list-item-icon>
            <v-icon>{{ items[indexOfDataType].icon }}</v-icon>
          </v-list-item-icon>
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
      drawer: true,
      dataInfoLabels: ["Dataset"],
      dataTypeLabels: ["Training", "Validation", "Test"],
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
