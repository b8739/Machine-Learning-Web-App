<template>
  <div>
    <Header></Header>

    <v-container fluid class="pl-10 pt-10">
      <v-row align="start" no-gutter dense>
        <!-- <v-col cols="1">
          <v-btn @click="newSimulation" block color="success">
            <v-icon left class="mdi-24">
              mdi-plus
            </v-icon>
            New Simulation
          </v-btn>
        </v-col> -->
        <v-col cols="11"></v-col>
        <v-sheet
          light
          outlined
          min-width="200px"
          max-height="300px"
          v-for="(simulation, index) in simulationList"
          :key="index"
          class="mr-5 mt-5 cursor-pointer"
        >
          <v-card-text class="font-weight-bold body-1">Simulation #</v-card-text>
          <v-card-text class="font-weight-light caption pt-0"> Explanation</v-card-text>
          <v-card-text class="font-weight-thin caption pt-0"> Created __ ago</v-card-text>
          <v-chip class="ma-2" color="orange" outlined small @click="newSimulation">
            <v-icon left x-small>
              mdi-chart-bell-curve-cumulative
            </v-icon>
            Simulation
          </v-chip>
        </v-sheet>
      </v-row>
    </v-container>
    <SimulationModal />
  </div>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import SimulationModal from "@/components/simulation/SimulationModal.vue";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      simulationList: [1]
    };
  },
  components: {
    SimulationModal
  },
  methods: {
    ...mapMutations("initialData", ["setNavStatus"]),
    newSimulation() {
      eventBus.$emit("openSimulation", true);
    }
  },
  created() {
    this.setNavStatus("optimize");
  }
};
</script>
