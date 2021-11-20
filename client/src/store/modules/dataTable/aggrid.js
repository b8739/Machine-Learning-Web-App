import Vue from "vue";
import axios from "axios";

const getDefaultState = () => {
  return {
    gridList: [],
    gridApi: {},
    gridColumnApi: {},

    summaryGridApi: null,
    summaryGridColumnApi: null,

    currentGrid: -1,

    analysisDisplay: false,

    // transaction
    updateTransaction: {},
    deleteTransaction: {},

    datasetToLoad: {},
    columnModel: {},
    columnsForGrid: {},
    gridType: {}
    // columns
  };
};
const state = getDefaultState();
const getters = {};

const mutations = {
  /* Grid Api */

  addGridApi(state, payload) {
    Vue.set(state.gridApi, payload.gridID, payload.api);
    // state.gridApi.push(payload); // params.api
  },

  delGridApi(state, gridID) {
    Vue.delete(state.gridApi, gridID);
  },
  /* Grid Column Api */

  addGridColumnApi(state, payload) {
    Vue.set(state.gridColumnApi, payload.gridID, payload.api);
  },
  delGridColumnApi(state, gridID) {
    Vue.delete(state.gridColumnApi, gridID);
  },
  /* Summary Grid Api*/
  setSummaryGridApi(state, payload) {
    state.summaryGridApi = payload;
  },
  /* Summary Grid Column Api*/
  setSummaryColumnGridApi(state, payload) {
    state.summaryGridColumnApi = payload;
  },
  /* Grid List */
  addGridList(state) {
    state.gridList.push(parseInt(state.currentGrid) + 1); // params.api
  },
  delGridList(state, gridID) {
    state.gridList.forEach((element, index) => {
      if (element == gridID) {
        Vue.delete(state.gridList, index);
      }
    });
  },

  /* Current Grid */
  addCurrentGrid(state) {
    state.currentGrid++; // params.api
  },

  setCurrentGrid(state, payload) {
    state.currentGrid = payload; // params.api
  },
  /* Analysis Display */

  setAnalysisDisplay(state, payload) {
    state.analysisDisplay = payload;
  },
  /* Reset */
  resetAggrid(state) {
    Object.assign(state, getDefaultState());
  },
  loadDraftInfo(state, payload) {
    Object.keys(payload).forEach(element => {
      state[element] = payload[element];
    });
    state.currentGrid = 0;
  },
  // Preprocess
  // Transaction

  /* Update */
  addNewUpdate(state, payload) {
    state.updateTransaction[state.currentGrid].push(payload);
  },
  revertUpdate(state, payload) {
    Vue.delete(state.updateTransaction, state.currentGrid, payload);
  },
  /* Delete */
  addNewDeletion(state, payload) {
    if (state.deleteTransaction[state.currentGrid] == undefined) {
      state.deleteTransaction[state.currentGrid] = [];
    }
    payload.forEach(element => {
      state.deleteTransaction[state.currentGrid].push(element["ID"]);
    });
  },
  /*tload setting*/
  setDatasetToLoad(state, payload) {
    state.datasetToLoad[parseInt(state.currentGrid) + 1] = payload;
  },
  delDatasetToLoad(state, gridID) {
    Vue.delete(state.datasetToLoad, gridID);
  },
  setColumnModel(state, payload) {
    state.columnModel[parseInt(state.currentGrid) + 1] = payload;
  },
  setColumnsForGrid(state, payload) {
    Vue.set(state.columnsForGrid, payload.tableName, payload.data);
  },

  onTabChange(state, payload) {
    state.columnsForGrid = {};
  },
  setGridType(state, payload) {
    state.gridType[parseInt(state.currentGrid) + 1] = payload;
  },
  delGridType(state, gridID) {
    Vue.delete(state.gridType, gridID);
  },
  delColumnModel(state, gridID) {
    Vue.delete(state.columnModel, gridID);
  },
  delColumnModelElement(state, payload) {
    Vue.delete(state.columnModel[state.currentGrid][payload.datasetName], payload.index);
  }
};
const actions = {
  loadDraft({ commit, state }, draftName) {
    console.log(draftName);
    const path = "http://localhost:5000/loadDraft";
    // 수정
    axios({
      method: "post",
      url: path,
      data: {
        draftName: draftName
      }
    })
      .then(res => {
        commit("resetAggrid");
        console.log(state.gridList.length);
        commit("loadDraftInfo", res.data);
        console.log(res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  saveDraft({ commit, state }, draftName) {
    const path = "http://localhost:5000/saveDraft";
    // 수정
    axios({
      method: "post",
      url: path,
      data: {
        draftName: draftName,
        gridList: state.gridList,
        deleteTransaction: state.deleteTransaction,
        datasetToLoad: state.datasetToLoad,
        columnModel: state.columnModel,
        gridType: state.gridType
      }
    })
      .then(res => {
        console.log(res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },

  createNewGrid({ commit, state }) {
    commit("addGridList");
    commit("addCurrentGrid");
    commit("setAnalysisDisplay", false);
    // grid 생성 (action으로 만들 필요성이 있음)
  },
  removeGrid({ commit, state }, gridID) {
    commit("delGridApi", gridID);
    commit("delGridColumnApi", gridID);
    commit("delGridList", gridID);
    commit("delDatasetToLoad", gridID);
    commit("delGridType", gridID);
    commit("delColumnModel", gridID);
    if (Object.keys(state.gridApi).length == 0) {
      commit("setCurrentGrid", -1);
    } else {
      commit("setCurrentGrid", Object.keys(state.gridApi)[0]);
    }
  }
};
export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
