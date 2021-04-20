import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";
import initialData from "./initialData.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    initialData: initialData
  },
  state: {
    //data
    dataset: {},
    summarizedInfo: [],
    indexNum: "",
    hadLoaded: false,
    columns: []
  },

  getters: {},

  mutations: {
    loadDataset(state, payload) {
      state.dataset = payload.data;
    },
    loadIndexNum(state, payload) {
      state.indexNum = payload;
    },
    setHadLoaded(state, payload) {
      state.hadLoaded = payload;
    },
    saveResponseData(state) {
      if (state.hadLoaded == false) {
        let columnValues = Object.keys(state.dataset);
        for (const columnValue of columnValues) {
          state.columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
          // state.updateForm[columnValue] = "";
          // state.addForm[columnValue] = "";
        }
      }
    },
    loadSummarizedInfo(state, payload) {
      state.summarizedInfo = payload;
    }
  },

  actions: {
    loadFundamentalData({ commit }, path) {
      // const path = "http://localhost:5000/loadData";
      axios
        .get(path)
        .then(res => {
          commit("loadDataset", res);
          console.log(res);
          commit("loadIndexNum", Object.keys(res.data["ID"]).length - 1);
          // 데이터 추가 시 필요한 index number
          //'처음' 데이터를 받아올때만 columns 받아오도록 처리
          commit("saveResponseData");
        })
        .catch(error => {
          console.error(error);
        });
    }
  },

  plugins: [createPersistedState({ paths: ["initialData"] })]
});