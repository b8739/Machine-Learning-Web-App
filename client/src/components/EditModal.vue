<template>
  <div class="outerWrap">
    <DarkBackground />
    <div class="innerWrap">
      <button class="exitButton" @click="closeEditModal()">Close</button>
      <h1 class="title">Edit Data</h1>
      <div class="graphContainer">
        <TimeSeries :dataValue="dataValue" :date="date" :indexNum="indexNum" @xaxis="getXaxis" />
      </div>
      <InfiniteTable :xaxis="xaxis" :columns="columns" />
    </div>
  </div>
</template>
<script>
import TimeSeries from "./TimeSeries";
import InfiniteTable from "../components/InfiniteTable";
import DarkBackground from "../components/DarkBackground";
export default {
  data() {
    return {
      xaxis: {}
    };
  },
  props: ["dataValue", "date", "indexNum", "columns"],
  components: {
    TimeSeries,
    InfiniteTable,
    DarkBackground
  },
  methods: {
    getXaxis(xaxis) {
      this.xaxis = xaxis;
    },
    closeEditModal() {
      const newEditModalStatus = true;
      this.$emit("newEditModalStatus", newEditModalStatus);
    }
  }
};
</script>
<style scoped>
.innerWrap {
  padding: 25px 10px;
}
.title {
  text-align: center;
}
.graphContainer {
  width: 500px;
  margin: 0 auto;
}
.innerWrap {
  width: 850px;
  height: 850px;
  background-color: #fff;
  position: absolute;
  transform: translate(61%, 25%);
  top: 0;
  left: 0;
  z-index: 1000;
  overflow: scroll;
  overflow-x: hidden;
}

.innerWrap .exitButton {
  width: 90px;
  margin-left: 5px;
  background: #d8d6d6;
  border: none;
  border-radius: 5px;
  color: rgb(29, 27, 27);
  display: inline-block;
  font-size: 1.2em;
  font-weight: bold;
  padding: 1px 0;
  text-align: center;
  text-transform: capitalize;
  position: absolute;
  right: 20px;
}
</style>
