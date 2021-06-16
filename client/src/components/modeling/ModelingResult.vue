<template>
  <div class="resultContainer">
    <v-container>
      <v-row>
        <v-col cols="12">
          <ApexChart />
        </v-col>
        <v-col cols="12">
          <ModelingSummary />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import ApexChart from "@/components/modeling/ApexChart.vue";
import ModelingSummary from "@/components/modeling/ModelingSummary.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },

  components: { ApexChart, ModelingSummary },
  computed: {
    ...mapState({
      graphSources: state => state.modelingResult.graphSources,
      modelingSummary: state => state.modelingResult.modelingSummary
    })
  },
  methods: {
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),

    changeCase(case_name) {
      // changecase
      let path = "http://localhost:5000/changeCase";
      this.$axios
        .get(path, {
          params: {
            //snippetProp 전송
            case_name: case_name
          }
        })
        .then(res => {
          // this.saveCaseDataset(res.data);
          this.saveGraphSources(res.data[0]); // 그래프 값 저장
          this.saveModelingSummary(res.data[1]); // 테이블 값 저장

          console.log(res.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    let caseNameFromUrl = window.location.search.substring(1);
    if (caseNameFromUrl != "") {
      this.changeCase(caseNameFromUrl);
    }
    eventBus.$on("changeCase", caseNameFromUrl => {
      this.changeCase(caseNameFromUrl);
    });
  }
};
</script>

<style scoped>
.resultContainer {
  /* width: 1000px; */
  height: 1000px;
}
</style>
