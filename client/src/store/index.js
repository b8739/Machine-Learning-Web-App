import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";
import initialData from "@/store/modules/initialData.js";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    // 키: 값 형태로 저장됩니다.
    initialData
  },
  plugins: [createPersistedState({ paths: ["initialData"] })]
});

export default store;
