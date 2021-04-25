<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">
          ‘data111’ 문서의 변경 사항을 저장하겠습니까?
        </v-card-title>
        <v-card-text>저장하지 않으면 변경 사항이 유실됩니다.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="saveSpecification">
            저장
          </v-btn>
          <v-btn color="green darken-1" text @click="dialog = false">
            저장하지 않음
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <SaveSpecification />
  </v-row>
</template>
<script>
import { eventBus } from "@/main";
import SaveSpecification from "@/components/save/SaveSpecification";
export default {
  data() {
    return {
      dialog: false
    };
  },
  components: {
    SaveSpecification
  },
  methods: {
    saveSpecification() {
      this.dialog = false;
      eventBus.$emit("saveSpecification", true);
    }
  },
  created() {
    eventBus.$on("openSaveChange", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>
