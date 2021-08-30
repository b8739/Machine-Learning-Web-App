<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-card light min-height="500px">
      <v-container>
        <slot> </slot>
        <v-row justify="end">
          <portal-target name="tableInsertRow"> </portal-target>
        </v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  props: ["dialog"],
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      editMode: state => state.preprocessHandler.editMode,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus
    })
  }
};
</script>
