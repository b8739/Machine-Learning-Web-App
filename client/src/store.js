import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
  state:{//data
    dataSet: {},
    indexNum: "",
    hadLoaded: false,
    columns: [],
  },
  getters:{
    // vuexTestGetters:state=>{
    //   return state.vuexTest+1;
    },
  mutations: {
    loadDataset(state,payload){
      state.dataSet = payload.data;
      state.indexNum = Object.keys(payload.data["ID"]).length - 1;
    },
    loadIndexNum(state,payload){
      state.indexNum = payload;
    },
    saveResponseData() {
      let columnValues = Object.keys(state.dataSet);
      for (const columnValue of columnValues) {
        state.columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        // state.updateForm[columnValue] = "";
        // state.addForm[columnValue] = "";
        
      }
    },
  },
  actions:{
    loadFundamentalData({commit}, path) {
      // const path = "http://localhost:5000/loadData";
      axios
        .get(path)
        .then(res => {
          commit('loadDataset', res);
          // 데이터 추가 시 필요한 index number
          //'처음' 데이터를 받아올때만 columns 받아오도록 처리
          // if (state.hadLoaded == false) this.saveResponseData();
        })
        .catch(error => {
          console.error(error);
        });
    },
  }
})