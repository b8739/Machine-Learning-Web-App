import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    duplicatedColumns: [],

    backedUpColumns: [],
    dialog: false
  };
};
const state = getDefaultState();

const getters = {
  summaryChangeNameFlag(state, getters, rootState) {
    let onlyDuplicatedColumnNames = [];
    state.duplicatedColumns.forEach(element => {
      onlyDuplicatedColumnNames.push(element.columnName);
    });

    let convertedString = JSON.stringify(onlyDuplicatedColumnNames);
    if (convertedString === JSON.stringify(rootState.initialData.columns)) {
      return false;
    } else {
      return true;
    }
  },
  summaryChangeTypeFlag(state, getters, rootState) {
    let onlyDuplicaedColumnTypes = [];
    state.duplicatedColumns.forEach(element => {
      onlyDuplicaedColumnTypes.push(element.datatype);
    });
    let convertedString = JSON.stringify(onlyDuplicaedColumnTypes);
    let datatypes = [];
    Object.keys(rootState.initialData.summarizedInfo.datatype).forEach(element => {
      datatypes.push(rootState.initialData.summarizedInfo.datatype[element]);
    });
    datatypes = JSON.stringify(datatypes);
    if (convertedString === datatypes) {
      return false;
    } else {
      return true;
    }
  },
  summaryChangeFlag(state, getters) {
    if (getters.summaryChangeNameFlag || getters.summaryChangeTypeFlag) {
      return true;
    } else return false;
  }
};

const mutations = {
  setDialog(state, payload) {
    state.dialog = payload;
  },
  changeColumnOrder(state, payload) {
    let temp = state.duplicatedColumns[payload.newIndex];
    Vue.set(state.duplicatedColumns, payload.newIndex, payload.columnName);
    Vue.set(state.duplicatedColumns, payload.oldIndex, temp);
    // Vue.set(state.duplicatedColumns, payload.index, payload.element);
  },
  resetSummaryTableVuex(state) {
    Object.assign(state, getDefaultState());
  },

  addDuplicatedColumn(state, payload) {
    state.duplicatedColumns.push(payload);
  },
  addBackedUpColumn(state, payload) {
    state.backedUpColumns.push(payload);
  }
};

const actions = {
  cloneOriginalArray({ commit, state, rootState }) {
    // 배열 초기화
    commit("resetSummaryTableVuex");
    // 다시 집어넣기
    let datatypes = rootState.initialData.summarizedInfo.datatype;
    rootState.initialData.columns.forEach((element, index) => {
      let columnInfo = { columnName: element, columnIndex: index, datatype: datatypes[element] };
      commit("addDuplicatedColumn", columnInfo);
      commit("addBackedUpColumn", columnInfo);
    });
  },
  backupColumns({ commit, state }) {
    state.backedUpColumns.splice(0, state.duplicatedColumns.length);
    state.duplicatedColumns.forEach(element => {
      commit("addBackedUpColumn", element);
    });
  },
  revertToBackupArray({ commit, state }) {
    state.duplicatedColumns.splice(0, state.duplicatedColumns.length);
    state.backedUpColumns.forEach(element => {
      commit("addDuplicatedColumn", element);
    });
    commit("setDialog", false);
  },
  revertNameChange({ commit, state, rootState, dispatch }) {
    console.log("revert");
    if (
      !(JSON.stringify(rootState.initialData.columns) === JSON.stringify(state.duplicatedColumns))
    )
      //false, 동일하지 않을 때
      dispatch("cloneBackupArray");
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
