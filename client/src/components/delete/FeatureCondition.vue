<template>
  <!-- 새로운거 -->
  <v-card color="rgb(245,245,245) " class="mb-12">
    <v-container>
      <!-- 상단 (타이틀)-->
      <v-row>
        <v-col>
          <v-subheader>{{ columns.length }} 개 열</v-subheader>
        </v-col>
        <!-- <v-col> <slot></slot></v-col> -->
      </v-row>
      <!-- 하단 (컨텐츠) -->
      <v-row align="center">
        <!-- 좌측 -->
        <v-col cols="3">
          <ColumnList :style="style_columnList"> </ColumnList>
        </v-col>
        <!-- 우측 -->
        <v-col cols="9" justify="center">
          <v-row align="center" justify="center">
            <v-col cols="4">
              <!-- textfield (Feature)-->
              <v-text-field
                v-model="featureName"
                :value="featureName"
                placeholder="Feature"
                outlined
                dense
                hide-details
              ></v-text-field
            ></v-col>
            <!-- 부등호 버튼 (menu) -->
            <v-col cols="2">
              <div class="text-center">
                <v-menu offset-y>
                  <template v-slot:activator="{ on, attrs }">
                    <!-- 부등호 버튼 -->
                    <v-btn
                      class="ma-2"
                      outlined
                      fab
                      color="indigo"
                      x-small
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>{{ icons[iconIndex] }}</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      v-for="(item, index) in items"
                      :key="index"
                      @click="changeIcon(index)"
                    >
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div></v-col
            >
            <!-- textfield (Value) -->
            <v-col cols="4">
              <v-text-field
                :value="featureValue"
                v-model="featureValue"
                placeholder="Enter the Value"
                outlined
                dense
                hide-details
              ></v-text-field>
            </v-col>
          </v-row>

          <v-spacer></v-spacer>
        </v-col>
      </v-row>
    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="addCondition">
        Add Condition
      </v-btn>
      <v-btn color="red darken-1" text>
        Reset
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import { mapState } from "vuex";
import { eventBus } from "@/main";
import ColumnList from "@/components/delete/ColumnList.vue";
export default {
  data() {
    return {
      iconIndex: 0,
      featureName: "",
      featureValue: "",
      items: [
        { title: "=" },
        { title: "!=" },
        { title: ">" },
        { title: "<" },
        { title: ">=" },
        { title: ">=" }
      ],
      icons: [
        "mdi-equal",
        "mdi-not-equal",
        "mdi-greater-than",
        "mdi-less-than",
        "mdi-greater-than-or-equal",
        "mdi-less-than-or-equal"
      ],
      style_columnList: {
        height: "230px",
        "overflow-y": "scroll"
      }
    };
  },
  methods: {
    changeIcon(index) {
      this.iconIndex = index;
      // console.log("d");
    },
    addCondition() {
      eventBus.$emit("featureConditions", this.fullCondition);
    }
  },
  components: {
    ColumnList
  },

  created() {
    eventBus.$on("featureClickedEvent", column => {
      this.featureName = column;
    });
    eventBus.$on("stepTwoSkipEvent", skipStatus => {
      this.iconIndex = 0;
      this.featureName = null;
    });
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
      // columns: state => state.columns
    }),
    fullCondition() {
      return this.featureName + " " + this.items[this.iconIndex].title + " " + this.featureValue;
    }
  }
};
</script>
<style scoped>
.condition {
  height: 50%;
}
</style>
