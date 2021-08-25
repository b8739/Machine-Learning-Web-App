<template>
  <tr>
    <slot></slot>
    <!-- 3rd Column -->
    <!-- category 일 경우: category summary 표시 -->
    <td>
      <tr v-for="(summary, categorySummaryIndex) in categorySummary" :key="categorySummaryIndex">
        <span class="info_title">{{ summary }} </span>
        <span>: {{ summarizedInfo["categorical"][column][summary] }}</span>
      </tr>
      <tr></tr>
    </td>

    <!-- 4th Column -->
    <td>
      <p class="info_title">Samples For Class:</p>
      <v-row
        no-gutters
        v-for="(sample, sampleIndex) in summarizedInfo['sampleForClass'][column]"
        :key="sampleIndex"
      >
        <v-col class="py-0"> {{ sampleIndex }}</v-col>
        <v-spacer></v-spacer>
        <v-col class="py-0">{{ sample }}% </v-col>
        <v-col cols="12" class="pa-0"><v-divider></v-divider></v-col>
      </v-row>
    </td>

    <!-- category 일 경우: -- 표시 -->
    <td>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" right v-if="columnIndex == 0"
            >mdi-information-outline</v-icon
          >
        </template>
      </v-tooltip>
    </td>
  </tr>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo
    }),
    categorySummary() {
      let categoricalColumn = Object.keys(this.summarizedInfo["categorical"]);
      let categorySummary = [];
      categorySummary = Object.keys(this.summarizedInfo["categorical"][categoricalColumn[0]]);
      return categorySummary;
    }
  },
  props: ["column", "columnIndex"]
};
</script>
<style scoped>
td {
  padding: 15px 10px;
  border: 1px solid rgba(104, 102, 102, 0.644);
  border-bottom: none;
}
.info_title {
  color: grey;
}
</style>
