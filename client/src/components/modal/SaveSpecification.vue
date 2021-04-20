<template>
  <v-row justify="center">
    <v-dialog v-model="showSpecification" persistent max-width="300">
      <v-card>
        <v-card-subtitle>별도 저장</v-card-subtitle>
        <v-text-field v-model="name" :counter="10" label="파일명"></v-text-field>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="showSpecification = false">
            저장
          </v-btn>
          <v-btn color="green darken-1" text @click="dialog = false">
            취소
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { eventBus } from "@/main";
export default {
  data() {
    return {
      name: "",
      showSpecification: false
    };
  },

  created() {
    eventBus.$on("saveSpecification", specificationStatus => {
      this.showSpecification = true;
    });
  }
};
</script>
