import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import initialData from "@/store/modules/initialData.js";
import modelingData from "@/store/modules/modelingData.js";
import modelingResult from "@/store/modules/modelingResult.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData,
    modelingData,
    modelingResult
  },
  plugins: [createPersistedState({ paths: ["initialData", "modelingResult"] })]
});
