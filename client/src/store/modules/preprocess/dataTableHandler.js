import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    //   overall
    datasetItems: [],
    //deleteData
    checkedRows: [],

    //insertData
    columnField: {},
    numOfInsertion: 0,
    insertedItems: [],
    dialog: false
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  resetDatasetItems(state, payload) {
    state.datasetItems = [];
    state.checkedRows = [];
  },
  deleteDatasetItems(state, payload) {
    payload.forEach(element => {
      Vue.delete(state.datasetItems, element);
    });
  },
  addDatasetItems(state, payload) {
    state.datasetItems.push(...payload);
  },
  setCheckedRows(state, payload) {
    state.checkedRows = payload;
  },
  setColumnField(state, payload) {
    state.columnField = payload;
  },
  setNumOfInsertion(state, payload) {
    state.numOfInsertion = payload;
  },
  addInsertItems(state, payload) {
    state.insertedItems.push(payload);
  },
  setDialog(state, payload) {
    state.dialog = payload;
  },
  resetDataTableVuex(state) {
    Object.assign(state, getDefaultState());
  }
};

const actions = {
  //   cancelEvent({ commit, state }) {

  //   },
  deleteRow({ commit, state, rootState }) {
    let path = "http://localhost:5000/deleteSingleRow";
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        idNumbers: state.checkedRows
      }
    })
      .then(res => {
        // 데이터 삭제 (updating frontend)
        commit("deleteDatasetItems", state.checkedRows);
        let numOfRows = state.checkedRows.length;
        // 체크박스 초기화
        let emptyArray = [];
        commit("setCheckedRows", emptyArray);

        commit("initialData/setDatasetSize", rootState.initialData.datasetSize - numOfRows, {
          root: true
        });
        alert(`Total ${numOfRows} row(s) Successfully Deleted!`); //삭제 알림
        // 초기화
        commit("preprocessHandler/setEditMode", false, { root: true });
        commit("preprocessHandler/setPreprocessStatus", null, { root: true });
      })
      .catch(error => {
        console.error(error);
      });
  },

  insertRow({ commit, state, rootState }) {
    let path = "http://localhost:5000/insertRow";
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        rowToInsert: state.columnField
      }
    })
      .then(res => {
        alert("Data Added");
        commit("setNumOfInsertion", state.numOfInsertion + 1);
        commit("addInsertItems", JSON.parse(JSON.stringify(state.columnField)));
        //   초기화
        commit("preprocessHandler/setPreprocessStatus", null, { root: true });
        commit("setDialog", false);
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
