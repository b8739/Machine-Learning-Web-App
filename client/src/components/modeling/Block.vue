<template>
  <v-label :draggable="true" :config="configLabel">
    <v-line
      ref="line"
      v-for="(line, index) in lines"
      :key="index"
      :config="index == 0 ? configLine : configLine2"
    ></v-line>
    <v-line :config="testLine"></v-line>
    <v-circle ref="anchorTop" :config="configAnchorTop"> </v-circle>
    <v-circle
      ref="dragCircleTop"
      @dragmove="checkPos1"
      :config="configdragCircleTop"
      @dragend="resetPos"
    >
    </v-circle>

    <v-tag :config="configTag"> </v-tag>
    <v-text ref="byee" :config="configTargetText"></v-text>
    <v-circle ref="anchorBottom" :config="configAnchorBottom"></v-circle>
    <v-circle
      ref="dragCircleBottom"
      @dragmove="checkPos2"
      :config="configdragCircleBottom"
      @dragend="resetPos"
      @mouseover="mouseoverevent"
    >
    </v-circle>
  </v-label>
</template>
<script>
export default {
  data() {
    return {
      testLine: {
        x: 100,
        y: 50,
        points: [50, 50, 20, 200, 300, 300],
        fill: "red",
        tension: 0.5,
        width: 50,
        strokeWidth: 1,
        stroke: "green"
      },
      // canvas
      lines: [1, 1],

      configGroup: {
        x: 50,
        y: 50
      },
      configLabel: {
        x: 10,
        y: 10
      },

      //   block
      configInput: {
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
        text: "SVR",
        fontSize: 15,

        fill: "black",
        padding: 7
      },
      //   circle
      configdragCircleTop: {
        x: 0,
        y: 0,
        // opacity: 0.1,

        draggable: true,
        radius: 5,
        fill: "red",
        strokeWidth: 5
      },
      configdragCircleBottom: {
        x: 0,
        y: 0,

        draggable: true,
        radius: 6,
        fill: "blue",
        strokeWidth: 5
      },
      configAnchorTop: {
        x: 0,
        radius: 5,
        stroke: "#666",
        fill: "#ddd",
        strokeWidth: 2,
        opacity: 0.2
      },
      configAnchorBottom: {
        x: 0,
        radius: 5,
        stroke: "#666",
        fill: "#ddd",
        strokeWidth: 2,
        opacity: 0.2
      },

      configLine: {
        tension: 0.1,
        points: [0, 0],
        stroke: "grey",
        strokeWidth: 10,
        lineJoin: "round",
        lineCap: "round"
      },
      configLine2: {
        points: [0, 0],
        stroke: "grey",
        strokeWidth: 10,
        lineJoin: "round",
        lineCap: "round"
      }
    };
  },
  watch: {},
  computed: {},
  methods: {
    mouseoverevent() {
      alert("hi");
    },

    resetPos() {
      this.$refs.dragCircleTop.getNode().position({
        x: this.configAnchorTop.x,
        y: this.configAnchorTop.y
      });
      this.$refs.dragCircleBottom.getNode().position({
        x: this.configAnchorBottom.x,
        y: this.configAnchorBottom.y
      });

      this.$refs.line[0].getNode().points()[2] = 0;
      this.$refs.line[0].getNode().points()[3] = 0;
      this.$refs.line[1].getNode().points()[2] = 0;
      this.$refs.line[1].getNode().points()[3] = 0;
    },
    checkPos1() {
      this.$refs.line[0].getNode().points()[2] =
        this.$refs.dragCircleTop.getNode().position().x - 25; //왠지 모르지만 25 정도를 안빼주면 격차가 생김

      this.$refs.line[0].getNode().points()[3] = this.$refs.dragCircleTop.getNode().position().y;
    },
    checkPos2() {
      this.$refs.line[1].getNode().points()[2] =
        this.$refs.dragCircleBottom.getNode().position().x - 20;
      this.$refs.line[1].getNode().points()[3] =
        this.$refs.dragCircleBottom.getNode().position().y - 25;
    }
  },
  created() {
    // console.log(this.$refs.bye.getNode().width());
  },
  mounted() {
    console.log("mounted");
    //   circle
    this.configAnchorTop.x = this.$refs.byee.getNode().width() / 2;
    this.configAnchorTop.y = -6;

    this.configAnchorBottom.x = this.$refs.byee.getNode().width() / 2;
    this.configAnchorBottom.y = this.$refs.byee.getNode().width() / 2 + 12;
    //첫 위치
    this.configdragCircleTop.x = this.configAnchorTop.x;
    this.configdragCircleTop.y = this.configAnchorTop.y;

    this.configdragCircleBottom.x = this.configAnchorBottom.x;
    this.configdragCircleBottom.y = this.configAnchorBottom.y;

    //   line
    this.$refs.line[0].getNode().position({
      x: this.configAnchorTop.x,
      y: this.configAnchorTop.y
    });
    this.$refs.line[1].getNode().position({
      x: this.configAnchorBottom.x,
      y: this.configAnchorBottom.y
    });
  }
};
</script>
