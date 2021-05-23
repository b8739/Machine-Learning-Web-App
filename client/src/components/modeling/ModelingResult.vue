<template>
  <div class="resultContainer">
    <v-container>
      <v-row>
        <v-col>
          <ApexChart />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import ApexChart from "@/components/modeling/ApexChart.vue";
export default {
  components: { ApexChart }
};
</script>

<style scoped>
.resultContainer {
  /* width: 1000px; */
  height: 1000px;
}
</style>
