import Vue from "vue";
import axios from "axios";

const getDefaultState = () => {
  return {
    gridList: [],
    gridApi: {},
    gridColumnApi: {},

    columnState: {},

    summaryGridApi: null,
    summaryGridColumnApi: null,

    currentGrid: -1,

    viewMode: "table",

    // transaction
    updateTransaction: {},
    deleteTransaction: {},

    datasetToLoad: {},
    columnModel: {},
    renameModel: {},
    columnsForGrid: {},
    gridType: {},
    typeModel: {},
    fillNaModel: {},
    draftList: []
    // columns
  };
};
const state = getDefaultState();
const getters = {};

const mutations = {
  // Column State
  setColumnState(state, payload) {
    Vue.set(state.columnState, state.currentGrid, payload);
  },
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

  setViewMode(state, payload) {
    state.viewMode = payload;
  },
  /* Reset */
  resetAggrid(state) {
    // Summary 저장
    let save1 = state.summaryGridApi;
    let save2 = state.summaryGridApi;
    let save3 = state.draftList;
    // 초기화
    Object.assign(state, getDefaultState());
    // 저장해둔 Summary 다시 assign
    state.summaryGridApi = save1;
    state.summaryGridColumnApi = save2;
    state.draftList = save3;
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
  setColumnModel(state, payload) {
    state.columnModel[parseInt(state.currentGrid) + 1] = payload;
  },
  delColumnModel(state, gridID) {
    Vue.delete(state.columnModel, gridID);
  },
  delColumnModelElement(state, payload) {
    Vue.delete(state.columnModel[state.currentGrid][payload.datasetName], payload.index);
  },
  setRenameModel(state, payload) {
    state.renameModel[state.currentGrid] = payload;
  },
  setTypeModel(state, payload) {
    state.typeModel[state.currentGrid] = payload;
  },
  setFillNaModel(state, payload) {
    state.fillNaModel[state.currentGrid] = payload;
  }
};
const actions = {
  // draft
  loadDraftList({ commit, state }) {
    let path = "http://localhost:5000/loadDraftList";
    // axios
    axios({
      method: "post",
      url: path
    })
      .then(res => {
        state.draftList = [];

        res.data.forEach(element => {
          state.draftList.push(element);
        });
      })

      .catch(error => {
        console.error(error);
      });
  },
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
        setTimeout(() => {
          commit("loadDraftInfo", res.data);
        }, 100);
        console.log(res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  saveDraft({ commit, state, dispatch }, draftName) {
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
        renameModel: state.renameModel,
        columnState: state.columnState,
        typeModel: state.typeModel,
        fillNaModel: state.fillNaModel,
        gridType: state.gridType
      }
    })
      .then(res => {
        console.log(res.data);
        dispatch("loadDraftList");
      })
      .catch(error => {
        console.error(error);
      });
  },

  createNewGrid({ commit, state }) {
    commit("addGridList");
    commit("addCurrentGrid");
    commit("setViewMode", "table");
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
