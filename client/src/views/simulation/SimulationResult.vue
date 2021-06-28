<template>
  <div>
    <Header></Header>
    <v-app>
      <v-container fluid>
        <v-row>
          <v-col cols="2">
            <SimulationResultSide />
          </v-col>

          <v-col cols="10">
            <v-toolbar elevation="1" dense>
              <v-spacer></v-spacer>

              <v-btn @click="dialog = true">Save Simulation</v-btn>
            </v-toolbar>
            <ApexChart> </ApexChart>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import ApexChart from "@/components/simulation/ApexChart.vue";
import SimulationResultSide from "@/components/simulation/SimulationResultSide.vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },

  components: { ApexChart, SimulationResultSide },
  computed: {
    ...mapState({})
  },
  methods: {},

  created() {
    let caseNameFromUrl = window.location.search.substring(1);
    if (caseNameFromUrl != "") {
      this.changeCase(caseNameFromUrl);
    }
    eventBus.$on("changeCase", caseNameFromUrl => {
      this.changeCase(caseNameFromUrl);
    });
  }
};
</script>

<style scoped></style>
