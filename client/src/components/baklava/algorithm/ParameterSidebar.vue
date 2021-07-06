<template>
  <div>
    <v-btn @click="getValue">get value</v-btn>
    <v-row align="center" justify="center" v-for="(parameter, index) in parameterKeys" :key="index">
      <v-col> {{ parameter }}</v-col>
      <v-col>
        <input type="text" class="dark-input" v-on="listeners" v-model="parameterValues[parameter]"
      /></v-col>
    </v-row>
  </div>
</template>
<script>
import { InputOption } from "@baklavajs/plugin-options-vue";
export default {
  extends: InputOption,
  props: ["node"],
  data() {
    return {
      parameterKeys: null,
      parameterValues: {}
    };
  },
  methods: {
    getValue() {
      console.log(this.node);
    }
  },
  computed: {
    listeners(ev) {
      return {
        ...this.$listeners,
        input: ev => this.$emit("input", JSON.stringify(this.parameterValues))
      };
    }
  },
  mounted() {
    this.parameterKeys = this.value.parameterKeys;
  }
};
</script>
