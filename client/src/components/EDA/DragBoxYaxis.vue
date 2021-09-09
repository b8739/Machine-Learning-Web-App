<template>
  <div style="height:100%">
    <draggable
      :class="{
        'flex-column': classHandler,

        hoverEffectOn: hoverStatus
      }"
      class="draggable full-height d-flex  justify-center align-center"
      :options="{ group: 'dragGroup' }"
      @change="onDragEvent"
      :list="middleColumns"
    >
      <v-chip
        v-for="(column, columnIndex) in middleColumns"
        :key="columnIndex"
        class="rotating my-12"
        small
        outlined
        >{{ column }}</v-chip
      >
    </draggable>
  </div>

  <!-- <span class="yLabel">Y</span> -->
  <!-- <slot></slot> -->
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
import draggable from "vuedraggable";

export default {
  data() {
    return {
      hoverStatus: false,
      topColumns: [],
      middleColumns: [],
      bottomColumns: [],
      numOfDragElement: 0
    };
  },
  methods: {
    ...mapMutations("edaHandler", ["setYaxisColumn"]),
    ...mapMutations("edaHandler", ["removeYaxisColumn"]),
    ...mapMutations("edaHandler", ["setYaxisEvent"]),
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];

      // console.log(evt);

      switch (eventName) {
        case "added":
          this.setYaxisColumn(this.middleColumns);
          this.setYaxisEvent(evt);
          // eventBus.$emit("yaxisBeingDragged", axisInfo);
          this.numOfDragElement++;
          //드래그 박스에 chip 하나만 유지하도록 초기화
          // this.topColumns = [evt.added.element];
          break;
        case "moved":
          this.setYaxisEvent(evt);
          this.setYaxisColumn(this.middleColumns);
          break;
        case "removed":
          this.setYaxisEvent(evt);
          this.removeYaxisColumn(evt.removed.element);
          this.numOfDragElement--;

          break;
      }
    }
  },
  props: ["styleObject", "axisPosition"],

  components: {
    draggable
  },
  computed: {
    classHandler() {
      if (this.numOfDragElement > 1 || this.hoverStatus == true) {
        return true;
      }
    },
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

.yLabel {
  position: absolute;
  top: 47%;
}
.draggable {
  width: 100%;
  height: 100%;
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
