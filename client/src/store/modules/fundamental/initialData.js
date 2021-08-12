import axios from "axios";
import Vue from "vue";

const state = {
  //data
  dataset: {},
  summarizedInfo: [],
  tableList: [],
  navStatus: null,
  randomRange: null,
  columns: []
};

const getters = {
  // columns(state) {
  //   let columnValues = Object.keys(state.dataset[0]);
  //   return columnValues;
  // },
  numericColumns(state) {
    let columnValues = Object.keys(state.summarizedInfo["numeric"]);
    return columnValues;
  },

  indexNum(state) {
    let columnValues = Object.keys(state.dataset);
    return Object.keys(state.dataset[columnValues[0]]).length - 1;
  }
};

const mutations = {
  // saveColumnNames(state) {
  //   state.columns = [];
  //   let columnValues = Object.keys(state.dataset);
  //   for (const columnValue of columnValues) {
  //     state.columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
  //   }
  // },
  changedColumnOrder(state, payload) {
    getters.columns;
    payload.forEach(element => {
      state.modifiedColumns.push(element);
    });
  },
  setColumns(state, payload) {
    state.columns = [];
    Object.keys(state.dataset[0]).forEach(element => {
      state.columns.push(element);
    });
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
  loadColumns(state, payload) {
    state.columns = Object.keys(state.dataset);
  },
  loadSelectedColumns(state, payload) {
    state.selectedColumns.push(payload);
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
  loadFundamentalData({ commit }, path) {
    // const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadData";
    axios
      .get(path)
      .then(res => {
        // console.log(res.data);
        commit("loadDataset", res.data);
        commit("setColumns");
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
