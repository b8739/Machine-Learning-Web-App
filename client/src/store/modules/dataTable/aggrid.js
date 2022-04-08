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
    currentDraft: null,

    // for dialog
    columnsForGrid: {},
    graphSelectModel: {}
  };
};
const state = getDefaultState();
const getters = {
  gridListSize(state) {
    return state.gridList.length;
  },
  currentDataset(state) {
    return state.datasetToLoad[state.currentGrid];
  }
};

const mutations = {
  setGraphSelectModel(state, payload) {
    state.graphSelectModel[state.currentGrid] = payload;
    state.gridApi[state.currentGrid].refreshInfiniteCache();
  },
  setFilterModel(state, payload) {
    Vue.set(state.filterModel, state.currentGrid, payload);
  },
  delFilterModel(state, gridID) {
    Vue.delete(state.filterModel, gridID);
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
  addGridList(state, gridInfo) {
    if (gridInfo.name == "") {
      gridInfo.name = "unnamed";
    }
    state.gridList.push(gridInfo); // params.api
  },
  delGridList(state, gridID) {
    state.gridList.forEach((element, index) => {
      if (element.id == gridID) {
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
    let save2 = state.summaryGridColumnApi;
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
      state.deleteModel[state.currentGrid].push(element);
    });
  },
  /*tload setting*/

  setDatasetToLoad(state, payload) {
    state.datasetToLoad[payload.gridID] = payload.datasetToLoad;
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
    state.gridType[state.currentGrid] = payload;
  },
  delGridType(state, gridID) {
    Vue.delete(state.gridType, gridID);
  },
  setColumnModel(state, payload) {
    state.columnModel[payload.gridID] = payload.columnModel;
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

  delRenameModel(state, gridID) {
    Vue.delete(state.renameModel, gridID);
  },
  setTypeModel(state, payload) {
    state.typeModel[state.currentGrid] = payload;
  },
  delTypeModel(state, gridID) {
    Vue.delete(state.typeModel, gridID);
  },
  setFillNaModel(state, payload) {
    state.fillNaModel[state.currentGrid] = payload;
  },
  delFillNaModel(state, gridID) {
    Vue.delete(state.fillNaModel, gridID);
  },
  setDeleteNaModel(state, payload) {
    state.deleteNaModel[state.currentGrid] = payload;
  },
  delDeleteNaModel(state, gridID) {
    Vue.delete(state.deleteNaModel, gridID);
  },
  setCurrentDraft(state, payload) {
    state.currentDraft = payload;
  }
};

const actions = {
  mergeTables({ commit, state, dispatch }, tableIndexes) {
    let targetTables;
    let gridType;
    let mergedColumnModel = {};
    // Single 일시에
    //  Set DatasetToLoad

    if (state.datasetToLoad[tableIndexes[0]] == state.datasetToLoad[tableIndexes[1]]) {
      targetTables = state.datasetToLoad[tableIndexes[0]];
      gridType = "AgGridSingle";
      // Set ColumnModel
      mergedColumnModel[targetTables] = [];
      tableIndexes.forEach(tbIndex => {
        state.columnModel[tbIndex][targetTables].forEach(col => {
          mergedColumnModel[targetTables].push(col);
        });
      });
    }
    //  Multiple일시에
    //Set DatasetToload
    else {
      targetTables = tableIndexes.map(function(tableIndex) {
        return state.datasetToLoad[tableIndex];
      });
      gridType = "AgGridMultiple";
      // Set ColumnModel
      mergedColumnModel = tableIndexes.reduce(function(result, value, index) {
        let tableName = targetTables[index];
        result[tableName] = state.columnModel[value][tableName];
        return result;
      }, {});
    }

    // 3. Create
    let payload = {
      datasetToLoad: targetTables,
      columnModel: mergedColumnModel
    };
    let newGridID = Promise.resolve(dispatch("getRandValue"));
    newGridID.then(value => {
      payload["newGridID"] = value;
      dispatch("createNewGrid", payload);
      commit("setGridType", gridType);
    });
    //초기화
  },
  // draft
  loadDraftList({ commit, state }) {
    let path = "http://localhost:8000/loadDraftList";
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
  loadDraft({ commit, state, rootState }) {
    const path = "http://localhost:8000/draft";
    // 수정
    axios({
      method: "get",
      url: path,
      params: {
        projectName: rootState.initialData.projectName
      }
    })
      .then(res => {
        // 비어있지 않을때만
        if (res.data.length != 0) {
          commit("resetAggrid");
          // commit("setCurrentDraft", draftName);
          setTimeout(() => {
            commit("loadDraftInfo", res.data);
            // Set Current Grid
            commit("setCurrentGrid", res.data["gridList"][0]["id"]);
          }, 100);
        }
      })
      .catch(error => {
        alert(error.response.data);
      });
  },
  saveDraft({ commit, state, rootState, dispatch }) {
    const path = "http://localhost:8000/saveDraft";

    // 수정
    axios({
      method: "post",
      url: path,
      data: {
        projectName: rootState.initialData.projectName,
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
        alert(res.data);
        dispatch("loadDraftList");
      })
      .catch(error => {
        console.error(error);
      });
  },
  getRandValue({ commit, state }) {
    let gridIdList = state.gridList.map(function(gridInfo) {
      return gridInfo.id;
    });
    let randValue = Math.floor(Math.random() * (10 - 1) + 1);

    while (gridIdList.includes(randValue)) {
      randValue = Math.floor(Math.random() * (10 - 1) + 1);
    }
    return randValue;
  },
  createNewGrid({ commit, state, getters }, payload) {
    commit("setDatasetToLoad", { gridID: payload.newGridID, datasetToLoad: payload.datasetToLoad });
    commit("setColumnModel", { gridID: payload.newGridID, columnModel: payload.columnModel });

    commit("addGridList", { id: payload.newGridID, name: payload.datatableName });

    commit("setCurrentGrid", payload.newGridID);

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
    //
    commit("delColumnModel", gridID);
    commit("delTypeModel", gridID);
    commit("delFillNaModel", gridID);
    commit("delDeleteNaModel", gridID);
    commit("delFilterModel", gridID);

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
