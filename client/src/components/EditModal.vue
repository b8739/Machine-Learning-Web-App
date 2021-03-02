<template>
  <div class="wrap">
    <Histogram :dataValue="dataValue" :date="date" :indexNum="indexNum" @xaxis="getXaxis" />
    <InfiniteTable :xaxis="xaxis" />
  </div>
</template>
<script>
import Histogram from "./Histogram";
import InfiniteTable from "../components/InfiniteTable";
export default {
  data() {
    return {
      xaxis: {}
    };
  },
  props: ["dataValue", "date", "indexNum"],
  components: {
    Histogram,
    InfiniteTable
  },
  methods: {
    getXaxis(xaxis) {
      this.xaxis = xaxis;
    }
  }
};
</script>
<style scoped>
.wrap {
  width: 850px;
  height: 850px;
  background-color: rgb(211, 211, 211);
  position: absolute;
  transform: translate(75%, 25%);
  top: 0;
  left: 0;
  z-index: 1000;
}
</style>
