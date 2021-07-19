import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
// initial
import initialData from "@/store/modules/fundamental/initialData.js";
import apexchartGraph from "@/store/modules/fundamental/apexchartGraph.js";
// modeling
import modelingData from "@/store/modules/modeling/modelingData.js";
import modelingResult from "@/store/modules/modeling/modelingResult.js";
// simulation
import simulationData from "@/store/modules/simulation/simulationData.js";
import simulationResult from "@/store/modules/simulation/simulationResult.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData,
    apexchartGraph,
    modelingData,
    modelingResult,
    simulationData,
    simulationResult
  },
  plugins: [
    createPersistedState({
      paths: [
        "initialData",
        "apexchartGraph",
        "modelingData",
        "modelingResult",
        "simulationData",
        "simulationResult"
      ]
    })
  ]
});
