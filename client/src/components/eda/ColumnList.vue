<template>
  <div>
    <!-- 여기에 요소 추가 -->
    <!-- column list -->

    <slot></slot>

    <!-- <v-divider></v-divider> -->
    <v-list>
      <draggable
        :options="{ group: 'dragGroup' }"
        @start="hoverOnDrag"
        @end="hoverOnDrag"
        :list="columns"
      >
        <v-list-item v-for="(column, columnIndex) in columns" :key="columnIndex">
          <v-list-item-content>
            <v-list-item-title>{{ column }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </draggable>
    </v-list>
  </div>
</template>
<script>
import { mapState, mapGetters } from "vuex";
import draggable from "vuedraggable";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      hoverStatus: true
    };
  },
  props: [],
  methods: {
    hoverOnDrag() {
      eventBus.$emit("hoverEffect", this.hoverStatus);
      this.hoverStatus = !this.hoverStatus;
    }
  },
  components: {
    draggable
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      columns: state => state.initialData.columns
    })
    // ...mapGetters("initialData", ["columns"])
  }
};
</script>
