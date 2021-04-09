import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import dataset from "./dataset.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: dataset,
  plugins: [createPersistedState({ paths: ["dataset"] })]
});
