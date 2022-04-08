<template>
  <div>
    <v-row align="center" justify="center" v-for="(parameter, index) in parameters" :key="index">
      <v-col> {{ parameter }}</v-col>
      <v-col>
        <input type="text" class="dark-input" v-on="listeners" v-model="userProps[index]"
      /></v-col>
    </v-row>
  </div>
</template>
<script>
import { TextOption } from "@baklavajs/plugin-options-vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
export default {
  extends: InputOption,
  data() {
    return {
      parameters: null,
      userProps: []
    };
  },
  computed: {
    listeners(ev) {
      return { ...this.$listeners, input: ev => this.$emit("input", this.userProps) };
    }
  },
  mounted() {
    this.parameters = this.value.parameters;
  }
};
</script>
