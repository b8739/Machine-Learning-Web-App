<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%">
    <!-- <v-btn @click="loadCases">hello</v-btn> -->
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold">Cases</v-list-item-title>
      </v-list-item>
      <v-list-item v-for="(case_, index) in caseList" :key="index">
        <v-sheet light outlined height="100" width="100%" @click="changeCase(case_[caseName])">
          <v-card-text class="font-weight-bold pt-2 pb-0"> {{ case_["caseName"] }}</v-card-text>
          <v-card-text class="font-weight-light caption pt-2 pb-1">
            {{ case_["snippet"] }}</v-card-text
          >
          <v-card-text class="font-weight-thin caption pt-1"> Created __ days ago</v-card-text>
        </v-sheet>
      </v-list-item>
      <!-- 여기 chip 들어감 -->
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import axios from "axios";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
export default {
  data() {
    return {
      tab: null,
      drawer: true,
      caseName: "caseName"
    };
  },
  computed: {
    ...mapState({
      caseList: state => state.modelingResult.caseList
    })
  },
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),
    ...mapMutations("modelingResult", ["saveCaseInfo"]),
    loadCases() {
      console.log("loadCases");
      let path = "http://localhost:5000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    },
    changeCase(caseName) {
      let path = "http://localhost:5000/changeCase";
      axios
        .get(path, {
          params: {
            //snippetProp 전송
            caseName: caseName
          }
        })
        .then(res => {
          this.saveCaseInfo(res.data);
          console.log(res.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    this.loadCases();
  }
};
</script>
