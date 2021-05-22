<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-btn @click="createShape">Create</v-btn>
        <div id="myholder"></div
      ></v-col>
      <v-col cols="2">
        <v-card v-show="showXgBoostOption" dark rounded min-height="300px" min-width="200px">
          <v-container>
            <v-row>
              <v-col cols="12" v-for="(xgboostOption, index) in xgboostOptions" :key="index">
                <v-text-field
                  hide-details
                  outlined
                  dense
                  :label="xgboostOption"
                  placeholder=""
                ></v-text-field
              ></v-col>
            </v-row>
          </v-container> </v-card
      ></v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  data() {
    return {
      shape: null,
      graph: null,
      showXgBoostOption: false,
      xgboostOptions: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      xTrain: [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT"
      ],
      yTrain: ["MEDV"]
    };
  },
  components: {},
  methods: {
    createShape() {
      let cloned = this.shape.clone();
      cloned.addTo(this.graph);
    }
  },

  mounted() {
    //graph 정의
    this.graph = new joint.dia.Graph();
    //paper 정의
    let paper = new joint.dia.Paper({
      el: $("#myholder"),
      width: "100%",
      height: 800,
      model: this.graph,
      gridSize: 1
    });

    // line이 connect 되지 않으면 사라지도록
    paper.model.on("batch:stop", function() {
      var links = paper.model.getLinks();
      _.each(links, function(link) {
        var source = link.get("source");
        var target = link.get("target");
        if (source.id === undefined || target.id === undefined) {
          link.remove();
        }
      });
    });
    // default connector를 곡선으로 설정
    paper.options.defaultConnector = {
      name: "smooth",
      args: {
        radius: 20
      }
    };

    // Model 정의
    this.shape = new joint.shapes.devs.Model({
      position: {
        x: 500,
        y: 300
      },
      size: { width: 60, height: 30 },
      inPorts: ["in"],
      outPorts: ["out"],

      ports: {
        groups: {
          in: {
            position: "top",
            attrs: {
              ".port-body": {
                r: 5,
                padding: 3
                // fill: "#16A085",
              },

              ".port-label": {
                fill: "transparent"
              }
            }
          },
          out: {
            position: "bottom",
            attrs: {
              ".port-body": {
                r: 5
                // fill: "#E74C3C"
              },
              ".port-label": {
                fill: "transparent"
              }
            }
          }
        }
      },
      attrs: {
        ".label": {
          text: "XGBOOST",
          "ref-x": 0.5,
          "ref-y": 0.3,
          "font-size": 12,
          fill: "charcoal"
        },
        rect: {
          fill: "#a9a9b0",
          // add a corner radius
          rx: 15,
          ry: 15
        }
      }
    });
    //shape 화면의 render
    this.shape.addTo(this.graph);
    let shapeView = this.shape.findView(paper);

    let x_position = 30;
    //Input Cloning
    for (let i = 0; i < this.xTrain.length; i++) {
      let cloned = this.shape.clone();

      cloned.position(x_position, 80);
      cloned.attr(".label/text", this.xTrain[i]);

      //화면에 렌더링
      cloned.addTo(this.graph);
      var link = new joint.shapes.standard.Link({
        source: { id: cloned.id, port: "out" },
        target: { id: this.shape.id, port: "in" },
        connector: { name: "rounded" }
      });
      this.graph.addCell(link);

      x_position = x_position + 80;
    }
    // Target Cloning

    for (let i = 0; i < this.yTrain.length; i++) {
      let cloned = this.shape.clone();
      cloned.position(500, 520);
      cloned.attr(".label/text", this.yTrain[i]);

      //화면에 렌더링
      cloned.addTo(this.graph);
      var link = new joint.shapes.standard.Link({
        source: { id: this.shape.id, port: "out" },
        target: { id: cloned.id, port: "in" },
        connector: { name: "rounded" }
      });
      this.graph.addCell(link);
    }

    //Tools (shape)
    let boundaryTool = new joint.elementTools.Boundary();
    let removeButton = new joint.elementTools.Remove();

    let toolsView = new joint.dia.ToolsView({
      tools: [boundaryTool, removeButton]
    });

    shapeView.addTools(toolsView);
    shapeView.hideTools();
    //Tools (Link)
    let tools = [
      new joint.linkTools.Remove({
        distance: 20,
        action: function(evt) {
          // do stuff and remove link using
          this.model.remove({ ui: true, tool: this.cid });
        }
      })
      // new joint.linkTools.TargetArrowhead({
      //   display: "none"
      // })
    ];
    // link hover 설정 (toolbar show/hide)
    paper.on("link:mouseenter", function(linkView) {
      linkView.addTools(
        new joint.dia.ToolsView({
          name: "onhover",
          tools: tools
        })
      );
    });
    paper.on("link:mouseleave", function(linkView) {
      linkView.hideTools();
    });

    // element hover 설정 (toolbar show/hide)
    paper.on("element:contextmenu", function(shapeView) {
      shapeView.showTools();
    });
    paper.on("element:pointerclick", shapeView => {
      this.showXgBoostOption = !this.showXgBoostOption;
    });

    paper.on("element:mouseleave", function(shapeView) {
      shapeView.hideTools();
      // console.log(shapeView);
    });

    // shapeView.addTools(toolsView);
    // let rect = new joint.shapes.standard.Rectangle({});

    // rect.position(100, 30);
    // rect.resize(100, 40);
    // rect.attr({
    //   body: {
    //     fill: "#a9a9a9",
    //     rx: 5,
    //     ry: 5
    //   },
    //   label: {
    //     text: "SVR",
    //     fill: "white"
    //   }
    // });

    // let rect2 = rect.clone();
    // rect2.translate(300);

    // var link = new joint.shapes.standard.Link();

    // link.source(rect);
    // link.target(rect2);

    // this.graph.addCells([rect, rect2, link]);

    // var link2 = new joint.shapes.standard.Link();
    // link2.prop("source", { x: 0, y: 0 });
    // link2.prop("target", { x: 200, y: 200 });
    // // link2.prop("vertices", [{ x: 450, y: 700 }]);
    // link2.attr("root/title", "joint.shapes.standard.Link");
    // link2.attr("line/stroke", "#fe854f");
    // link2.addTo(this.graph);
  }
};
</script>
<style>
#stage {
  width: 1000px;
  height: 1000px;
}
</style>
