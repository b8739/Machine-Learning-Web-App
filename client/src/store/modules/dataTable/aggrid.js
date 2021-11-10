import Vue from "vue";

const getDefaultState = () => {
  return {
    gridApi: {},
    gridColumnApi: {},
    summaryGridApi: null,
    summaryGridColumnApi: null,
    currentGrid: -1,
    hiddenCols: {},
    gridList: [],
    analysisDisplay: false,
    //undo & redo
    availableUndo: 0,
    availableRedo: 0,
    // transaction
    updateTransaction: {},
    deleteTransaction: {}
    // columns
  };
};
const state = getDefaultState();
const getters = {};
const mutations = {
  // transaction
  deleteUpdateTransaction(state, payload) {
    Vue.delete(state.updateTransaction, state.currentGrid, payload);
  },
  addUpdateTransaction(state, payload) {
    state.updateTransaction[state.currentGrid].push(payload);
  },

  addDeleteTransaction(state, payload) {
    if (state.deleteTransaction[state.currentGrid] == undefined) {
      state.deleteTransaction[state.currentGrid] = [];
    }
    payload.forEach(element => {
      state.deleteTransaction[state.currentGrid].push(element["ID"]);
    });
  },
  // undo redo
  setAvailableUndo(state, payload) {
    state.availableUndo = payload;
  },
  setAvailableRedo(state, payload) {
    state.availableRedo = payload;
  },
  delGridApi(state, gridID) {
    Vue.delete(state.gridApi, gridID);
  },
  delGridColumnApi(state, gridID) {
    Vue.delete(state.gridColumnApi, gridID);
  },
  delGridList(state, gridID) {
    state.gridList.forEach((element, index) => {
      if (element == gridID) {
        Vue.set(state.gridList, index, undefined);
        // Vue.delete(state.gridList, index);
        // state.gridList.splice(index, 1);
      }
    });
  },
  addGridApi(state, payload) {
    Vue.set(state.gridApi, state.currentGrid, payload);
    // state.gridApi.push(payload); // params.api
  },

  addGridColumnApi(state, payload) {
    state.gridColumnApi[state.currentGrid] = payload; // params.api
  },
  setSummaryGridApi(state, payload) {
    state.summaryGridApi = payload;
  },
  setSummaryColumnGridApi(state, payload) {
    state.summaryGridColumnApi = payload;
  },

  addGridList(state) {
    state.gridList.push(parseInt(state.currentGrid) + 1); // params.api
  },
  addCurrentGrid(state) {
    state.currentGrid++; // params.api
  },

  setCurrentGrid(state, payload) {
    state.currentGrid = payload; // params.api
  },
  setAnalysisDisplay(state, payload) {
    state.analysisDisplay = payload;
  },
  resetAggrid(state) {
    Object.assign(state, getDefaultState());
  }
};
const actions = {
  removeGrid({ commit, state }, gridID) {
    commit("delGridApi", gridID);
    commit("delGridColumnApi", gridID);
    commit("delGridList", gridID);
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
