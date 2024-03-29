import axios from "axios";
import Vue from "vue";
import router from "@/router";
const getDefaultState = () => {
  return {
    summarizedInfo: {},
    tableList: [],
    navStatus: null,
    randomRange: null,
    columns: [],
    datasetSize: null,
    tableName: null,
    projectName: null,
    aggridWidth: null,
    edaWidth: null
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
  splitScreen(state) {
    state.aggridWidth = "50%";
    state.edaWidth = "45%";
  },
  resetScreen(state) {
    state.aggridWidth = "";
    state.edaWidth = "";
  },
  resetState(state) {
    Object.assign(state, getDefaultState());
  },
  resetSummarizedInfo(state) {
    state.summarizedInfo = {};
  },
  loadColumns(state, payload) {
    state.columns.splice(0, state.columns.length);
    payload.forEach(element => {
      state.columns.push(element);
    });
  },

  setDatasetSize(state, payload) {
    state.datasetSize = payload;
  },

  setNavStatus(state, payload) {
    state.navStatus = payload;
  },

  loadSummarizedInfo(state, payload) {
    // state.summarizedInfo = null;

    Vue.set(state.summarizedInfo, payload.tableName, payload.data);
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
  },
  setTableName(state, payload) {
    state.tableName = payload;
  },
  setProjectName(state, payload) {
    state.projectName = payload;
  }
};

const actions = {
  resetAllState({ commit, state, rootState }) {
    commit("resetState");
    commit("modelingData/resetModelingData", null, { root: true });
    commit("preprocessHandler/setPreprocessStatus", null, { root: true });
  },
  loadDatasetSize({ commit, state }) {
    const path = "http://localhost:8000/loadDatasetSize";
    // 수정
    axios({
      method: "post",
      url: path,
      data: { tableName: state.tableName, projectName: state.projectName }
    })
      .then(res => {
        commit("setDatasetSize", res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  loadColumns({ commit, state }) {
    let path = "http://localhost:8000/loadColumns";
    axios({
      method: "post",
      url: path,
      data: { tableName: state.tableName, projectName: state.projectName }
    })
      .then(res => {
        commit("loadColumns", res.data);
      })
      .catch(error => {
        console.error(error);
      });

    // 원본
  },
  loadStatistics({ commit, state, rootState }, tableName) {
    const path = "http://localhost:8000/loadStatistics";
    axios({
      method: "post",
      url: path,
      data: {
        tableName: tableName,
        projectName: state.projectName
        // columnModel: loadInfo.columnModel
      }
    })
      .then(res => {
        // res.data를 AgGrid에 적합하게 데이터 가공
        let summarizedInfo = Object.keys(res.data).map(function(key) {
          return res.data[key];
        });
        // summary aggrid data update
        rootState.aggrid.summaryGridApi.setRowData(summarizedInfo);

        // mutation
        let payload = { tableName: tableName, data: summarizedInfo };
        commit("loadSummarizedInfo", payload);
      })
      .catch(error => {
        console.error(error);
      });
  },
  loadRandomData({ commit, state }) {
    const path = "http://localhost:8000/loadRandomInfo";
    axios
      .get(path, {
        params: {
          //algorithmProp 전송
          tableName: state.tableName
        }
      })
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
