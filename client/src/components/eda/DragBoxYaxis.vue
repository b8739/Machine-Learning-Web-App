<template>
  <div class="dragYaxisBox">
    <draggable
      class="draggable"
      :options="{ group: 'dragGroup' }"
      @start="drag = true"
      @end="drag = false"
      :list="topColumns"
    >
      <v-chip v-for="(column, columnIndex) in topColumns" :key="columnIndex" small outlined>{{
        column
      }}</v-chip>
    </draggable>
    <draggable
      class="draggable"
      :options="{ group: 'dragGroup' }"
      @start="drag = true"
      @end="drag = false"
      @change="onDragEvent"
      :list="middleColumns"
    >
      <span class="yLabel">Y</span>
      <v-chip v-for="(column, columnIndex) in middleColumns" :key="columnIndex" small outlined>{{
        column
      }}</v-chip>
    </draggable>
    <draggable
      class="draggable"
      :options="{ group: 'dragGroup' }"
      @start="drag = true"
      @end="drag = false"
      :list="bottomColumns"
    >
      <v-chip v-for="(column, columnIndex) in bottomColumns" :key="columnIndex" small outlined>{{
        column
      }}</v-chip>
    </draggable>
    <!-- <slot></slot> -->
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      topColumns: [],
      middleColumns: [],
      bottomColumns: [],
      numOfDragElement: 0
    };
  },
  methods: {
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      console.log(evt);
      switch (eventName) {
        case "added":
          let axisInfo = {
            evt: evt,
            type: "axis",
            numOfDragElement: this.numOfDragElement
          };
          eventBus.$emit("yaxisBeingDragged", axisInfo);
          this.numOfDragElement++;
          //드래그 박스에 chip 하나만 유지하도록 초기화
          // this.topColumns = [evt.added.element];
          break;
        case "removed":
          numOfDragElement--;
          eventBus.$emit("yaxisBeingRemoved", false);
          break;
      }
    }
  },
  props: ["styleObject", "axisPosition"],

  components: {
    draggable
  },
  computed: {
    ...mapState({
      dataset: state => state.dataset,
      indexNum: state => state.indexNum
      // topColumns: state => state.topColumns
    })
  }
};
</script>
<style scoped>
.dragYaxisBox {
  /* border: 1px solid rgb(90, 47, 47); */
  /* margin: 50px 0; */
  height: 100%;
}
.yLabel {
  position: absolute;
  top: 45%;
}
.draggable {
  height: 33.333%;
  border-bottom: 1px solid lightgray;
}
.draggable:nth-child(3) {
  border-bottom: none;
}
</style>
