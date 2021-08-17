import axios from "axios";
import Vue from "vue";
import router from "@/router";
const getDefaultState = () => {
  return {
    summarizedInfo: null,
    tableList: [],
    navStatus: null,
    randomRange: null,
    columns: [],
    datasetSize: null
  };
};
const state = getDefaultState();

const getters = {
  numericColumns(state) {
    let columnValues = Object.keys(state.summarizedInfo["numeric"]);
    return columnValues;
  }
};

const mutations = {
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  loadColumns(state, payload) {
    state.columns.splice(0, state.columns.length);
    payload.forEach(element => {
      state.columns.push(element);
    });
  },
  loadDatasetSize(state, payload) {
    state.datasetSize = payload;
  },

  loadDataset(state, payload) {
    state.dataset = payload;
  },

  setNavStatus(state, payload) {
    state.navStatus = payload;
  },

  loadSummarizedInfo(state, payload) {
    state.summarizedInfo = payload;
  },
  changeColumnName_vuex(state, payload) {
    let columnList = Object.keys(state.dataset);
    let originalIndex = payload.columnIndex;
    let oldName = columnList[originalIndex];
    let newName = payload.newName;
    Vue.set(state.dataset, newName, state.dataset[oldName]);
    Vue.delete(state.dataset, oldName);
    // summarizedInfo
    // Vue.set(state.summarizedInfo.datatype, newName, state.summarizedInfo.datatype[oldName]);
    // Vue.delete(state.summarizedInfo.datatype, oldName);
  },

  loadTableList(state, payload) {
    state.tableList = payload;
  },
  loadRandomInfo(state, payload) {
    state.randomRange = payload;
  },
  deleteDataFromGraph(state, payload) {
    payload.checkedRows.forEach(element => {
      Vue.delete(state.dataset, element);
      // Vue.set(state.dataset[element], payload.featureName, null);
    });
    // console.log(state.dataset);
  },
  updateColumnOrder(state, payload) {
    state.columns = [];
    payload.forEach(element => {
      state.columns.push(element);
    });
  }
};

const actions = {
  loadDatasetSize({ commit }) {
    const path = "http://localhost:5000/loadDatasetSize";
    axios
      .get(path)
      .then(res => {
        // console.log(res.data);
        commit("loadDatasetSize", res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  loadColumns({ commit }) {
    let path = "http://localhost:5000/loadColumns";
    axios
      .get(path)
      .then(res => {
        // console.log(res.data);
        commit("loadColumns", res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  loadSummarizedData({ commit }) {
    const path = "http://localhost:5000/loadSummarizedData";
    axios
      .get(path)
      .then(res => {
        commit("loadSummarizedInfo", res.data);
        router.push({ name: "preprocess" });
      })
      .catch(error => {
        console.error(error);
      });
  },
  loadRandomData({ commit }) {
    const path = "http://localhost:5000/loadRandomInfo";
    axios
      .get(path)
      .then(res => {
        commit("loadRandomInfo", res.data);
      })
      .catch(error => {
        console.error(error);
      });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
