<template>
  <div>
    <v-btn @click="getValue">get value</v-btn>
    <v-row align="center" justify="center" v-for="(parameter, index) in parameters" :key="index">
      <v-col> {{ parameter }}</v-col>
      <v-col>
        <input type="text" class="dark-input" v-on="listeners" v-model="userProps[parameter]"
      /></v-col>
    </v-row>
  </div>
</template>
<script>
import { InputOption } from "@baklavajs/plugin-options-vue";
export default {
  extends: InputOption,
  data() {
    return {
      parameters: null,
      userProps: {}
    };
  },
  methods: {
    getValue() {
      console.log(this.userProps);
    }
  },
  computed: {
    listeners(ev) {
      return {
        ...this.$listeners,
        input: ev => this.$emit("input", JSON.stringify(this.userProps))
      };
    }
  },
  mounted() {
    this.parameters = this.value.parameters;
  }
};
</script>
