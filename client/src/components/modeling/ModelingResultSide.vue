<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%">
    <!-- <v-btn @click="loadCases">hello</v-btn> -->
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold">Cases</v-list-item-title>
      </v-list-item>
      <v-list-item v-for="(case_, index) in caseList" :key="index">
        <v-sheet
          class="cursor-pointer"
          light
          outlined
          height="100"
          width="100%"
          @click="newWindow(case_[case_name])"
        >
          <v-card-text class="font-weight-bold subheading pt-2 pb-0">
            {{ case_["case_name"] }}</v-card-text
          >
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
      case_name: "case_name"
    };
  },
  computed: {
    ...mapState({
      caseList: state => state.modelingResult.caseList
    })
  },
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),
    ...mapMutations("modelingResult", ["saveCaseDataset"]),
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
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
    newWindow(case_name) {
      let w = 1000;
      let h = 500;
      let leftPosition = (screen.width - w) / 2;
      let topPosition = (screen.height - h) / 2;
      let url = "http://localhost:8080/modelingResult?" + case_name;
      window.open(
        url,
        "modelingResult",
        "width=" +
          w +
          ",height=" +
          h +
          ",top=" +
          topPosition +
          ",left=" +
          leftPosition +
          ", scrollbars=no"
      );
    }
  },
  created() {
    this.loadCases();
  }
};
</script>
