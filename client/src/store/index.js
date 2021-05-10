import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import initialData from "@/store/modules/initialData.js";
import modelingData from "@/store/modules/modelingData.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData,
    modelingData
  },
  plugins: [createPersistedState({ paths: ["initialData"] })]
});
