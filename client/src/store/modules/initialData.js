import axios from "axios";

const state = {
  //data
  dataset: {},
  summarizedInfo: [],
  tableList: [],
  navStatus: null
};

const getters = {
  columns: function(state) {
    let columns = [];
    let columnValues = Object.keys(state.dataset);
    for (const columnValue of columnValues) {
      columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
    }
    return columns;
  },
  indexNum: function(state) {
    let columnValues = Object.keys(state.dataset);
    return Object.keys(state.dataset[columnValues[0]]).length - 1;
  }
};

const mutations = {
  loadDataset(state, payload) {
    state.dataset = payload.data;
  },

  setNavStatus(state, payload) {
    state.navStatus = payload;
  },

  loadSummarizedInfo(state, payload) {
    state.summarizedInfo = payload;
  },
  changeColumnName_vuex(state, payload) {
    let oldName = Object.keys(state.dataset)[payload.columnIndex]; //여기가 문제 되고 있음
    state.dataset[payload.newName] = state.dataset[oldName]; // 새로운 이름 생성 (복제)
    delete state.dataset[oldName]; //예전 이름 삭제
  },
  loadSelectedColumns(state, payload) {
    state.selectedColumns.push(payload);
  },
  loadTableList(state, payload) {
    state.tableList = payload;
  }
};

const actions = {
  loadFundamentalData({ commit }, path) {
    // const path = "http://localhost:5000/loadData";
    axios
      .get(path)
      .then(res => {
        commit("loadDataset", res);
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
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
