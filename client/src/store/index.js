import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import initialData from "@/store/modules/initialData.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData
  },
  plugins: [createPersistedState({ paths: ["initialData"] })]
});
