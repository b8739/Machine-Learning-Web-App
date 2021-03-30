<template>
  <div class="dragYaxisBox">
    <slot></slot>
    <v-chip-group :style="styleObject" column>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        @change="onDragEvent"
        :list="columns"
      >
        <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex">{{ column }}</v-chip>
      </draggable>
    </v-chip-group>
  </div>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";
export default {
  data() {
    return {
      columns: [""]
    };
  },
  methods: {
    onDragEvent(evt) {
      let eventName = Object.keys(evt)[0];
      console.log(eventName);
      switch (eventName) {
        case "added":
          let axisInfo = { evt: evt, axisPosition: this.axisPosition };
          eventBus.$emit("yaxisBeingDragged", axisInfo);
          //드래그 박스에 chip 하나만 유지하도록 초기화
          this.columns = [evt.added.element];
          break;
        case "removed":
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
      // columns: state => state.columns
    })
  }
};
</script>
<style scoped>
.dragYaxisBox {
  /* border: 1px solid rgb(90, 47, 47); */
  margin: 40px 0;
}
</style>
