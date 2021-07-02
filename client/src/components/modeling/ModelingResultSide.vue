<template>
  <v-navigation-drawer v-model="drawer" absolute width="100%" height="100vh">
    <!-- <v-btn @click="loadCases">hello</v-btn> -->
    <v-list>
      <!-- title -->
      <v-list-item>
        <v-list-item-title class="font-weight-bold">Cases</v-list-item-title>
      </v-list-item>
      <!-- item -->
      <v-list-item-group>
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
              {{ case_["algorithm"] }}</v-card-text
            >
            <v-card-text class="font-weight-thin caption pt-1"> Created __ days ago</v-card-text>
          </v-sheet>
        </v-list-item>
      </v-list-item-group>
      <!-- 여기 chip 들어감 -->
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";
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
      let url = "http://localhost:8080/modelingSingleResult/" + case_name;

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
      eventBus.$emit("multiTab", true);
    }
  },
  created() {
    this.loadCases();
  }
};
</script>
