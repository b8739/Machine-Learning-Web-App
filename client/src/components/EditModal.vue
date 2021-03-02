<template>
  <div class="innerWrap">
    <Histogram :dataValue="dataValue" :date="date" :indexNum="indexNum" @xaxis="getXaxis" />
    <InfiniteTable :xaxis="xaxis" :columns="columns" />
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
  props: ["dataValue", "date", "indexNum", "columns"],
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
.innerWrap {
  width: 850px;
  height: 850px;
  background-color: rgb(211, 211, 211);
  position: absolute;
  transform: translate(75%, 25%);
  top: 0;
  left: 0;
  z-index: 1000;
  overflow: scroll;
  overflow-x: hidden;
}
</style>
