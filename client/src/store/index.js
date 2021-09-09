import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
// import router from "@/router";
import createPersistedState from "vuex-persistedstate";
// initial
import initialData from "@/store/modules/fundamental/initialData.js";
import apexchartGraph from "@/store/modules/fundamental/apexchartGraph.js";
// modeling
import modelingData from "@/store/modules/modeling/modelingData.js";
// simulation
import simulationData from "@/store/modules/simulation/simulationData.js";
import simulationResult from "@/store/modules/simulation/simulationResult.js";
// save
import saveFlag from "@/store/modules/save/saveFlag.js";
// infiniteTable
import tableData from "@/store/modules/dataTable/tableData.js";
// preprocess
import preprocessHandler from "@/store/modules/preprocess/preprocessHandler.js";
import dataTableHandler from "@/store/modules/preprocess/dataTableHandler.js";
import summaryTableHandler from "@/store/modules/preprocess/summaryTableHandler.js";
//eda
import edaHandler from "@/store/modules/eda/edaHandler.js";
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData,
    apexchartGraph,
    modelingData,
    simulationData,
    simulationResult,
    saveFlag,
    tableData,
    preprocessHandler,
    dataTableHandler,
    summaryTableHandler,
    edaHandler
  },
  plugins: [
    createPersistedState({
      // paths: ["initialData", "apexchartGraph", "modelingData", "simulationData", "simulationResult"]
      // paths: ["initialData"]
    })
  ]
});
