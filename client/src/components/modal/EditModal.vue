<template
  ><div>
    <v-dialog v-model="dialog">
      <v-card v>
        <v-btn x-small right absolute min-width="20" min-height="30" @click="hideEditModal()"
          ><v-icon small>mdi-close</v-icon>
        </v-btn>
        <v-container>
          <v-card-text style="text-align:center" class="title">Edit Data</v-card-text>
          <v-row justify="center" align="center">
            <portal-target name="destination"> </portal-target>
          </v-row>
          <v-row> <InfiniteTable /></v-row>
        </v-container>
      </v-card>
    </v-dialog>
    <portal to="destination">
      <TimeSeries
        v-if="dialog"
        :graphWidth="500"
        :graphHeight="500"
        :seriesName="column"
        :dialog="dialog"
      />
    </portal>
  </div>
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
      column: null,
      graphReady: false
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
    ...mapState("initialData", ["columns"]),
    ...mapGetters("initialData", ["indexNum"])
  },
  methods: {
    hideEditModal() {
      this.dialog = false;
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
