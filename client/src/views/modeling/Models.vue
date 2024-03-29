<template>
  <div>
    <Header />

    <v-container fluid class="pl-10 pt-10">
      <v-row align="start" no-gutter dense>
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              개발 현황
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-simple-table>
                <template>
                  <thead>
                    <tr>
                      <th>Feature</th>
                      <th>Progress</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(info, index) in devProgess" :key="index">
                      <td>{{ info.function }}</td>
                      <td>
                        <v-icon :color="iconColor(info.progress)">{{ info.progress }}</v-icon>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>

        <v-col cols="1">
          <v-btn @click="openModeling" block color="success">
            <v-icon left class="mdi-24">
              mdi-plus
            </v-icon>
            New Model
          </v-btn>
        </v-col>
        <v-col cols="11"></v-col>
        <v-sheet
          light
          outlined
          width="200px"
          max-height="300px"
          v-for="(case_, index) in caseList"
          :key="index"
          class="mr-5 mt-5 cursor-pointer"
        >
          <!-- @click="routeModelingResult(case_[case_name])" v-sheet-->
          <v-card-text class="font-weight-bold body-1">{{ case_["case_name"] }}</v-card-text>
          <v-card-text class="font-weight-light caption pt-0">
            {{ case_["algorithm"] }}</v-card-text
          >
          <!-- <v-card-text class="font-weight-thin caption pt-0">
            {{ case_["used_dataset"] }}</v-card-text
          > -->
          <v-chip-group column>
            <v-chip
              class="ma-2"
              color="success"
              outlined
              small
              @click="routeModelingResult(case_[case_name])"
            >
              <v-icon left small>
                mdi-transit-connection
              </v-icon>
              Modeling
            </v-chip>
            <v-chip class="ma-2" color="orange" outlined small @click="newSimulation(case_['id'])">
              <v-icon left x-small>
                mdi-chart-bell-curve-cumulative
              </v-icon>
              Simulation
            </v-chip>
          </v-chip-group>
        </v-sheet>
      </v-row>
    </v-container>
    <!-- <ModelingModal /> -->

    <NewSimulationModal />
  </div>
</template>

<script>
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

import { eventBus } from "@/main";

import ModelingModal from "@/components/modeling/ModelingModal.vue";
import SimulationModal from "@/components/simulation/SimulationModal.vue";
import NewSimulationModal from "@/components/simulation/NewSimulationModal.vue";

export default {
  /*
      Defines the data used by the component
    */
  data() {
    return {
      devProgess: [
        { function: "Create New Model", progress: "mdi-check" },
        { function: "Load Model from DB", progress: "mdi-check" },
        { function: "Execute Modeling", progress: "mdi-check" },
        { function: "Save Model in DB", progress: "mdi-check" },
        { function: "Delete Model", progress: "mdi-close" },
        { function: "Simulation", progress: "mdi-close" }
      ],
      files: [],
      case_name: "case_name"
    };
  },

  components: { ModelingModal, SimulationModal, NewSimulationModal },

  computed: {
    ...mapState({
      caseList: state => state.modelingData.caseList
    })
  },
  /*
      Defines the method used by the component
    */
  methods: {
    // 테이블 정보
    ...mapMutations("modelingData", ["saveCaseList"]),
    ...mapMutations("modelingData", ["saveCaseDataset"]),
    // 시각화
    ...mapMutations("modelingData", ["saveGraphSources"]),
    ...mapMutations("modelingData", ["saveModelingSummary"]),
    // nav 정보
    ...mapMutations("initialData", ["setNavStatus"]),
    iconColor(value) {
      if (value == "mdi-check") {
        return "blue";
      } else return "red";
    },
    newSimulation(caseID) {
      console.log(caseID);
      eventBus.$emit("openSimulation", caseID);
    },
    routeModelingResult(case_name) {
      //   console.log(case_name);
      this.$router.push({ name: "modelingResult", params: { case: case_name } });
    },
    openModeling() {
      eventBus.$emit("openModeling", true);
      this.$router.push({ name: "modelingProcess" });
    },
    loadCases() {
      let path = "http://localhost:8000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    }
  },
  //실험
  created() {
    this.loadCases();
    this.setNavStatus("models");
  },
  mounted() {
    this.setNavStatus("models");
  }
};
</script>

<style scoped></style>
