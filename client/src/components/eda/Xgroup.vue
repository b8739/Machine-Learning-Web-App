<template>
  <v-row :class="{ hoverEffectOn: hoverStatus }" class="vrow xGroup" no-gutters justify="center">
    <v-col cols="12">
      <span class="groupXlabel">Group X</span>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="drag = true"
        @end="drag = false"
        :list="columns"
        @change="onDragEvent"
      >
        <v-chip v-for="(column, columnIndex) in columns" :key="columnIndex" small outlined>{{
          column
        }}</v-chip>
      </draggable>
    </v-col>
  </v-row>
</template>
<script>
import { eventBus } from "@/main";
import { mapState } from "vuex";
import draggable from "vuedraggable";

export default {
  data() {
    return {
      hoverStatus: false,
      columns: []
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
          let axisInfo = { evt: evt, type: "xGroup" };
          eventBus.$emit("xGroupBeingDragged", axisInfo);
          //드래그 박스에 chip 하나만 유지하도록 초기화
          this.columns = [evt.added.element];
          break;
        case "removed":
          eventBus.$emit("xGroupBeingRemoved", false);
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
      // columns: state => state.columns
    })
  }
};
</script>
<style scoped>
.hoverEffectOn {
  background-color: rgba(205, 205, 205, 0.695);
}
.xGroup {
  height: 100%;
}
.draggable {
  /* width: 33.333%; */
  height: 100%;
}
.groupXlabel {
  position: absolute;
  top: 25%;
  left: 45%;
}
</style>
