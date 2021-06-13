<template>
  <div>
    <Header />
    <v-app>
      <v-container fluid class="pl-10 pt-10">
        <v-row align="start" no-gutter dense>
          <v-col cols="1">
            <v-btn @click="openModeling" block color="success">
              <v-icon left class="mdi-24">
                mdi-plus
              </v-icon>
              New Model
            </v-btn>
          </v-col>
          <v-col cols="11"></v-col>
          <v-sheet
            light
            outlined
            width="200px"
            height="100px"
            v-for="(case_, index) in caseList"
            :key="index"
            class="mr-5 mt-5 cursor-pointer"
            @click="routeModelingResult(case_[case_name])"
          >
            <v-card-text class="font-weight-bold body-1">{{ case_["case_name"] }}</v-card-text>

            <v-card-text class="font-weight-thin caption"> {{ case_["snippet"] }}</v-card-text>
          </v-sheet>
        </v-row>
      </v-container>
      <ModelingModal />
    </v-app>
  </div>
</template>

<script>
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

import { eventBus } from "@/main";

import ModelingModal from "@/components/modeling/ModelingModal.vue";
export default {
  /*
      Defines the data used by the component
    */
  data() {
    return {
      files: [],
      case_name: "case_name"
    };
  },

  components: { ModelingModal },

  computed: {
    ...mapState({
      caseList: state => state.modelingResult.caseList
    })
  },
  /*
      Defines the method used by the component
    */
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),
    ...mapMutations("modelingResult", ["saveCaseInfo"]),
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    ...mapMutations("initialData", ["setNavStatus"]),

    routeModelingResult(case_name) {
      //   console.log(case_name);
      this.$router.push({ name: "modeling", params: { case: case_name } });
    },
    openModeling() {
      eventBus.$emit("openModeling", true);
    },
    loadCases() {
      console.log("loadCases");
      let path = "http://localhost:5000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    }
  },
  //실험
  created() {
    this.loadCases();
    this.setNavStatus("models");
  },
  mounted() {
    this.setNavStatus("models");
  }
};
</script>

<style scoped></style>
