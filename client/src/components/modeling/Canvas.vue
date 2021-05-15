<template>
  <div>
    <button @click="button">button</button>
    <v-stage ref="stage" :config="configKonva">
      <v-layer>
        <!-- <v-line :config="configLine" :x="configInput.x" :y="configInput.y"></v-line>
        <v-label ref="hi" :config="configInput" @dragmove="checkPos1">
          <v-tag :config="configTag"> </v-tag>
          <v-text ref="hii" :config="configInputText"></v-text>
        </v-label>
        ><v-label ref="bye" :config="configInput" @dragmove="checkPos2">
          <v-tag :config="configTag"> </v-tag>
          <v-text ref="byee" :config="configTargetText"></v-text>
        </v-label> -->
        <v-label :draggable="true" :config="configLabel">
          <v-line ref="line" :config="configLine" :x="configInput.x" :y="configInput.y"></v-line>
          <v-circle
            ref="dragCircle"
            @dragmove="checkPos2"
            :config="configDragCircle"
            :x="configDragCircle.x"
            :y="configDragCircle.y"
            @dragend="resetPos"
          >
          </v-circle>
          <v-circle :config="configAnchorTop"> </v-circle>
          <v-tag :config="configTag"> </v-tag>
          <v-text ref="byee" :config="configTargetText"></v-text>
          <v-circle :config="configAnchorBottom"></v-circle>
        </v-label>
        <!-- <v-circle
        :config="configAnchor"
        :x="configLine.points[0]"
        :y="configLine.points[1]"
      ></v-circle>
   -->
      </v-layer>
    </v-stage>
  </div>
</template>
<script>
export default {
  data() {
    return {
      // canvas

      configKonva: {
        width: 1140,
        height: 700
      },
      configLabel: {
        x: 100,
        y: 100,
        opacity: 0.5
      },

      //   block
      configInput: {
        x: 10,
        y: 10,

        draggable: true
      },
      configTag: { fill: "lightgrey", cornerRadius: 5 },
      configInputText: {
        text: "Input",
        fontSize: 15,

        fill: "black",
        padding: 7
      },
      configTargetText: {
        text: "Target",
        fontSize: 15,

        fill: "black",
        padding: 7
      },
      //   circle
      configDragCircle: {
        zIndex: 1,
        x: 0,
        y: 0,
        draggable: true,
        radius: 5,
        // stroke: "#666",
        // opacity: 0.4,
        fill: "red",
        strokeWidth: 5
      },
      configAnchorTop: {
        x: 0,
        radius: 5,
        stroke: "#666",
        fill: "#ddd",
        strokeWidth: 2
      },
      configAnchorBottom: {
        x: 0,
        radius: 5,
        stroke: "#666",
        fill: "#ddd",
        strokeWidth: 2
      },

      configLine: {
        x: 0,
        y: 0,
        points: [0, 0],
        stroke: "grey",
        strokeWidth: 10,
        lineJoin: "round",
        lineCap: "round"
      },
      x: 500
    };
  },
  watch: {},
  computed: {},
  methods: {
    button() {},
    resetPos() {
      this.$refs.dragCircle.getNode().position({
        x: this.configAnchorTop.x + 5,
        y: this.configAnchorTop.y + 5
      });
      this.configLine.points[2] = this.$refs.dragCircle.getNode().position().x;
      this.configLine.points[3] = this.$refs.dragCircle.getNode().position().y;
    },
    // checkPos1() {
    //   this.configLine.points[0] = this.$refs.hi.getNode().x();
    //   this.configAnchor.x = this.$refs.hi.getNode().x();
    //   this.configLine.points[1] = this.$refs.hi.getNode().y();
    //   this.configAnchor.y = this.$refs.hi.getNode().y();
    // },
    checkPos2() {
      // this.configLine.points[2] = this.$refs.dragCircle.getNode().x();
      // this.configLine.points[3] = this.$refs.dragCircle.getNode().y();
      console.log(this.$refs.dragCircle.getNode().position());
      this.configLine.points[2] = this.$refs.dragCircle.getNode().position().x;
      this.configLine.points[3] = this.$refs.dragCircle.getNode().position().y;
    }
    // dragEvent() {
    //   this.configLine.x = this.$refs.hi.getNode().absolutePosition().x;
    //   this.configLine.y = this.$refs.hi.getNode().absolutePosition().y;
    // }
  },
  created() {
    // console.log(this.$refs.bye.getNode().width());
  },
  mounted() {
    //   circle

    this.configAnchorTop.x = this.$refs.byee.getNode().width() / 2;
    this.configAnchorTop.y = -6;
    this.configAnchorBottom.x = this.$refs.byee.getNode().width() / 2;
    this.configAnchorBottom.y = this.$refs.byee.getNode().width() / 2 + 6;
    //   line
    this.configLine.points[0] = this.configAnchorTop.x;
    this.configLine.points[1] = this.configAnchorTop.y;
    // dragCircle
    // this.configDragCircle.x = this.configAnchorTop.x;
  }
};
</script>
