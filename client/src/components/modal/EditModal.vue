<template>
  <v-dialog v-model="dialog">
    <v-btn x-small min-width="20" min-height="30" @click="hideEditModal()"
      ><v-icon small>mdi-close</v-icon>
    </v-btn>
    <v-card>
      <v-container>
        <v-card-text style="text-align:center" class="title">Edit Data</v-card-text>
        <v-row justify="center" align="center">
          <TimeSeries :graphWidth="500" :graphHeight="500" :seriesName="column" :dialog="dialog"
        /></v-row>
        <v-row> <InfiniteTable /></v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<script>
import TimeSeries from "@/components/graph/TimeSeries";
import InfiniteTable from "@/components/layout/InfiniteTable";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";

export default {
  data() {
    return {
      dialog: false,
      column: null
    };
  },
  watch: {
    // dialog: function(data) {
    //   if (data == false) {
    //     this.resetSeries();
    //     console.log("reset");
    //   }
    // }
  },
  props: [],

  components: {
    TimeSeries,
    InfiniteTable
  },
  computed: {
    ...mapGetters("initialData", ["columns", "indexNum"])
  },
  methods: {
    hideEditModal() {
      // eventBus.$emit("hideEditModal", true);
    }
  },
  created() {
    eventBus.$on("openEditModal", column => {
      this.dialog = true;
      this.column = column;
    });
  }
};
</script>
