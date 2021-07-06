<template>
  <div>
    <v-select
      :items="featureTypes"
      dense
      hide-details
      v-model="select"
      label="Change Feature"
      dark
    ></v-select>
  </div>
</template>
<script>
import { ButtonOption } from "@baklavajs/plugin-options-vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
import { TextOption } from "@baklavajs/plugin-options-vue";
export default {
  props: ["value", "name", "node", "editor"],
  data() {
    return {
      select: null,
      featureTypes: ["Input", "Target"]
    };
  },
  watch: {
    select: function(data) {
      // 기존 node 위치 정보
      const currentNodePosition = this.node.position;
      // 새로운 Node 생성
      let MyNode = this.node.editorInstance.nodeTypes.get(data);
      let n = new MyNode();
      this.node.editorInstance.addNode(n);
      // 기존 node 삭제
      this.node.editorInstance.removeNode(this.node);
      // 새로운 Node 위치 수정
      n.position = { x: currentNodePosition.x, y: currentNodePosition.y };
    }
  },
  components: {
    ButtonOption,
    InputOption
  },
  computed: {
    // selectOption() {
    //   return this.node.getOptionValue("Operation");
    // }
  },
  methods: {}
};
</script>
