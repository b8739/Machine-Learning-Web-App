import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    duplicatedColumns: []
  };
};
const state = getDefaultState();

const getters = {
  changeFlag(state, getters, rootState) {
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
  }
};

const mutations = {
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
  }
};

const actions = {
  cloneArray({ commit, state, rootState }) {
    state.duplicatedColumns.splice(0, state.duplicatedColumns.length);
    rootState.initialData.columns.forEach((element, index) => {
      let columnInfo = { columnName: element, columnIndex: index };
      commit("addDuplicatedColumn", columnInfo);
    });
  }
  //  calculateTransaction({ commit, state, rootState }){
  //      let sql = "ALTER TABLE dataset MODIFY COLUMN "
  //      +movedColumnName+ ' ' +originalType+ ' BEFORE '
  //      this.duplicatedColumns.forEach((element,index) => {
  //          if(index!=element.columnIndex){
  //             sql = sql +element.columnName+' ';
  //          }
  //      });
  //  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
