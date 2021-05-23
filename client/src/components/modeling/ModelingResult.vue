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
import ApexChart from "@/components/modeling/ApexChart.vue";
import ModelingSummary from "@/components/modeling/ModelingSummary.vue";
export default {
  components: { ApexChart, ModelingSummary }
};
</script>

<style scoped>
.resultContainer {
  /* width: 1000px; */
  height: 1000px;
}
</style>
