<template>
  <tr>
    <slot></slot>
    <!-- 3rd Column -->
    <td>
      <tr></tr>
      <tr></tr>
    </td>

    <!-- 4th Column -->
    <td></td>

    <!-- category 일 경우: -- 표시 -->
    <td></td>
    <!-- numeric 일 경우: Graph 표시 -->
  </tr>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,
      columns: state => state.initialData.columns,
      summarizedInfo: state => state.initialData.summarizedInfo,
      featureNameFlag: state => state.saveFlag.summarizedInfo
    })
  },
  props: ["column", "columnIndex"]
};
</script>
<style scoped>
td {
  padding: 15px 10px;
  border: 1px solid rgba(104, 102, 102, 0.644);
  border-bottom: none;
}
</style>
