<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%">
    <!-- <v-btn @click="loadCases">hello</v-btn> -->
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold">Cases</v-list-item-title>
      </v-list-item>
      <v-list-item v-for="(caseName, index) in caseList" :key="index">
        <v-sheet light outlined height="100" width="100%" @click="changeCase">
          <v-card-subtitle> {{ caseName }}</v-card-subtitle>
          <v-card-text class="font-weight-thin body-2"> Created __ days ago</v-card-text>
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
      drawer: true
    };
  },
  computed: {
    ...mapState({
      caseList: state => state.modelingResult.caseList
    })
  },
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),
    loadCases() {
      let path = "http://localhost:5000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    }
  },
  created() {
    this.loadCases();
  }
};
</script>
