<template>
  <div class="dragYaxisBox">
    <draggable
      small
      outlined
      class="draggable"
      :options="{ group: 'dragGroup' }"
      :list="topColumns"
      :class="{ hoverEffectOn: hoverStatus }"
    >
      <v-chip v-for="(column, columnIndex) in columns[index]" :key="columnIndex" small outlined>{{
        column
      }}</v-chip>
    </draggable>

    <draggable
      class="draggable"
      :options="{ group: 'dragGroup' }"
      @change="onDragEvent"
      :list="middleColumns"
      :class="{ hoverEffectOn: hoverStatus }"
    >
      <v-chip
        class="rotating"
        v-for="(column, columnIndex) in middleColumns"
        :key="columnIndex"
        small
        outlined
        >{{ column }}</v-chip
      >
    </draggable>
    <draggable
      class="draggable"
      :options="{ group: 'dragGroup' }"
      @change="onDragBottomEvent"
      :list="bottomColumns"
      :class="{ hoverEffectOn: hoverStatus }"
    >
      <v-chip v-for="(column, columnIndex) in bottomColumns" :key="columnIndex" small outlined>{{
        column
      }}</v-chip>
    </draggable>
    <span class="yLabel">Y</span>
    <!-- <slot></slot> -->
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState, mapGetters } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      hoverStatus: false,
      columns: { topColumns: [], middleColumns: [], bottomColumns: [] },
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
          this.numOfDragElement--;
          eventBus.$emit("yaxisBeingRemoved", evt);
          break;
      }
    },
    onDragBottomEvent(evt) {
      let eventName = Object.keys(evt)[0];

      switch (eventName) {
        case "added":
          let axisInfo = {
            evt: evt,
            type: "axis",
            numOfDragElement: this.numOfDragElement
          };
          eventBus.$emit("addSyncBottom", axisInfo);
          //드래그 박스에 chip 하나만 유지하도록 초기화
          // this.topColumns = [evt.added.element];
          break;
        case "removed":
          eventBus.$emit("removeSyncBottom", evt);
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
      dataset: state => state.initialData.dataset
    }),
    ...mapGetters("initialData", ["indexNum"])
  },
  created() {
    eventBus.$on("hoverEffect", hoverStatus => {
      this.hoverStatus = hoverStatus;
    });
  }
};
</script>

<style scoped>
.rotating {
  /* transform: translateY(50px) rotate(90deg); */
}
.dragYaxisBox {
  /* border: 1px solid rgb(90, 47, 47); */
  /* margin: 50px 0; */
  height: 100%;
}
.yLabel {
  position: absolute;
  top: 47%;
}
.draggable {
  height: 33.333%;
  border-bottom: 1px solid lightgray;
}
.draggable:nth-child(3) {
  border-bottom: none;
}

.hoverEffectOn {
  margin-top: 2px;
  background-color: rgba(205, 205, 205, 0.695);
}
</style>
