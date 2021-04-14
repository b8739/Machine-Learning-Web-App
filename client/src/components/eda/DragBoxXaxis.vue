<template>
  <div class="dragXaxisBox">
    <v-row class="dragXaxisBox" no-gutters>
      <v-col cols="4" :class="{ hoverEffectOn: hoverStatus }">
        <draggable
          class="draggable"
          :options="{ group: 'dragGroup' }"
          @start="drag = true"
          @end="drag = false"
          :list="leftColumns"
        >
          <v-chip v-for="(column, columnIndex) in leftColumns" :key="columnIndex" small outlined>{{
            column
          }}</v-chip>
        </draggable>
      </v-col>
      <v-col cols="4" :class="{ hoverEffectOn: hoverStatus }">
        <span class="xLabel">X</span>
        <draggable
          class="draggable"
          :options="{ group: 'dragGroup' }"
          @start="drag = true"
          @end="drag = false"
          :list="centerColumns"
          @change="onDragEvent"
        >
          <v-chip
            v-for="(column, columnIndex) in centerColumns"
            :key="columnIndex"
            small
            outlined
            >{{ column }}</v-chip
          >
        </draggable>
      </v-col>
      <v-col cols="4" :class="{ hoverEffectOn: hoverStatus }">
        <draggable
          class="draggable"
          :options="{ group: 'dragGroup' }"
          @start="drag = true"
          @end="drag = false"
          :list="rightColumns"
        >
          <v-chip v-for="(column, columnIndex) in rightColumns" :key="columnIndex" small outlined>{{
            column
          }}</v-chip>
        </draggable>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";

export default {
  data() {
    return {
      // columns: { leftColumns: [], centerColumns: [], rightColumns: [] },
      hoverStatus: false,
      leftColumns: [],
      centerColumns: [],
      rightColumns: []
    };
  },
  props: ["styleObject", "axisPosition"],

  components: {
    draggable
  },
  methods: {
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      console.log(eventName);
      switch (eventName) {
        case "added":
          let axisInfo = { evt: evt, type: "axis" };
          eventBus.$emit("xaxisBeingDragged", axisInfo);
          //드래그 박스에 chip 하나만 유지하도록 초기화
          this.centerColumns = [evt.added.element];
          break;
        case "removed":
          eventBus.$emit("xaxisBeingRemoved", false);
          break;
      }
    }
  },
  created() {
    eventBus.$on("hoverEffect", hoverStatus => {
      this.hoverStatus = hoverStatus;
    });
  },
  computed: {
    ...mapState({
      dataset: state => state.dataset,
      indexNum: state => state.indexNum
      // leftColumns: state => state.leftColumns
    })
  }
};
</script>
<style scoped>
.dragXaxisBox {
  height: 100%;
}
.draggable {
  /* width: 33.333%; */
  height: 100%;
  border-right: 1px solid lightgray;
}
.draggable:nth-child(3) {
  border-right: none;
}
.xLabel {
  position: absolute;
  top: 25%;
  left: 50%;
}
.hoverEffectOn {
  border: 1px solid white;
  background-color: rgba(205, 205, 205, 0.695);
}
</style>
