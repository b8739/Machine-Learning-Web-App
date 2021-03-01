<template>
  <div class="wrap">
    <Histogram :dataValue="dataValue" :date="date" :indexNum="indexNum" />
  </div>
</template>
<script>
import Histogram from "./Histogram";
export default {
  data() {
    return {};
  },
  props: ["dataValue", "date", "indexNum"],
  components: {
    Histogram
  }
};
</script>
<style scoped>
.wrap {
  width: 850px;
  height: 850px;
  background-color: #fff;
  position: absolute;
  transform: translate(75%, 25%);
  top: 0;
  left: 0;
  z-index: 1000;
}
</style>
