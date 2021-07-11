<template>
  <div>
    <Header></Header>

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
  methods: {
    ...mapMutations("simulationResult", ["saveGraphSources"]),
    runSimulation() {
      //uniform (관찰변수:min & max(np.random.uniform), 나머지:median) mode uniform 통일,일단은 Median값이지만 수정가능하도록
      // let path = "http://localhost:5000/simulation_ud";

      //normal (관찰변수:정규분포 (np.random.normal), 나머지:median)
      let path = "http://localhost:5000/simulation_nd"; 
      this.$axios
        .get(path, {
          params: {
            observedVariable: this.observedVariable
          }
        })
        .then(res => {
          this.saveGraphSources(res.data); // 그래프 값 저장
          this.eventBus.$emit("updateChart", true);
        })
        .catch(error => {
          console.error(error);
        });

      // customzied
    }
  },

  created() {
    let caseNameFromUrl = window.location.search.substring(1);
    if (caseNameFromUrl != "") {
      this.changeCase(caseNameFromUrl);
    }
    eventBus.$on("changeCase", caseNameFromUrl => {
      this.changeCase(caseNameFromUrl);
    });
  },
  mounted() {
    console.log("mounted");
    this.runSimulation();
  }
};
</script>

<style scoped></style>
