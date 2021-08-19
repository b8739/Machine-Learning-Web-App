<template>
  <tr>
    <slot></slot>
    <!-- 3rd Column -->
    <td>
      <tr>
        <span v-once class="info_title">Mean </span>
        <span>: {{ summarizedInfo["numeric"][column]["mean"] }}</span>
      </tr>
      <tr>
        <span v-once class="info_title">Mode </span>
        <span>: {{ summarizedInfo["numeric"][column]["mode"] }}</span>
      </tr>
      <tr>
        <span v-once class="info_title">Median </span>
        <span>: {{ summarizedInfo["numeric"][column]["median"] }}</span>
      </tr>
      <tr>
        <span v-once class="info_title">Num of NA </span>
        <span>: {{ summarizedInfo["numeric"][column]["numOfNA"] }}</span>
      </tr>
      <tr>
        <span v-once class="info_title">Standard Deviation </span>
        <span>: {{ summarizedInfo["numeric"][column]["standard deviation"] }}</span>
      </tr>
      <tr>
        <span v-once class="info_title">Quantile </span>
        <span>: {{ summarizedInfo["numeric"][column]["Q1"] }}, </span>
        <span>{{ summarizedInfo["numeric"][column]["Q2"] }}, </span>
        <span>{{ summarizedInfo["numeric"][column]["Q3"] }}, </span>
        <span>{{ summarizedInfo["numeric"][column]["Q4"] }}, </span>
      </tr>
    </td>

    <!-- numeric 일 경우: distribution 표시 -->
    <td>
      <span v-once class="tdTitle">Distribution</span>
      <Histogram
        :distribution="summarizedInfo['distribution'][column]"
        :interval="summarizedInfo['interval'][column]"
      />
    </td>

    <td @click="openEditModal(column)">
      <!-- <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" right>mdi-information-outline</v-icon>
        </template>
        <span>Only shows upto 500 rows of the dataset (randomized)</span>
      </v-tooltip> -->

      <v-row align="center">
        <v-col align-self="center"> <span class="tdTitle"> Graph </span></v-col>
      </v-row>

      <TimeSeries :graphWidth="graphWidth" :graphHeight="graphHeight" :seriesName="column" />
    </td>
    <EditModal />
  </tr>
</template>
<script>
import TimeSeries from "@/components/graph/TimeSeries";
import Histogram from "@/components/graph/Histogram";
import EditModal from "@/components/modal/EditModal";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      graphWidth: "260px",
      graphHeight: "200px"
    };
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo
    })
  },
  props: ["column", "columnIndex"],
  components: {
    TimeSeries,
    Histogram,
    EditModal
  },
  methods: {
    openEditModal(column) {
      eventBus.$emit("openEditModal", column);
    }
  }
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
