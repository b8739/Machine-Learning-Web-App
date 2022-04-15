<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab>Test</v-tab>
      <v-tab>Validation</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-data-table :headers="headers" :items="test_result" class="elevation-1"></v-data-table>
      </v-tab-item>
      <v-tab-item>
        <v-data-table :headers="headers" :items="valid_result" class="elevation-1"></v-data-table>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  //   watch: {
  //   modelingSummary: {
  //     handler: function(data) {

  //       this.updatePlot();
  //     },
  //     deep: true
  //   }
  // },
  data() {
    return {
      tab: null,
      // showModelingSummary: false,
      headers: [
        {
          text: "Prediction Power",
          align: "start",
          sortable: false,
          value: "name"
        },
        { text: "Value", value: "value" }
      ]
    };
  },
  computed: {
    ...mapState({
      modelingSummary: state => state.modelingData.modelingSummary
    }),

    test_result() {
      let results = [];
      let resultsFormat = {};
      for (const [key, value] of Object.entries(this.modelingSummary["test"])) {
        resultsFormat = { name: key, value: value };
        results.push(resultsFormat);
      }

      return results;
    },
    valid_result() {
      let results = [];
      let resultsFormat = {};
      for (const [key, value] of Object.entries(this.modelingSummary["valid"])) {
        resultsFormat = { name: key, value: value };
        results.push(resultsFormat);
      }

      return results;
    }
  },
  created() {
    // eventBus.$on("showModelingSummary", status => {
    //   this.showModelingSummary = status;
    // });
  }
};
</script>
