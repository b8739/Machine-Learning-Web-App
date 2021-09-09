<template>
  <div class="dragXaxisBox">
    <draggable
      class="draggable d-flex  justify-center align-center"
      :class="{ hoverEffectOn: hoverStatus }"
      :options="{ group: 'dragGroup' }"
      @start="drag = true"
      @end="drag = false"
      :list="centerColumns"
      @change="onDragEvent"
    >
      <v-chip
        class="mx-12"
        v-for="(column, columnIndex) in centerColumns"
        :key="columnIndex"
        small
        outlined
        >{{ column }}</v-chip
      >
    </draggable>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

import draggable from "vuedraggable";

export default {
  data() {
    return {
      // columns: { leftColumns: [], centerColumns: [], rightColumns: [] },
      hoverStatus: false,

      centerColumns: [],

      numOfDragElement: 0
    };
  },
  props: ["styleObject", "axisPosition"],

  components: {
    draggable
  },
  methods: {
    ...mapMutations("edaHandler", ["setXaxisColumn"]),
    ...mapMutations("edaHandler", ["removeXaxisColumn"]),
    ...mapMutations("edaHandler", ["setXaxisEvent"]),

    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      // console.log(eventName);
      switch (eventName) {
        case "added":
          this.setXaxisColumn(this.centerColumns);
          this.setXaxisEvent(evt);
          this.numOfDragElement++;
          // eventBus.$emit("xaxisBeingDragged", axisInfo);
          break;
        case "moved":
          this.setXaxisEvent(evt);
          this.setXaxisColumn(this.centerColumns);
          break;
        case "removed":
          eventBus.$emit("xaxisBeingRemoved", false);
          this.setXaxisEvent(evt);
          this.removeXaxisColumn(evt.removed.element);
          this.numOfDragElement--;
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
      xaxisColumns: state => state.edaHandler.xaxisColumns
    }),
    ...mapGetters("initialData", ["indexNum"])
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
