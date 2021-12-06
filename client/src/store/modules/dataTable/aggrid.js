import Vue from "vue";
import axios from "axios";

const getDefaultState = () => {
  return {
    // GRID STATE
    gridList: [],
    currentGrid: -1,
    viewMode: "table",

    // GRID API
    gridApi: {},
    gridColumnApi: {},

    // GRID SUMMARY API
    summaryGridApi: null,
    summaryGridColumnApi: null,

    columnState: {},
    // GRID INFO (REQUIRED)
    datasetToLoad: {},
    columnModel: {},
    gridType: {},

    // GRID FILTER
    updateTransaction: {},
    deleteModel: {},
    renameModel: {},
    typeModel: {},

    filterModel: {},
    clientFilterModel: {},

    fillNaModel: {},
    deleteNaModel: {},

    //DRAFT
    draftList: [],

    // for dialog
    columnsForGrid: {}
  };
};
const state = getDefaultState();
const getters = {
  gridListSize(state) {
    return state.gridList.length;
  }
};

const mutations = {
  setFilterModel(state, payload) {
    Vue.set(state.filterModel, state.currentGrid, payload);
  },
  setClientFilterModel(state, payload) {
    Vue.set(state.clientFilterModel, state.currentGrid, payload);
  },
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
  addGridList(state, gridListSize) {
    state.gridList.push(gridListSize); // params.api
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
    if (state.deleteModel[state.currentGrid] == undefined) {
      state.deleteModel[state.currentGrid] = [];
    }
    payload.forEach(element => {
      state.deleteModel[state.currentGrid].push(element["ID"]);
    });
  },
  /*tload setting*/
  setDatasetToLoad(state, payload) {
    state.datasetToLoad[state.gridList.length] = payload;
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
    state.gridType[state.gridList.length] = payload;
  },
  delGridType(state, gridID) {
    Vue.delete(state.gridType, gridID);
  },
  setColumnModel(state, payload) {
    state.columnModel[state.gridList.length] = payload;
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
  },
  setDeleteNaModel(state, payload) {
    state.deleteNaModel[state.currentGrid] = payload;
  }
};
const actions = {
  mergeTables({ commit, state, dispatch }, tableIndexes) {
    if (tableIndexes.length == 2) {
      let targetTables = tableIndexes.map(function(tableIndex) {
        return state.datasetToLoad[tableIndex];
      }); // ex. [boston, concrete]

      //Set datasetToLoad
      // console.log(state.datasetToLoad);
      // let mergedDatasetToLoad = Object.keys(state.datasetToLoad).map(function(col) {
      //   return state.datasetToLoad[col];
      // });
      commit("setDatasetToLoad", targetTables);

      //Set columnModel
      let mergedColumnModel = tableIndexes.reduce(function(result, value, index) {
        let tableName = targetTables[index];
        result[tableName] = state.columnModel[value][tableName];
        return result;
      }, {});
      console.log(mergedColumnModel);

      commit("setColumnModel", mergedColumnModel);

      commit("setGridType", "AgGridMultiple");
      //마지막
      dispatch("createNewGrid");
    }
  },
  // draft
  loadDraftList({ commit, state }) {
    let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadDraftList";
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
    const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadDraft";
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
        // console.log(state.gridList.length);
        setTimeout(() => {
          commit("loadDraftInfo", res.data);
        }, 100);
        // console.log(res.data);
      })
      .catch(error => {
        console.error(error);
      });
  },
  saveDraft({ commit, state, dispatch }, draftName) {
    const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/saveDraft";

    // 수정
    axios({
      method: "post",
      url: path,
      data: {
        draftName: draftName,
        gridList: state.gridList,
        filterModel: state.filterModel,
        clientFilterModel: state.clientFilterModel,

        deleteModel: state.deleteModel,
        datasetToLoad: state.datasetToLoad,
        columnModel: state.columnModel,
        renameModel: state.renameModel,
        columnState: state.columnState,
        typeModel: state.typeModel,
        fillNaModel: state.fillNaModel,
        deleteNaModel: state.deleteNaModel,
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

  createNewGrid({ commit, state, getters }) {
    commit("addGridList", getters.gridListSize);
    commit("setCurrentGrid", getters.gridListSize - 1);
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
